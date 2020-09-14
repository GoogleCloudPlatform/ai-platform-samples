"""Report JupyterLab Metrics"""
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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.cloud import monitoring_v3

import argparse
import requests
import subprocess
import time

JUPYTER_HOST = "http://127.0.0.1"
JUPYTER_PORT = 8080

_API_STATUS = "{}:{}/api/status".format(JUPYTER_HOST, JUPYTER_PORT)
_API_KERNELS = "{}:{}/api/kernels".format(JUPYTER_HOST, JUPYTER_PORT)
_API_SESSIONS = "{}:{}/api/sessions".format(JUPYTER_HOST, JUPYTER_PORT)
_API_TERMINALS = "{}:{}/api/terminals".format(JUPYTER_HOST, JUPYTER_PORT)
_JUPYTERLAB_MEMORY_HIGH = "systemctl show jupyter.service --no-pager | grep MemoryHigh | awk -F \"=\" '{print $2}'"
_JUPYTERLAB_MEMORY_MAX = "systemctl show jupyter.service --no-pager | grep MemoryMax | awk -F \"=\" '{print $2}'"
_JUPYTERLAB_MEMORY_CURRENT = "systemctl show jupyter.service --no-pager | grep MemoryCurrent | awk -F \"=\" '{print $2}'"
_JUPYTERLAB_STATUS = " if [ \"$(systemctl show --property ActiveState jupyter | awk -F \"=\" '{print $2}')\" == \"active\" ]; then echo 1; else echo 0; fi"
_PROXY_AGENT_STATUS="if [ \"$( docker container inspect -f '{{.State.Running}}' proxy-agent )\" == \"true\" ]; then echo 1; else echo 0; fi"


_METADATA_SERVER = "http://metadata/computeMetadata/v1/instance/"
_METADATA_FLAVOR = {"Metadata-Flavor": "Google"}


class Kernel(object):
    """Represents a Jupyter Kernel."""

    def __init__(self, kernel_id, name, last_activity, execution_state,
                 connections):
        self._kernel_id = kernel_id
        self._name = name
        self._last_activity = last_activity
        self._execution_state = execution_state
        self._connections = connections

    @property
    def kernel_id(self):
        return self._kernel_id

    @property
    def name(self):
        return self._name

    @property
    def last_activity(self):
        return self._last_activity

    @property
    def execution_state(self):
        return self._execution_state

    @property
    def connections(self):
        return self._connections

    def __str__(self):
        return "{},{},{},{},{}".format(self.kernel_id, self.name,
                                       self.last_activity,
                                       self.execution_state, self.connections)


def get_args():
    """Argument parser.

    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--sleep',
        type=int,
        default=30,
        help='number of seconds to wait while collecting metrics, default=15')
    args, _ = parser.parse_known_args()
    return args


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
        r = requests.get(_API_STATUS)
        r.raise_for_status()
        result = r.json()
        if result is not None:
            total_connections = result.get("connections")
            total_kernels = result.get("kernels")
        return total_connections, total_kernels
    except requests.exceptions.RequestException as e:
        print("Unable to contact API {}".format(e))
        return -1, -1
    except ValueError as e:
        print("Unable to process API response {}".format(e))
        return -1, -1


def api_kernels():
    """Collects Jupyter API Kernels information.
    curl -s http://127.0.0.1:8080/api/kernels

    Returns:
        Connections and Kernels

    Raises:
        Exception: Unable to contact API.
    """
    try:
        kernel_list = []
        r = requests.get(_API_KERNELS)
        r.raise_for_status()
        kernels = r.json()
        if kernels is not None:
            for kernel in kernels:
                k = Kernel(kernel_id=kernel.get("id"),
                           name=kernel.get("name"),
                           last_activity=kernel.get("last_activity"),
                           execution_state=kernel.get("execution_state"),
                           connections=kernel.get("connections"))
                kernel_list.append(k)
        return kernel_list
    except requests.exceptions.RequestException as e:
        print("Unable to contact API {}".format(e))
    except ValueError as e:
        print("Unable to process API response {}".format(e))


def api_sessions():
    """Collects API terminals details.

    Returns:
        The number of active sessions.
    """
    try:
        total_sessions = 0
        r = requests.get(_API_SESSIONS)
        r.raise_for_status()
        sessions = r.json()
        if sessions is not None:
            total_sessions = len(sessions)
        return total_sessions
    except requests.exceptions.RequestException as e:
        print("Unable to contact API {}".format(e))
        return -1
    except ValueError as e:
        print("Unable to process API response {}".format(e))
        return -1


def api_terminals():
    """Collects API terminals details.

    Returns:
        The number of active terminals.
    """
    try:
        total_terminals = 0
        r = requests.get(_API_TERMINALS)
        r.raise_for_status()
        terminals = r.json()
        if terminals is not None:
            total_terminals = len(terminals)
        return total_terminals
    except requests.exceptions.RequestException as e:
        print("Unable to contact API {}".format(e))
        return -1
    except ValueError as e:
        print("Unable to process API response {}".format(e))
        return -1


def get_notebooks_service(shell_command):
    """Obtain JupyterLab status.
    Args:
      shell_command: (str) Parse Jupyter Service status

    Returns:
      A Metric.
    """
    try:
        metric_value = subprocess.run([
            "/bin/bash", "-c",
            shell_command], stdout=subprocess.PIPE, text=True).stdout
        return int(metric_value)
    except ValueError:
        return -1
    except subprocess.CalledProcessError as e:
        print(e)
        return -1


def _get_resource_values():
    """Get Resources Values

    Return:
        A dictionary with Instance values.
    """
    # Get instance information
    data = requests.get('{}zone'.format(_METADATA_SERVER),
                        headers=_METADATA_FLAVOR).text
    instance_id = requests.get(
        '{}id'.format(_METADATA_SERVER), headers=_METADATA_FLAVOR).text
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
    print("Reporting metric: {} Value: {}".format(metric_type, metric_value))
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


def report_metrics(sleep_time, resource_values):
    """Collects metrics

    Args:
      sleep_time:(int) Wait time.
      resource_values:(dict) Dict to pass to Stackdriver.

    Returns:
    """
    while True:
        try:
            report_metric(
                metric_value=api_status()[0],
                metric_type="kernels",
                resource_values=resource_values)
            report_metric(
                metric_value=api_status()[1],
                metric_type="connections",
                resource_values=resource_values)
            report_metric(
                metric_value=api_sessions(),
                metric_type="sessions",
                resource_values=resource_values)
            report_metric(
                metric_value=api_terminals(),
                metric_type="terminals",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(_JUPYTERLAB_MEMORY_CURRENT),
                metric_type="jupyterlab_memory_current",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(_JUPYTERLAB_MEMORY_HIGH),
                metric_type="jupyterlab_memory_high",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(_JUPYTERLAB_MEMORY_MAX),
                metric_type="jupyterlab_memory_max",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(_JUPYTERLAB_STATUS),
                metric_type="jupyterlab_status",
                resource_values=resource_values)
            report_metric(
                metric_value=get_notebooks_service(_PROXY_AGENT_STATUS),
                metric_type="proxy_agent_status",
                resource_values=resource_values)
        except IndexError as e:
            print("IndexError found reporting metrics {}".format(e))
        except Exception as e:
            print("Exception found reporting metrics {}".format(e))
        time.sleep(sleep_time)


def main(args):
    resource_values = _get_resource_values()
    print("Notebooks Collection Agent starting...")
    report_metrics(args.sleep, resource_values)


if __name__ == '__main__':
    args = get_args()
    main(args)
