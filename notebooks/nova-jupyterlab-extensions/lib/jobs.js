"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const widgets_1 = require("@phosphor/widgets");
require("../style/index.css");
const apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to a jobs widget.
 */
const JOBS_CLASS = 'jp-Jobs';
/**
 * The class name added to a jobs list node.
 */
const JOBS_LIST_CLASS = 'jp-Jobs-list';
/**
 * The class name added to a jobs header node.
 */
const HEADER_CLASS = 'jp-Jobs-header';
/**
 * The class name added to a jobs list header cell.
 */
const HEADER_ITEM_CLASS = 'jp-Jobs-headerItem';
/**
 * The class name added to a header cell text node.
 */
const HEADER_ITEM_TEXT_CLASS = 'jp-Jobs-headerItemText';
/**
 * The class name added to the jobs content node.
 */
const CONTENT_CLASS = 'jp-Jobs-content';
/**
 * The class name added to jobs content item.
 */
// const ITEM_CLASS = 'jp-Jobs-item';
/**
 * The class name added to the job item text cell.
 */
const ITEM_TEXT_CLASS = 'jp-Jobs-itemText';
/**
 * The class name added to the job item status cell.
 */
const ITEM_STATUS_CLASS = 'jp-Jobs-itemStatus';
/**
 * The class name added to the name column header cell.
 */
const NAME_ID_CLASS = 'jp-id-name';
/**
 * The class name added to the status column header cell.
 */
const STATUS_ID_CLASS = 'jp-id-status';
class JobsWidget extends widgets_1.Widget {
    /**
     * Construct a new xkcd widget.
     */
    constructor() {
        super({
            node: JobsWidget.createNode()
        });
        this.addClass(JOBS_CLASS);
        this.populateHeaderNode(apputils_1.DOMUtils.findElement(this.node, HEADER_CLASS));
    }
    static createNode() {
        let node = document.createElement('div');
        let list = document.createElement('div');
        let header = document.createElement('div');
        let content = document.createElement('ul');
        content.className = CONTENT_CLASS;
        header.className = HEADER_CLASS;
        list.className = JOBS_LIST_CLASS;
        list.appendChild(header);
        list.appendChild(content);
        list.tabIndex = 1;
        node.appendChild(list);
        return node;
    }
    /**
     * Create a node for a header item.
     */
    createHeaderItemNode(label) {
        let node = document.createElement('div');
        let text = document.createElement('span');
        node.className = HEADER_ITEM_CLASS;
        text.className = HEADER_ITEM_TEXT_CLASS;
        text.textContent = label;
        node.appendChild(text);
        return node;
    }
    /**
     * Populate and empty header node for a dir listing.
     *
     * @param node - The header node to populate.
     */
    populateHeaderNode(node) {
        let name = this.createHeaderItemNode('Name');
        let status = this.createHeaderItemNode('Status');
        name.classList.add(NAME_ID_CLASS);
        status.classList.add(STATUS_ID_CLASS);
        node.appendChild(name);
        node.appendChild(status);
    }
    /**
     * Create a new item node for a dir listing.
     *
     * @returns A new DOM node to use as a content item.
     */
    static createItemNode() {
        let node = document.createElement('li');
        let text = document.createElement('span');
        let modified = document.createElement('span');
        text.className = ITEM_TEXT_CLASS;
        modified.className = ITEM_STATUS_CLASS;
        node.appendChild(text);
        node.appendChild(modified);
        return node;
    }
    /**
     * Handle update requests for the widget.
     */
    onUpdateRequest(msg) {
    }
}
exports.JobsWidget = JobsWidget;
;
