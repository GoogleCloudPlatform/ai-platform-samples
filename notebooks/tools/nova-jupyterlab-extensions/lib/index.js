"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const coreutils_1 = require("@jupyterlab/coreutils");
const widgets_1 = require("@phosphor/widgets");
const apputils_1 = require("@jupyterlab/apputils");
const disposable_1 = require("@phosphor/disposable");
const application_1 = require("@jupyterlab/application");
const apputils_2 = require("@jupyterlab/apputils");
const coreutils_2 = require("@jupyterlab/coreutils");
const services_1 = require("@jupyterlab/services");
const jobs_1 = require("./jobs");
/**
 * The plugin registration information.
 */
const buttonPlugin = {
    activate: activateButton,
    id: 'nova:button',
    autoStart: true,
};
const jobsPlugin = {
    activate: activateJobs,
    id: 'nova:jobs',
    autoStart: true,
    requires: [application_1.ILayoutRestorer],
};
const typestyle_1 = require("typestyle");
exports.iconStyle = typestyle_1.style({
    backgroundImage: 'var(--jp-nova-icon-train)',
    backgroundRepeat: 'no-repeat',
    backgroundSize: '16px'
});
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
class ButtonExtension {
    /**
     * Create a new extension object.
     */
    createNew(panel, context) {
        let callback = () => {
            let notebook_path = panel.context.contentsModel.path;
            let notebook_path_array = notebook_path.split("/");
            let notebook = notebook_path_array[notebook_path_array.length - 1];
            let path_to_folder = coreutils_2.PageConfig.getOption('serverRoot') + "/" + notebook_path;
            path_to_folder = path_to_folder.substring(0, path_to_folder.length - notebook.length);
            let setting = services_1.ServerConnection.makeSettings();
            let fullUrl = coreutils_1.URLExt.join(setting.baseUrl, "nova");
            const dialog = new apputils_1.Dialog({
                title: 'Submit notebook',
                body: new SubmitJobForm(),
                focusNodeSelector: 'input',
                buttons: [
                    apputils_1.Dialog.cancelButton(),
                    apputils_1.Dialog.okButton({ label: 'SUBMIT' })
                ]
            });
            const result = dialog.launch();
            result.then(result => {
                if (typeof result.value != 'undefined' && result.value) {
                    let fullRequest = {
                        method: 'POST',
                        body: JSON.stringify({
                            "home_dir": coreutils_2.PageConfig.getOption('serverRoot'),
                            "dir": path_to_folder,
                            "notebook": notebook,
                            "gpu_count": result.value["gpu_count"],
                            "gpu_type": result.value["gpu_type"],
                            "instance_type": result.value["instance_type"],
                            "local": result.value["local"]
                        })
                    };
                    services_1.ServerConnection.makeRequest(fullUrl, fullRequest, setting);
                    console.log(result.value);
                }
                dialog.dispose();
            });
        };
        let button = new apputils_2.ToolbarButton({
            className: 'backgroundTraining',
            iconClassName: exports.iconStyle + ' jp-Icon jp-Icon-16 jp-ToolbarButtonComponent-icon',
            onClick: callback,
            tooltip: 'Submit for background training.'
        });
        panel.toolbar.insertItem(0, 'trainOnBackground', button);
        return new disposable_1.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
exports.ButtonExtension = ButtonExtension;
function activateButton(app) {
    console.log('JupyterLab nova button extension is activated!');
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}
/**
 * Activate the extension.
 */
function activateJobs(app, restorer) {
    console.log('JupyterLab nova jobs extension is activated!');
    let sidePanel = new jobs_1.JobsWidget();
    sidePanel.id = 'jp-nova-jobs';
    sidePanel.title.iconClass = 'jp-FolderIcon jp-SideBar-tabIcon';
    sidePanel.title.caption = 'Background Jobs';
    if (restorer) {
        restorer.add(sidePanel, 'background-jobs');
    }
    app.shell.addToLeftArea(sidePanel, { rank: 453 });
}
;
class SubmitJobForm extends widgets_1.Widget {
    /**
     * Create a redirect form.
     */
    constructor() {
        super({ node: SubmitJobForm.createFormNode() });
    }
    static createFormNode() {
        const node = document.createElement('div');
        const text = document.createElement('span');
        const instanceTypeInput = document.createElement('input');
        const gpuTypeInput = document.createElement('input');
        const gpuCountInput = document.createElement('input');
        const instanceTypeLabel = document.createElement('span');
        const gpuTypeLabel = document.createElement('span');
        const gpuCountLabel = document.createElement('span');
        const trainingTypeLabel = document.createElement('span');
        gpuTypeLabel.textContent = 'Enter GPU type';
        gpuCountLabel.textContent = 'Select GPU count';
        instanceTypeLabel.textContent = 'Select instance type';
        trainingTypeLabel.textContent = 'Select training target';
        gpuTypeInput.placeholder = "t4";
        gpuTypeInput.setAttribute("id", "gpuTypeInput");
        instanceTypeInput.placeholder = "n1-standard-8";
        instanceTypeInput.setAttribute("id", "instanceTypeInput");
        gpuCountInput.placeholder = "0";
        gpuCountInput.setAttribute("id", "gpuCountInput");
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
            let instance_types_per_gpu_type_per_count = {
                "k80": {
                    "1": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8"
                    ],
                    "2": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16"
                    ],
                    "4": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32"
                    ],
                    "8": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32",
                        "n1-standard-64"
                    ]
                },
                "p4": {
                    "1": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16"
                    ],
                    "2": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32"
                    ],
                    "4": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32",
                        "n1-standard-64",
                        "n1-standard-96"
                    ]
                },
                "t4": {
                    "1": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16"
                    ],
                    "2": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32"
                    ],
                    "4": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32",
                        "n1-standard-64",
                        "n1-standard-96"
                    ]
                },
                "p100": {
                    "1": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16"
                    ],
                    "2": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32"
                    ],
                    "4": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32",
                        "n1-standard-64"
                    ]
                },
                "v100": {
                    "1": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8"
                    ],
                    "2": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16"
                    ],
                    "4": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32"
                    ],
                    "8": [
                        "n1-standard-1",
                        "n1-standard-2",
                        "n1-standard-4",
                        "n1-standard-8",
                        "n1-standard-16",
                        "n1-standard-32",
                        "n1-standard-64",
                        "n1-standard-96"
                    ]
                }
            };
            let gpu_type_to_counts = {
                "k80": ["1", "2", "4", "8"],
                "p4": ["1", "2", "4"],
                "t4": ["1", "2", "4"],
                "p100": ["1", "2", "4"],
                "v100": ["1", "2", "4", "8"]
            };
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
        ];
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
            }
            else {
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
        let setting = services_1.ServerConnection.makeSettings();
        let fullUrl = coreutils_1.URLExt.join(setting.baseUrl, "nova");
        let fullRequest = {
            method: 'GET'
        };
        services_1.ServerConnection.makeRequest(fullUrl, fullRequest, setting).then(response => {
            response.text().then(function processText(region) {
                console.info("\"" + region + "\"");
                let gpu_type_per_region = {
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
    getValue() {
        return {
            "gpu_type": this.node.querySelector('#gpuTypeInput').value,
            "gpu_count": +this.node.querySelector('#gpuCountInput').value,
            "instance_type": this.node.querySelector('#instanceTypeInput').value,
            "local": this.node.querySelector('#trainingTypeInput').value == "local"
        };
    }
}
/**
 * Export the plugin as default.
 */
exports.default = [buttonPlugin, jobsPlugin];
