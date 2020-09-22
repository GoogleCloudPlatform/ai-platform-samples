"""Report JupyterLab Metrics to Google Cloud Monitoring."""
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from google.cloud import monitoring_v3

import argparse
import requests
from requests.adapters import HTTPAdapter
import subprocess
import time

# JupyterLab default settings.
JUPYTER_HOST = "http://127.0.0.1"
JUPYTER_PORT = 8080

# JupyterLab service status
JUPYTERLAB_MEMORY_HIGH = "systemctl show jupyter.service --no-pager | grep MemoryHigh | awk -F \"=\" '{print $2}'"
JUPYTERLAB_MEMORY_MAX = "systemctl show jupyter.service --no-pager | grep MemoryMax | awk -F \"=\" '{print $2}'"
JUPYTERLAB_MEMORY_CURRENT = "systemctl show jupyter.service --no-pager | grep MemoryCurrent | awk -F \"=\" '{print $2}'"
JUPYTERLAB_STATUS = "if [ \"$(systemctl show --property ActiveState jupyter | awk -F \"=\" '{print $2}')\" == \"active\" ]; then echo 1; else echo 0; fi"

# JupyterLab API checks
API_STATUS = "{}:{}/api/status".format(JUPYTER_HOST, JUPYTER_PORT)
API_KERNELS = "{}:{}/api/kernels".format(JUPYTER_HOST, JUPYTER_PORT)
API_SESSIONS = "{}:{}/api/sessions".format(JUPYTER_HOST, JUPYTER_PORT)
API_TERMINALS = "{}:{}/api/terminals".format(JUPYTER_HOST, JUPYTER_PORT)

# Docker Service and Inverse Proxy agent
DOCKER_STATUS = "if [ \"$(systemctl show --property ActiveState docker | awk -F \"=\" '{print $2}')\" == \"active\" ]; then echo 1; else echo 0; fi"
PROXY_AGENT_STATUS = "if [ \"$( docker container inspect -f '{{ .State.Running}}' proxy-agent )\" == \"true\" ]; then echo 1; else echo 0; fi"

METADATA_SERVER = "http://metadata/computeMetadata/v1/instance/"
METADATA_FLAVOR = {"Metadata-Flavor": "Google"}

ULONG_MAX = 18446744073709551615
MAX_RETRIES = 2
HTTP_TIMEOUT_SESSION = 5


def get_args():
    """Argument parser.

    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--sampling_interval',
        type=int,
        default=15,
        help='number of seconds to wait while collecting metrics, default=15')
    args, _ = parser.parse_known_args()
    return args


def get_session():
    """Return an HTTP Session. """
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    return session


def api_status():
    """Collects Jupyter API status.
    curl -s http://127.0.0.1:8080/api/status

    Returns:
        Number of connections and kernels.

    Raises:
        Exception: Unable to contact API.
    """
    try:
        total_connections = 0
        total_kernels = 0
        session = get_session()
        r = session.get(API_STATUS, timeout=HTTP_TIMEOUT_SESSION)
        r.raise_for_status()
        result = r.json()
        if result is not None:
            total_connections = result.get("connections")
            total_kernels = result.get("kernels")
        return total_connections, total_kernels
    except requests.exceptions.RequestException as e:
        print("api_status. Unable to contact Jupyter API {}".format(e))
        return -1, -1
    except ValueError as e:
        print("api_status. Unable to process Jupyter API response {}".format(e))
        return -1, -1


def api_sessions():
    """Collects API terminals details.

    Returns:
        The number of active sessions.
    """
    try:
        total_sessions = 0
        session = get_session()
        r = session.get(API_SESSIONS, timeout=HTTP_TIMEOUT_SESSION)
        r.raise_for_status()
        sessions = r.json()
        if sessions is not None:
            total_sessions = len(sessions)
        return total_sessions
    except requests.exceptions.RequestException as e:
        print("api_sessions. Unable to contact Jupyter API {}".format(e))
        return -1
    except ValueError as e:
        print(
            "api_sessions. Unable to process Jupyter API response {}".format(e))
        return -1


def api_terminals():
    """Collects API terminals details.

    Returns:
        The number of active terminals.
    """
    try:
        total_terminals = 0
        session = get_session()
        r = session.get(API_TERMINALS, timeout=HTTP_TIMEOUT_SESSION)
        r.raise_for_status()
        terminals = r.json()
        if terminals is not None:
            total_terminals = len(terminals)
        return total_terminals
    except requests.exceptions.RequestException as e:
        print("api_terminals. Unable to contact Jupyter API {}".format(e))
        return -1
    except ValueError as e:
        print("api_terminals. Unable to process Jupyter API response {}".format(
            e))
        return -1


def get_notebooks_service(shell_command):
    """Obtain JupyterLab status.

    Args:
      shell_command: (str) Parse a shell command and return status code.

    Returns:
      A metric value.
    """
    try:
        metric_value = subprocess.run([
            "/bin/bash", "-c",
            shell_command], stdout=subprocess.PIPE, text=True).stdout
        # 2^64-1 - ULONG_MAX. Displayed when Service is stopped.
        metric_value = int(metric_value)
        if metric_value == ULONG_MAX:
            return -1
        return metric_value
    except subprocess.CalledProcessError as e:
        print(e)
        return -1
    except ValueError:
        return -1


def _get_resource_values():
    """Get Resources Values

    Return:
        A dictionary with Notebook instance resource values.
    """
    # Get instance information
    data = requests.get('{}zone'.format(METADATA_SERVER),
                        headers=METADATA_FLAVOR).text
    instance_id = requests.get(
        '{}id'.format(METADATA_SERVER), headers=METADATA_FLAVOR).text
    client = monitoring_v3.MetricServiceClient()
    # Collect zone
    zone = data.split('/')[3]
    # Collect project id
    project_id = data.split('/')[1]
    resource_values = {
        'client': client,
        'instance_id': instance_id,
        'zone': zone,
        'project_id': project_id
    }
    return resource_values


def report_metric(metric_value, metric_type, resource_values):
    """Create time series for report.

    Args:
      metric_value: (int) Report metric value.
      metric_type: (str) Metric type
      resource_values: (dict) Contains resources information
    """
    # Extract Notebook instance details.
    client = resource_values.get("client")
    project_id = resource_values.get("project_id")
    instance_id = resource_values.get("instance_id")
    zone = resource_values.get("zone")
    project_name = client.project_path(project_id)

    # TimeSeries definition.
    series = monitoring_v3.types.TimeSeries()
    metric_type = "custom.googleapis.com/notebooks/{type}".format(
        type=metric_type)
    series.metric.type = metric_type
    series.resource.type = "gce_instance"
    series.resource.labels["instance_id"] = instance_id
    series.resource.labels["zone"] = zone
    series.resource.labels["project_id"] = project_id
    point = series.points.add()
    point.value.int64_value = metric_value
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int(
        (now - point.interval.end_time.seconds) * 10 ** 9)
    client.create_time_series(project_name, [series])


def report_metrics(sampling_interval, resource_values):
    """Collects metrics

    Args:
      sampling_interval:(int) Wait time.
      resource_values:(dict) Dict to pass to Stackdriver.

    Returns:
    """
    while True:
        try:
            report_metric(
                metric_value=get_notebooks_service(JUPYTERLAB_STATUS),
                metric_type="jupyterlab_status",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(DOCKER_STATUS),
                metric_type="docker_status",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(PROXY_AGENT_STATUS),
                metric_type="proxy_agent_status",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(JUPYTERLAB_MEMORY_CURRENT),
                metric_type="jupyterlab_memory_current",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(JUPYTERLAB_MEMORY_HIGH),
                metric_type="jupyterlab_memory_high",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(JUPYTERLAB_MEMORY_MAX),
                metric_type="jupyterlab_memory_max",
                resource_values=resource_values)
            report_metric(
                metric_value=api_status()[1],
                metric_type="connections",
                resource_values=resource_values)
            report_metric(
                metric_value=api_status()[0],
                metric_type="kernels",
                resource_values=resource_values)
            report_metric(
                metric_value=api_sessions(),
                metric_type="sessions",
                resource_values=resource_values)
            report_metric(
                metric_value=api_terminals(),
                metric_type="terminals",
                resource_values=resource_values)
        except IndexError as e:
            print("IndexError found reporting metrics {}".format(e))
        except Exception as e:
            print("Exception found reporting metrics {}".format(e))
        time.sleep(sampling_interval)


def main(args):
    resource_values = _get_resource_values()
    print("AI Platform Notebooks Collection Agent starting...")
    report_metrics(args.sampling_interval, resource_values)


if __name__ == '__main__':
    args = get_args()
    main(args)
