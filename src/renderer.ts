import { Widget } from '@lumino/widgets';
import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { renderGraph } from './graph';
import { GraphData } from './graph';

/**
 * MIME type for NetVis graph data
 */
export const MIME_TYPE = 'application/vnd.netvis+json';

/**
 * NetVis MIME renderer for JupyterLab
 *
 * This renderer handles the custom MIME type 'application/vnd.netvis+json'
 * and renders network graphs as interactive D3.js visualizations.
 */
export class NetVisRenderer extends Widget implements IRenderMime.IRenderer {
  private _mimeType: string;

  /**
   * Construct a new NetVisRenderer.
   *
   * @param options - Renderer options provided by JupyterLab
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this._mimeType = options.mimeType;
    this.addClass('jp-NetVisRenderer');
  }

  /**
   * Render the MIME model into this widget's node.
   *
   * @param model - The MIME model to render
   * @returns A promise that resolves when rendering is complete
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    try {
      // Extract data from MIME bundle
      const data = model.data[this._mimeType] as any;

      if (!data || !data.data) {
        throw new Error('Invalid MIME bundle: missing data field');
      }

      // Parse JSON string to GraphData
      const graphData: GraphData = JSON.parse(data.data);

      // Validate required fields
      if (!graphData.nodes || !graphData.links) {
        throw new Error('Invalid graph data: missing nodes or links');
      }

      // Validate nodes have id field
      if (graphData.nodes.length > 0 && !graphData.nodes[0].id) {
        throw new Error('Invalid graph data: nodes must have "id" field');
      }

      // Clear any existing content
      this.node.textContent = '';

      // Render the graph
      renderGraph(this.node, graphData);
    } catch (error: any) {
      // Display error message to user
      this.node.innerHTML = `
        <div style="color: red; padding: 10px; border: 1px solid red; border-radius: 4px;">
          <strong>NetVis Error:</strong><br/>
          ${error.message || 'Unknown error occurred'}
        </div>
      `;
      throw error;
    }
  }
}
