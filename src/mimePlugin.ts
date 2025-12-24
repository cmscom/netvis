import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { Widget } from '@lumino/widgets';
import packageJson from '../package.json';

/**
 * MIME type for NetVis graph data
 */
export const MIME_TYPE = 'application/vnd.netvis+json';

/**
 * Frontend package version (automatically loaded from package.json)
 */
const FRONTEND_VERSION = packageJson.version;

/**
 * Parse graph data string and handle empty data case.
 *
 * @param dataString - JSON string or empty string
 * @returns Parsed graph data with nodes and links arrays
 */
export function parseGraphData(dataString: string): {
  nodes: any[];
  links: any[];
} {
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
        'This may cause rendering issues. Please ensure both packages are updated to the same version.',
    );
  } else {
    console.log(`[NetVis] Version check passed: v${FRONTEND_VERSION}`);
  }
}

/**
 * A widget for rendering NetVis graphs.
 */
export class NetVisMimeRenderer
  extends Widget
  implements IRenderMime.IRenderer
{
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
 * Mime extension definition (JupyterLab expects rendererFactory & rank here).
 */
const rendererFactory: IRenderMime.IRendererFactory & { defaultRank?: number } =
  {
    safe: true,
    mimeTypes: [MIME_TYPE],
    // Explicit default rank to match JupyterLab 4 expectations and avoid
    // `defaultRank` lookups on undefined.
    defaultRank: 0,
    createRenderer: (options: IRenderMime.IRendererOptions) => {
      return new NetVisMimeRenderer(options);
    },
  };

const mimeExtension: IRenderMime.IExtension = {
  id: 'net_vis:mime',
  rendererFactory,
  // Rank used by JupyterLab registry; also keep defaultRank on factory.
  rank: 0,
  dataType: 'json',
};

export default mimeExtension;
