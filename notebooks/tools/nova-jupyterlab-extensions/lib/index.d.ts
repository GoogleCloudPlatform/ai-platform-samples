import { IDisposable } from '@phosphor/disposable';
import { JupyterLab } from '@jupyterlab/application';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';
export declare const iconStyle: string;
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export declare class ButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
    /**
     * Create a new extension object.
     */
    createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable;
}
declare const _default: import("@phosphor/application").IPlugin<JupyterLab, void>[];
/**
 * Export the plugin as default.
 */
export default _default;
