import re, json, copy, uuid, yaml, subprocess

import tornado.gen as gen

from notebook.utils import url_path_join, url_escape
from notebook.base.handlers import APIHandler

__version__ = '0.3.0'



class NovaHandler(APIHandler):

    @gen.coroutine
    def post(self, path=''):
        data = json.loads(self.request.body.decode('utf-8'))
        data = self.get_json_body()
        request_id = str(uuid.uuid1())
        job_data = {}
        job_data["machine_type"] = data["instance_type"]
        if data["local"]:
            job_data["machine_count"] = 0
        else:
            job_data["machine_count"] = 1
        if data["gpu_type"] and data["gpu_type"] != "N/A":
            gpu_type = data["gpu_type"]
            job_data["gpu_type"] = "nvidia-tesla-{}".format(gpu_type)
            gpu_count = data["gpu_count"]
        else:
            gpu_type = "N/A"
            gpu_count = 0
        parameters = data["parameter"].strip().split(",")
        param_string = ""
        for p in parameters:
            lr = p.split("=", 1)
            if len(lr) != 2:
                raise Exception('Parameter format wrong: {}'.format(p))
            param_string += "-p " + lr[0].strip() + " " + lr[1].strip() + " "
        job_data["parameter"] = param_string[:-1]
        job_data["gpu_count"] = gpu_count
        job_data["notebook"] = data["notebook"]
        job_data["dir"] = data["dir"]
        home_dir = data["home_dir"]
        yaml_raw = yaml.dump(job_data, default_flow_style=False)
        f = open(home_dir + "/.jobs/" + request_id + ".yaml", "w")
        f.write(yaml_raw)

    @gen.coroutine
    def get(self, path=''):
        command = """
        INSTANCE_ZONE="/"$(curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google") &&
        echo "${INSTANCE_ZONE##/*/}"
        """
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        return self.finish(output.decode('ascii').replace("\n", ""))

def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyterlab_nova'
    }]

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    base_url = web_app.settings['base_url']
    endpoint = url_path_join(base_url, 'nova')
    handlers = [(endpoint, NovaHandler)]
    web_app.add_handlers('.*$', handlers)
