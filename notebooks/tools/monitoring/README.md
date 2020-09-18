# AI Platform Notebooks Monitoring Agent

## Overview

This service monitors AI Platform Notebooks JupyterLab and Proxy Agent in Docker, 
just run the agent on each of your Notebooks instances in GCP. The following metrics are collected:

- Jupyter Number of Kernels
- Jupyter Number of Connections
- Jupyter Number of Sessions
- Jupyter Number of Terminals
- JupyterLab memory utilization. Current, High, Max.
- JupyterLab service status
- Proxy Agent status


### Report metrics

Installs a monitoring agent that monitors the JupyterLab service on the instance.

```bash
git clone https://github.com/GoogleCloudPlatform/ai-platform-samples.git
cd ai-platform-samples/notebooks/tools/monitoring
pip install -r ./requirements.txt
python notebooks_agent.py &
```

### Adding more metrics

If you want to add more metrics, just do the following changes:


1. Edit [notebooks_agent.py](notebooks_agent.py) and add a new method under
   `report_metrics` Example:
   
   ```
   report_metric(
            value=get_metric_value(metrics.get('memory_free')),
            metric_type='memory_free',
            resource_values=resource_values)
   ```

Currently we support the parameters defined
[here](https://jupyter-server.readthedocs.io/_/downloads/en/latest/pdf/)
Feel free to contribute and add more parameters.

# Install service

```
./install.sh
```

# Reload systemd manager configuration

```
systemctl daemon-reload
```

# Enable notebooks_agent service

```
systemctl --no-reload --now enable /lib/systemd/system/notebooks_agent.service
```

### Testing


	1. Open JupyterLab in your instance and open multiple notebooks.
	2. Run some cells in the Notebooks
	3. Open Google Cloud Console > Monitoring > Metrics Explorer > Type notebooks and the new Metrics should be shown.

### Troubleshooting

Problem: Error when running [notebooks_agent.py](notebooks_agent.py)

```
google.api_core.exceptions.InvalidArgument: 400 One or more TimeSeries could not be written: One or more points were written more frequently than the maximum sampling period configured for the metric.
: timeSeries[0]
```

Solution:
Verify a single instance of this process is running in background

```
ps aux | grep "[n]otebooks_agent.py"
```

Problem: Warning when running
[notebooks_agent.py](notebooks_agent.py)

```
/usr/local/src/venv/gogasca/lib/python3.5/site-packages/google/auth/_default.py:66: UserWarning: Your application ha
s authenticated using end user credentials from Google Cloud SDK. We recommend that most server applications use service accounts instead. If your application continues to use end user credentials fro
m Cloud SDK, you might receive a "quota exceeded" or "API not enabled" error. For more information about service accounts, see https://cloud.google.com/docs/authentication/
  warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
```

Solution:
Configure GOOGLE_APPLICATION_CREDENTIALS using a service account.

```
export GOOGLE_APLICATION_CREDENTIALS=/usr/local/src/credentials.json
```

Problem: 404 Error when running
[notebooks_agent.py](notebooks_agent.py)

```
 'Failed to retrieve
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/?recursive=true
```

Solution: Your Compute Engine needs Google API Cloud access. Allow Read 
access in "Access scopes" Compute Engine, Stackdriver Logging and Monitoring.
