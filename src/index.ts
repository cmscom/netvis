// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { IRenderMimeRegistry, IRenderMime } from '@jupyterlab/rendermime';
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
    // JupyterLab 4.x compatible registration
    const rendererFactory: IRenderMime.IRendererFactory = {
      safe: true,
      mimeTypes: [MIME_TYPE],
      createRenderer: (options: IRenderMime.IRendererOptions) => new NetVisRenderer(options),
    };

    try {
      // Try to add factory with default rank
      // JupyterLab 4.x doesn't use rank parameter directly
      rendermime.addFactory(rendererFactory);
      console.log('NetVis MIME renderer registered successfully');
    } catch (error) {
      console.error('Failed to register NetVis MIME renderer:', error);
      // Fallback: try alternative registration if the first attempt fails
      try {
        // @ts-ignore - For backward compatibility
        rendermime.addFactory(rendererFactory, 0);
        console.log('NetVis MIME renderer registered with rank 0');
      } catch (fallbackError) {
        console.error('Fallback registration also failed:', fallbackError);
      }
    }
  },
};

export default mimeExtension;
