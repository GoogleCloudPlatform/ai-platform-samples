import { Widget } from '@phosphor/widgets';
import '../style/index.css';
import { Message } from '@phosphor/messaging';
export declare class JobsWidget extends Widget {
    /**
     * Construct a new xkcd widget.
     */
    constructor();
    static createNode(): HTMLElement;
    /**
     * Create a node for a header item.
     */
    createHeaderItemNode(label: string): HTMLElement;
    /**
     * Populate and empty header node for a dir listing.
     *
     * @param node - The header node to populate.
     */
    populateHeaderNode(node: HTMLElement): void;
    /**
     * Create a new item node for a dir listing.
     *
     * @returns A new DOM node to use as a content item.
     */
    static createItemNode(): HTMLElement;
    /**
     * Handle update requests for the widget.
     */
    onUpdateRequest(msg: Message): void;
}
