// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import * as widgetExports from './widget';

import { NetVisRenderer, MIME_TYPE } from './renderer';

import { MODULE_NAME, MODULE_VERSION } from './version';

const EXTENSION_ID = 'net_vis:plugin';

/**
 * The NetVis MIME renderer extension.
 *
 * This plugin registers both the MIME renderer (for _repr_mimebundle_)
 * and the widget extension (for backward compatibility with ipywidgets).
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  autoStart: true,
  requires: [IRenderMimeRegistry],
  optional: [IJupyterWidgetRegistry],
  activate: activateNetVisExtension,
};

export default plugin;

/**
 * Activate the NetVis extension.
 *
 * This function registers the MIME renderer and optionally the widget extension.
 */
function activateNetVisExtension(
  app: JupyterFrontEnd,
  rendermime: IRenderMimeRegistry,
  widgetRegistry: IJupyterWidgetRegistry | null,
): void {
  // Register MIME renderer for _repr_mimebundle_
  rendermime.addFactory(
    {
      safe: true,
      mimeTypes: [MIME_TYPE],
      createRenderer: (options) => new NetVisRenderer(options),
    },
    0, // rank: 0 means highest priority
  );

  console.log('NetVis MIME renderer registered');

  // Register widget extension for backward compatibility (optional)
  if (widgetRegistry) {
    widgetRegistry.registerWidget({
      name: MODULE_NAME,
      version: MODULE_VERSION,
      exports: widgetExports,
    });
    console.log('NetVis widget extension registered');
  }
}
