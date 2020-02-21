"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const apputils_1 = require("@jupyterlab/apputils");
const widgets_1 = require("@phosphor/widgets");
const filebrowser_1 = require("@jupyterlab/filebrowser");
const mainmenu_1 = require("@jupyterlab/mainmenu");
require("../style/index.css");
/**
 * An xckd comic viewer.
 */
class XkcdWidget extends widgets_1.Widget {
    /**
     * Construct a new xkcd widget.
     */
    constructor() {
        super();
        this.id = 'xkcd-jupyterlab';
        this.title.label = 'xkcd.com';
        this.title.closable = true;
        this.addClass('jp-xkcdWidget');
        this.img = document.createElement('img');
        this.img.className = 'jp-xkcdCartoon';
        this.node.appendChild(this.img);
        this.img.insertAdjacentHTML('afterend', `<div class="jp-xkcdAttribution">
        <a href="https://creativecommons.org/licenses/by-nc/2.5/" class="jp-xkcdAttribution" target="_blank">
          <img src="https://licensebuttons.net/l/by-nc/2.5/80x15.png" />
        </a>
      </div>`);
    }
    /**
     * Handle update requests for the widget.
     */
    onUpdateRequest(msg) {
        fetch('https://egszlpbmle.execute-api.us-east-1.amazonaws.com/prod').then(response => {
            return response.json();
        }).then(data => {
            this.img.src = data.img;
            this.img.alt = data.title;
            this.img.title = data.alt;
        });
    }
}
;
/**
 * Activate the xckd widget extension.
 */
function activate(app, palette, files, mainMenu) {
    console.log('JupyterLab extension jupyterlab_xkcd is activated!');
    // Create a single widget
    let widget = new XkcdWidget();
    // Add an application command
    const command = 'xkcd:open';
    app.commands.addCommand(command, {
        label: 'Random xkcd comic',
        execute: () => {
            let it = files.defaultBrowser.model.items();
            let i = it.next();
            while (i != null) {
                console.log(i);
                i = it.next();
            }
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.addToMainArea(widget);
            }
            // Refresh the comic in the widget
            widget.update();
            // Activate the widget
            app.shell.activateById(widget.id);
        }
    });
    // Add an application command
    const overnightCommand = 'gcloud:overnight';
    app.commands.addCommand(overnightCommand, {
        label: 'Run notebook overnight',
        execute: () => {
            let it = files.defaultBrowser.model.items();
            let i = it.next();
            let found = false;
            while (i != null) {
                if (i.name == 'jobs') {
                    found = true;
                }
                i = it.next();
            }
            let currentWidget = app.shell.currentWidget;
            if (!found) {
                files.defaultBrowser.model.manager.newUntitled({ path: '', type: 'directory' }).then(model => {
                    files.defaultBrowser.model.manager.rename('Untitled Folder', 'jobs');
                });
            }
            if (currentWidget) {
                files.defaultBrowser.model.manager.copy(currentWidget.context.session.path, 'jobs');
                console.log(currentWidget.context.session.path);
            }
            else {
                console.log('Null widget');
            }
        }
    });
    const runOvernightGroup = [
        overnightCommand,
    ].map(command => {
        return { command };
    });
    mainMenu.runMenu.addGroup(runOvernightGroup);
    // Add the command to the palette.
    palette.addItem({ command, category: 'Tutorial' });
}
;
/**
 * Initialization data for the jlab_xkcd extension.
 */
const extension = {
    id: 'jlab_xkcd',
    autoStart: true,
    requires: [apputils_1.ICommandPalette, filebrowser_1.IFileBrowserFactory, mainmenu_1.IMainMenu],
    activate: activate,
};
exports.default = extension;
