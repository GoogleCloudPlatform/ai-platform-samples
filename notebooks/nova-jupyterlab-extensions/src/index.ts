import { URLExt } from '@jupyterlab/coreutils';

import {
    Widget
} from "@phosphor/widgets";

import {
    Dialog
} from "@jupyterlab/apputils";

import {
  IDisposable, DisposableDelegate
} from '@phosphor/disposable';

import {
  JupyterLab, JupyterLabPlugin, ILayoutRestorer
} from '@jupyterlab/application';

import {
  ToolbarButton
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, INotebookModel
} from '@jupyterlab/notebook';

import {
  PageConfig 
} from '@jupyterlab/coreutils';

import { ServerConnection } from '@jupyterlab/services';

import { JobsWidget } from './jobs';

/**
 * The plugin registration information.
 */
const buttonPlugin: JupyterLabPlugin<void> = {
  activate: activateButton,
  id: 'nova:button',
  autoStart: true,
};

const jobsPlugin: JupyterLabPlugin<void> = {
  activate: activateJobs,
  id: 'nova:jobs',
  autoStart: true,
  requires: [ILayoutRestorer],
};

import { style } from 'typestyle'

export const iconStyle = style({
    backgroundImage: 'var(--jp-nova-icon-train)',
    backgroundRepeat: 'no-repeat',
    backgroundSize: '16px'
})


/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export
class ButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * Create a new extension object.
   */
  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {

    let callback = () => {
      let notebook_path = panel.context.contentsModel.path;
      let notebook_path_array = notebook_path.split("/")
      let notebook = notebook_path_array[notebook_path_array.length - 1]
      let path_to_folder = PageConfig.getOption('serverRoot') + "/" + notebook_path
      path_to_folder = path_to_folder.substring(0, path_to_folder.length - notebook.length);
      let setting = ServerConnection.makeSettings();
      let fullUrl = URLExt.join(setting.baseUrl, "nova");
          
      const dialog = new Dialog({
        title: 'Submit notebook',
        body: new SubmitJobForm(),
        focusNodeSelector: 'input',
        buttons: [
            Dialog.cancelButton(),
            Dialog.okButton({label: 'SUBMIT'})
        ]
      });
      const result = dialog.launch();
      result.then(result => {
        if (typeof result.value != 'undefined' && result.value) {
          let fullRequest = {
            method: 'POST',
            body: JSON.stringify(
              {
                "home_dir": PageConfig.getOption('serverRoot'),
                "dir": path_to_folder,
                "notebook": notebook,
                "gpu_count": result.value["gpu_count"],
                "gpu_type": result.value["gpu_type"],
                "instance_type": result.value["instance_type"],
                "local": result.value["local"],
                "parameter": result.value["parameter"]
              }
            )
          };
          ServerConnection.makeRequest(fullUrl, fullRequest, setting);
          console.log(result.value);
        }
        dialog.dispose();
      });
    };
    let button = new ToolbarButton({
      className: 'backgroundTraining',
      iconClassName: iconStyle + ' jp-Icon jp-Icon-16 jp-ToolbarButtonComponent-icon',
      onClick: callback,
      tooltip: 'Submit for background training.'
    });
    panel.toolbar.insertItem(0, 'trainOnBackground', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

function activateButton(  app: JupyterLab) {
  console.log('JupyterLab nova button extension is activated!');
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}

/**
 * Activate the extension.
 */
function activateJobs(
  app: JupyterLab,
  restorer: ILayoutRestorer
): void {
  console.log('JupyterLab nova jobs extension is activated!');
  let sidePanel = new JobsWidget();

  sidePanel.id = 'jp-nova-jobs'
  sidePanel.title.iconClass = 'jp-FolderIcon jp-SideBar-tabIcon';
  sidePanel.title.caption = 'Background Jobs';

  
  if (restorer) {
    restorer.add(sidePanel, 'background-jobs');
  }

  app.shell.addToLeftArea(sidePanel, {rank: 453} );
};

class SubmitJobForm extends Widget {

    /**
     * Create a redirect form.
     */
    constructor() {
        super({node: SubmitJobForm.createFormNode()});
    }

    private static createFormNode(): HTMLElement {
        const node = document.createElement('div');
        const text = document.createElement('span');
        const instanceTypeInput = document.createElement('input');
        const gpuTypeInput = document.createElement('input');
        const gpuCountInput = document.createElement('input');
        const parameterInput = document.createElement('input');
        const instanceTypeLabel = document.createElement('span');
        const gpuTypeLabel = document.createElement('span');
        const gpuCountLabel = document.createElement('span');
        const trainingTypeLabel = document.createElement('span');
        const parameterLabel = document.createElement('span');

        gpuTypeLabel.textContent = 'Enter GPU type';
        gpuCountLabel.textContent = 'Select GPU count';
        instanceTypeLabel.textContent = 'Select instance type';
        trainingTypeLabel.textContent = 'Select training target';
        parameterLabel.textContent = 'Notebook parameters (optional)'

        gpuTypeInput.placeholder = "t4";
        gpuTypeInput.setAttribute("id", "gpuTypeInput");
        instanceTypeInput.placeholder = "n1-standard-8";
        instanceTypeInput.setAttribute("id", "instanceTypeInput");
        gpuCountInput.placeholder = "0";
        gpuCountInput.setAttribute("id", "gpuCountInput");
        parameterInput.placeholder = "";
        parameterInput.setAttribute("id", "parameterInput");

        var setParameterBox = document.createElement('input');
        setParameterBox.type = 'text';
         setParameterBox.id = "parameterInput";

        var instanceTypes = [
          "n1-standard-1",
          "n1-standard-2",
          "n1-standard-4",
          "n1-standard-8",
          "n1-standard-16",
          "n1-standard-32",
          "n1-standard-64",
          "n1-standard-96"
        ];
        var selectInstanceTypeList = document.createElement("select");
        selectInstanceTypeList.id = "instanceTypeInput";
        for (var i = 0; i < instanceTypes.length; i++) {
          var option = document.createElement("option");
          option.value = instanceTypes[i];
          option.text = instanceTypes[i];
          selectInstanceTypeList.appendChild(option);
        }
        selectInstanceTypeList.value = "n1-standard-4";

        var selectGpuList = document.createElement("select");
        selectGpuList.id = "gpuTypeInput";

        var k80_counts = ["1", "2", "4", "8"];
        var selectGpuCount = document.createElement("select");
        selectGpuCount.id = "gpuCountInput";
        for (var i = 0; i < k80_counts.length; i++) {
          var option = document.createElement("option");
          option.value = k80_counts[i];
          option.text = k80_counts[i];
          selectGpuCount.appendChild(option);
        }

        function update_gpu_count() {

            let instance_types_per_gpu_type_per_count: {[key: string]:  {[key: string]: string[]}} = {
              "k80": {
                "1":  [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8"],
                "2": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16"],
                "4": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32"],
                "8": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32",
                  "n1-standard-64"]},
              "p4": {
                "1": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16"],
                "2": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32"], 
                "4": [
                    "n1-standard-1",
                    "n1-standard-2",
                    "n1-standard-4",
                    "n1-standard-8",
                    "n1-standard-16",
                    "n1-standard-32",
                    "n1-standard-64",
                    "n1-standard-96"]},
              "t4": {
                "1": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16"],
                "2": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32"],
                "4": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32",
                  "n1-standard-64",
                  "n1-standard-96"]
              },
              "p100": {
                "1": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16"],
                "2": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32"], 
                "4": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32",
                  "n1-standard-64"]},
              "v100": {
                "1": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8"],
                "2": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16"],
                "4": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32"], 
                "8": [
                  "n1-standard-1",
                  "n1-standard-2",
                  "n1-standard-4",
                  "n1-standard-8",
                  "n1-standard-16",
                  "n1-standard-32",
                  "n1-standard-64",
                  "n1-standard-96"]}
            }
            let gpu_type_to_counts: {[key: string]: string[]} = {
              "k80": ["1", "2", "4", "8"],
              "p4": ["1", "2", "4"],
              "t4": ["1", "2", "4"],
              "p100": ["1", "2", "4"],
              "v100": ["1", "2", "4", "8"]
            }
            let gpu_type = selectGpuList.value;
            if (gpu_type == "N/A") {
              selectGpuCount.hidden = true;
              gpuCountLabel.hidden = true;
              return;
            }
            selectGpuCount.hidden = false;
            gpuCountLabel.hidden = false;
            let gpu_counts = gpu_type_to_counts[gpu_type];
            while (selectGpuCount.firstChild) {
              selectGpuCount.removeChild(selectGpuCount.firstChild);
            }
            for (var i = 0; i < gpu_counts.length; i++) {
              var option = document.createElement("option");
              option.value = gpu_counts[i];
              option.text = gpu_counts[i];
              selectGpuCount.appendChild(option);
            }
            
            function on_gpu_count_change() {
              var gpu_cout = selectGpuCount.value;
              var instance_types = instance_types_per_gpu_type_per_count[gpu_type][gpu_cout];
              var curren_instance_type = selectInstanceTypeList.value;
              while (selectInstanceTypeList.firstChild) {
                selectInstanceTypeList.removeChild(selectInstanceTypeList.firstChild);
              }
              for (var i = 0; i < instance_types.length; i++) {
                var option = document.createElement("option");
                option.value = instance_types[i];
                option.text = instance_types[i];
                selectInstanceTypeList.appendChild(option);
              }
              if (instance_types.indexOf(curren_instance_type) > -1) {
                selectInstanceTypeList.value = curren_instance_type;
              }
            }
            selectGpuCount.onchange = on_gpu_count_change;
        }
        selectGpuList.onchange = update_gpu_count;

        var trainingTargets = [
          "gce",
          // "local" - local trainig is not yet supported and should be reanabled as soon as it is working.
        ]
        var trainingTypeInput = document.createElement("select");
        trainingTypeInput.id = "trainingTypeInput";
        for (var i = 0; i < trainingTargets.length; i++) {
          var option = document.createElement("option");
          option.value = trainingTargets[i];
          option.text = trainingTargets[i];
          trainingTypeInput.appendChild(option);
        }
        function change_training_type() {
          var trainingType = trainingTypeInput.value;
          if (trainingType == "local") {
            selectGpuCount.hidden = true;
            gpuCountLabel.hidden = true;
            selectGpuList.hidden = true;
            gpuTypeLabel.hidden = true;
            selectInstanceTypeList.hidden = true;
            instanceTypeLabel.hidden = true;
          } else {
            selectGpuList.hidden = false;
            gpuTypeLabel.hidden = false;
            selectInstanceTypeList.hidden = false;
            instanceTypeLabel.hidden = false;
            update_gpu_count();
          }
        }
        trainingTypeInput.onchange = change_training_type;
        selectGpuCount.hidden = true;
        gpuCountLabel.hidden = true;
        selectGpuList.hidden = false;
        gpuTypeLabel.hidden = false;
        selectInstanceTypeList.hidden = false;
        instanceTypeLabel.hidden = false;
        parameterLabel.hidden = false;
        setParameterBox.hidden = false;


        node.className = 'jp-RedirectForm';
        text.textContent = 'Enter configuratio for the background training';

        node.appendChild(trainingTypeLabel);
        node.appendChild(trainingTypeInput);
        node.appendChild(instanceTypeLabel);
        node.appendChild(selectInstanceTypeList);
        node.appendChild(gpuTypeLabel);
        node.appendChild(selectGpuList);
        node.appendChild(gpuCountLabel);
        node.appendChild(selectGpuCount);
        node.appendChild(parameterLabel);
        node.appendChild(setParameterBox);


        let setting = ServerConnection.makeSettings();
        let fullUrl = URLExt.join(setting.baseUrl, "nova");
        let fullRequest = {
          method: 'GET'
        };
        ServerConnection.makeRequest(fullUrl, fullRequest, setting).then(response => {
          response.text().then(function processText(region: string) {
            console.info("\"" + region + "\"");
            let gpu_type_per_region: {[key: string]: string[]} = {
              "asia-east1-a": ["k80"],
              "asia-east1-b": ["k80"],
              "asia-east1-c": ["v100"],
              "asia-northeast1-a": ["t4"],
              "asia-south1-b": ["t4"],
              "asia-southeast1-b": ["t4", "p4"],
              "asia-southeast1-c": ["p4"],
              "australia-southeast1-a": ["p4"],
              "australia-southeast1-b": ["p4"],
              "europe-west1-b": ["k80"],
              "europe-west1-d": ["k80"],
              "europe-west4-a": ["v100"],
              "europe-west4-b": ["t4", "p4", "v100"],
              "europe-west4-c": ["t4", "p4", "v100"],
              "southamerica-east1-c": ["t4"],
              "northamerica-northeast1-a": ["p4"],
              "northamerica-northeast1-b": ["p4"],
              "northamerica-northeast1-c": ["p4"],
              "us-central1-a": ["t4", "p4", "v100", "k80"],
              "us-central1-b": ["t4", "v100"],
              "us-central1-c": ["p4", "k80"],
              "us-central1-f": ["v100"],
              "us-east1-c": ["t4", "k80"],
              "us-east1-d": ["t4", "k80"],
              "us-east4-a": ["p4"],
              "us-east4-b": ["p4"],
              "us-east4-c": ["p4"],
              "us-west1-a": ["t4", "v100", "k80"],
              "us-west1-b": ["t4", "v100", "k80"],
              "us-west2-b": ["p4"],
              "us-west2-c": ["p4"]
            };
            console.info(gpu_type_per_region);
            console.info(gpu_type_per_region[region]);
            var gpus = gpu_type_per_region[region];
            gpus.push("N/A");
            console.info(gpus);
            while (selectGpuList.firstChild) {
              selectGpuList.removeChild(selectGpuList.firstChild);
            }
            for (var i = 0; i < gpus.length; i++) {
              var option = document.createElement("option");
              option.value = gpus[i];
              option.text = gpus[i];
              selectGpuList.appendChild(option);
            }
            selectGpuList.value = "N/A";
          });
        });
        
        return node;
    }

    getValue(): {gpu_type: string, gpu_count: number, instance_type: string, local:boolean, parameter:string} {
      return {
        "gpu_type": (<HTMLInputElement>this.node.querySelector('#gpuTypeInput')).value,
        "gpu_count": +(<HTMLInputElement>this.node.querySelector('#gpuCountInput')).value,
        "instance_type": (<HTMLInputElement>this.node.querySelector('#instanceTypeInput')).value,
        "local": (<HTMLInputElement>this.node.querySelector('#trainingTypeInput')).value == "local",
        "parameter": (<HTMLInputElement>this.node.querySelector('#parameterInput')).value
      };
    }
}


/**
 * Export the plugin as default.
 */
export default [buttonPlugin, jobsPlugin];

