import collections
import datetime
import json
import multiprocessing
import os
import subprocess
import sys
import time

_SSHD_BINARY_PATH = "/usr/sbin/sshd"

EnvironmentConfig = collections.namedtuple(
    "EnvironmentConfig",
    ["hosts", "port", "is_chief", "pools", "job_id"])


class DeadlineExceededError(Exception):
  """Indicates an action took too long."""
  pass


def _sub_process_num_gpus(unused):
  del unused
  # This is imported here so that we don't load tensorflow in the parent
  # process. Once the sub-process exits, it releases its allocated GPU memory.
  from tensorflow.python.client import device_lib
  local_device_protos = device_lib.list_local_devices()
  gpus = [x.name for x in local_device_protos if x.device_type == "GPU"]
  return len(gpus)


def _get_available_gpus():
  """Returns the number of GPUs on the machine."""
  pool = multiprocessing.Pool(1)
  result = pool.map(_sub_process_num_gpus, [None])[0]
  pool.close()
  pool.join()
  return result


def parse_environment_config(env_config_str, job_id):
  """Parses environment config and returns a list of hosts as well as the role.

  Returns:
    An EnvironmentConfig.
  """
  if env_config_str:
    ssh_port = -1
    env_config_json = json.loads(env_config_str)
    cluster = env_config_json.get("cluster")
    if not cluster:
      return None, True
    hosts = []
    pools = collections.defaultdict(list)
    for pool_type, tasks_per_type in cluster.items():
      if pool_type == "master":
        pool_type = "chief"
      for host_and_port in tasks_per_type:
        host, port = host_and_port.split(":")
        if host == "127.0.0.1":
          host = "localhost"
        port = int(port)
        if ssh_port == -1:
          ssh_port = port
        elif ssh_port != port:
          raise ValueError("Inconsistent ssh ports across tasks %d != %d." %
                           (ssh_port, port))
        hosts.append(host)
        pools[pool_type].append(host)
    is_chief = False
    has_chief = "chief" in pools
    if (env_config_json["task"]["type"] == "master" or
        env_config_json["task"]["type"] == "chief"):
      is_chief = True
      if int(env_config_json["task"]["index"]) != 0:
        raise ValueError("Only one master node is expected.")
    elif ((not has_chief) and
          (env_config_json["task"]["type"] == "worker") and
          int(env_config_json["task"]["index"]) == 0):
      is_chief = True
      pools["chief"].append(pools["worker"].pop(0))
    elif env_config_json["task"]["type"] != "worker":
      raise ValueError("Unexpected task type for Horovod training: %s." %
                       env_config_json["task"]["type"])
    return EnvironmentConfig(hosts=hosts, port=port, is_chief=is_chief,
                             pools=pools, job_id=job_id)
  else:
    return EnvironmentConfig(hosts=["localhost"], port=2222, is_chief=True,
                             pools={"chief": ["localhost"]}, job_id=job_id)


def start_ssh_server(port, is_chief):
  ssh_server_command = [_SSHD_BINARY_PATH, "-p", str(port)]
  if not is_chief:
    ssh_server_command.append("-D")
  completed = subprocess.call(ssh_server_command)
  if completed != 0:
    raise OSError("SSH server did not start successfully.")


def wait_for_ssh_servers(hosts, port, timeout_seconds):
  deadline_datetime = datetime.datetime.utcnow() + datetime.timedelta(
      seconds=timeout_seconds)
  unavailable_hosts = []
  while datetime.datetime.utcnow() < deadline_datetime:
    unavailable_hosts = []
    for host in hosts:
      ssh_command = ["ssh", "-q", host, "-p", str(port), "true"]
      result = subprocess.call(ssh_command)
      if result != 0:
        unavailable_hosts.append(host)
    if not unavailable_hosts:
      return
    # Retry in 1 second.
    time.sleep(1)

  raise DeadlineExceededError(
      "Timed out while waiting for all hosts to start. "
      "Hosts still not available: %s. TASK_STARTUP_TIMEOUT_SECONDS=%d" %
      (unavailable_hosts, timeout_seconds))


def run_horovod(env_config, jobs_per_host, args):
  env = dict(os.environ)
  del env["TF_CONFIG"]

  num_jobs = len(env_config.hosts) * jobs_per_host
  hosts = ",".join("%s:%d" % (h, jobs_per_host) for h in env_config.hosts)
  horovod_command = [
      "horovodrun", "--ssh-port", str(env_config.port), "-H",
      hosts, "--num-proc", str(num_jobs)
  ]
  horovod_command.extend(args)
  exit_code = subprocess.call(horovod_command, env=env)
  return exit_code


def benchmark_network(env_config):
  if not env_config.pools["worker"]:
    raise ValueError("No workers in the pool to do network benchmarking.")
  iperf_server = ["iperf", "-s", "-p", "6000"]
  server = subprocess.Popen(iperf_server)
  # Wait 10 seconds for the local server to start.
  time.sleep(10)
  iperf_command = ["ssh", "-q", env_config.pools["worker"][0], "-p",
                   str(env_config.port),
                   "iperf", "-p", "6000", "-c", env_config.pools["chief"][0]]
  subprocess.call(iperf_command)
  server.kill()


def copy_files_recursively(src, dest):
  if not dest.startswith("gs://"):
    try:
      os.makedirs(dest)
    except OSError:
      pass
  copy_cmd = ["gsutil", "-m", "rsync", "-r", src, dest]
  exit_code = subprocess.call(copy_cmd)
  if exit_code != 0:
    raise RuntimeError("Error while copying %s to %s" % (src, dest))
  return exit_code


def main():
  env_config_str = os.environ.get("TF_CONFIG")
  job_id = os.environ.get("CLOUD_ML_JOB_ID", "localrun")

  env_config = parse_environment_config(env_config_str, job_id)
  print (env_config, env_config.pools, env_config.hosts, os.environ)
  if os.environ.get("STAGE_GCS_PATH", False):
    copy_files_recursively(
        os.environ.get("STAGE_GCS_PATH"),
        os.environ.get("STAGING_DIR", "/input"))

  start_ssh_server(env_config.port, env_config.is_chief)
  max_num_retries = os.environ.get("NUM_HOROVOD_RETRIES", 1)
  if env_config.is_chief:
    exit_code = 0
    for retry in range(max_num_retries):
      staging_timeout_seconds = int(
          os.environ.get("TASK_STARTUP_TIMEOUT_SECONDS", 600))
      wait_for_ssh_servers(env_config.hosts, env_config.port,
                           staging_timeout_seconds)
      if os.environ.get("BENCHMARK_NETWORK", False):
        benchmark_network(env_config)
      num_gpus = _get_available_gpus()
      # If there are no GPUs, we can just run single process per machine.
      jobs_per_host = max(1, num_gpus)
      args = sys.argv[1:]
      exit_code = run_horovod(env_config=env_config, jobs_per_host=jobs_per_host,
                              args=args)
      if exit_code == 0:
        break
      else:
        print ("Retrying...", retry, "out of", max_num_retries)
    if os.environ.get("GCS_OUTPUT_PATH", False):
      copy_files_recursively(
          os.environ.get("OUTPUT_DIR", "/output"),
          os.path.join(os.environ.get("GCS_OUTPUT_PATH"), job_id))
    sys.exit(exit_code)


if __name__ == "__main__":
  main()
