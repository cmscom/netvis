// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { Widget } from '@lumino/widgets';

/**
 * MIME type for NetVis graph data
 */
export const MIME_TYPE = 'application/vnd.netvis+json';

/**
 * Frontend package version (should match package.json)
 */
const FRONTEND_VERSION = '0.4.0';

/**
 * Parse graph data string and handle empty data case.
 *
 * @param dataString - JSON string or empty string
 * @returns Parsed graph data with nodes and links arrays
 */
export function parseGraphData(dataString: string): { nodes: any[]; links: any[] } {
  // Handle empty string case - return empty graph
  if (!dataString || dataString.trim() === '') {
    console.log('[NetVis] Empty data received, rendering empty graph');
    return { nodes: [], links: [] };
  }

  try {
    const parsed = JSON.parse(dataString);

    // Validate structure
    if (!parsed || typeof parsed !== 'object') {
      throw new Error('Graph data must be an object');
    }

    if (!Array.isArray(parsed.nodes)) {
      throw new Error('Graph data must have a nodes array');
    }

    if (!Array.isArray(parsed.links)) {
      throw new Error('Graph data must have a links array');
    }

    return parsed;
  } catch (error: any) {
    console.error('[NetVis] Error parsing graph data:', error);
    throw new Error(`Invalid graph data: ${error.message}`);
  }
}

/**
 * Validate version compatibility between frontend and backend.
 * Logs a warning if versions don't match.
 *
 * @param backendVersion - Version string from Python package
 */
export function validateVersion(backendVersion: string | undefined): void {
  if (!backendVersion) {
    console.warn('[NetVis] Warning: Backend version information missing');
    return;
  }

  if (backendVersion !== FRONTEND_VERSION) {
    console.warn(
      `[NetVis] Version mismatch: Frontend v${FRONTEND_VERSION}, Backend v${backendVersion}. ` +
      'This may cause rendering issues. Please ensure both packages are updated to the same version.'
    );
  } else {
    console.log(`[NetVis] Version check passed: v${FRONTEND_VERSION}`);
  }
}

/**
 * A widget for rendering NetVis graphs.
 */
export class NetVisMimeRenderer extends Widget implements IRenderMime.IRenderer {
  private _mimeType: string;

  /**
   * Construct a new NetVis renderer.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this._mimeType = options.mimeType;
    this.addClass('jp-NetVisRenderer');
  }

  /**
   * Render NetVis data into this widget's node.
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    const data = model.data[this._mimeType] as any;

    if (!data) {
      this.node.textContent = 'No data to display';
      return;
    }

    try {
      // Validate version compatibility
      validateVersion(data.version);

      // Parse graph data (handles empty strings)
      const graphData = parseGraphData(data.data || '');

      // Import graph rendering dynamically to avoid circular dependencies
      const { renderGraph } = await import('./graph');

      // Clear any existing content
      this.node.textContent = '';

      // Render the graph (handles empty graphs gracefully)
      renderGraph(this.node, graphData);
    } catch (error: any) {
      console.error('Error rendering NetVis graph:', error);
      this.node.innerHTML = `
        <div style="color: red; padding: 10px; border: 1px solid red; border-radius: 4px;">
          <strong>NetVis Error:</strong><br/>
          ${error.message || 'Unknown error occurred'}
        </div>
      `;
    }
  }
}

/**
 * Extension definition for JupyterLab 4.x
 */
const mimeExtension: JupyterFrontEndPlugin<void> = {
  id: 'net_vis:mime',
  autoStart: true,
  requires: [IRenderMimeRegistry],
  activate: (app: JupyterFrontEnd, rendermime: IRenderMimeRegistry) => {
    console.log('NetVis MIME extension activation started');

    /**
     * Create a renderer factory for NetVis data.
     */
    const factory: IRenderMime.IRendererFactory & { defaultRank?: number } = {
      safe: true,
      mimeTypes: [MIME_TYPE],
      // Explicit default rank to match JupyterLab 4 expectations and avoid
      // `defaultRank` lookups on undefined.
      defaultRank: 0,
      createRenderer: (options: IRenderMime.IRendererOptions) => {
        return new NetVisMimeRenderer(options);
      }
    };

    // Register the factory with fallback paths for JL3/JL4
    try {
      // Preferred path (JL4): factory carries its defaultRank
      rendermime.addFactory(factory);
    } catch (primaryError) {
      console.warn('[NetVis] Primary factory registration failed, retrying with explicit rank', primaryError);
      try {
        // JL3-style explicit rank argument
        rendermime.addFactory(factory, 0);
      } catch (fallbackError) {
        console.error('[NetVis] Failed to register MIME renderer factory', {
          primaryError,
          fallbackError
        });
        return;
      }
    }

    console.log(`NetVis MIME renderer registered for ${MIME_TYPE}`);
  }
};

export default mimeExtension;
