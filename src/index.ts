// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { NetVisRenderer, MIME_TYPE } from './renderer';

// Export other modules for backward compatibility
export * from './version';
export * from './widget';

/**
 * The NetVis MIME renderer extension.
 */
const mimeExtension: JupyterFrontEndPlugin<void> = {
  id: 'net_vis:mime',
  autoStart: true,
  requires: [IRenderMimeRegistry],
  activate: (
    app: JupyterFrontEnd,
    rendermime: IRenderMimeRegistry,
  ): void => {
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
  },
};

export default mimeExtension;
