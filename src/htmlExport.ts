/**
 * HTML Export functionality for download button in JupyterLab.
 *
 * This module provides client-side HTML generation and download capabilities
 * for exporting NetVis graphs as standalone HTML files.
 */

import { STANDALONE_BUNDLE } from './standaloneBundleContent';

/**
 * Configuration for HTML export.
 */
export interface ExportConfig {
  /** HTML document title */
  title: string;
  /** CSS width value (e.g., "100%", "800px") */
  width: string;
  /** Height in pixels */
  height: number;
  /** Graph data to embed */
  graphData: {
    nodes: any[];
    links: any[];
  };
}

/**
 * Normalize graph data for standalone HTML export.
 *
 * After D3.js simulation runs, link.source and link.target become
 * object references instead of IDs. This function converts them back
 * to IDs so the standalone HTML can create its own simulation.
 *
 * @param graphData - Graph data potentially containing object references
 * @returns Normalized graph data with IDs for source/target
 */
function normalizeGraphData(graphData: { nodes: any[]; links: any[] }): {
  nodes: any[];
  links: any[];
} {
  // Normalize links: convert source/target objects back to IDs
  const normalizedLinks = graphData.links.map((link) => {
    const source =
      typeof link.source === 'object' && link.source !== null
        ? link.source.id
        : link.source;
    const target =
      typeof link.target === 'object' && link.target !== null
        ? link.target.id
        : link.target;

    // Keep other link properties (weight, etc.) but exclude D3 simulation props
    const { index: _index, ...rest } = link;

    return {
      ...rest,
      source,
      target,
    };
  });

  // Normalize nodes: remove D3 simulation properties
  const normalizedNodes = graphData.nodes.map((node) => {
    const {
      x: _x,
      y: _y,
      vx: _vx,
      vy: _vy,
      fx: _fx,
      fy: _fy,
      index: _index,
      ...rest
    } = node;
    return rest;
  });

  return {
    nodes: normalizedNodes,
    links: normalizedLinks,
  };
}

/**
 * Default export configuration values.
 */
export const DEFAULT_EXPORT_CONFIG: Partial<ExportConfig> = {
  title: 'Network Visualization',
  width: '100%',
  height: 600,
};

/**
 * Generate filename for HTML export.
 * Format: netvis_export_YYYY-MM-DD.html
 *
 * @returns Generated filename with current date
 */
export function generateFilename(): string {
  const date = new Date().toISOString().split('T')[0];
  return `netvis_export_${date}.html`;
}

/**
 * Generate standalone HTML document from export configuration.
 *
 * @param config - Export configuration with title, dimensions, and graph data
 * @returns Complete HTML document as string
 */
export function generateStandaloneHtml(config: ExportConfig): string {
  const title = config.title || DEFAULT_EXPORT_CONFIG.title!;
  const width = config.width || DEFAULT_EXPORT_CONFIG.width!;
  const height = config.height || DEFAULT_EXPORT_CONFIG.height!;

  // Normalize graph data to ensure source/target are IDs, not object references
  const graphData = normalizeGraphData(config.graphData);

  // Serialize graph data as JSON
  const jsonData = JSON.stringify(graphData);

  // Generate inline CSS
  const css = generateCss();

  // Get the pre-built JavaScript bundle (D3.js + rendering code)
  const js = getJsBundle();

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${escapeHtml(title)}</title>
    <style>
${css}
    </style>
</head>
<body>
    <div class="netvis-container">
        <div id="netvis-graph" style="width: ${escapeHtml(width)}; height: ${height}px;"></div>
    </div>
    <script>
${js}
    </script>
    <script>
        (function() {
            const graphData = ${jsonData};
            if (typeof netvis !== 'undefined' && netvis.renderGraph) {
                netvis.renderGraph(document.getElementById('netvis-graph'), graphData);
            }
        })();
    </script>
</body>
</html>`;
}

/**
 * Trigger browser download of HTML content.
 *
 * @param htmlContent - HTML document content as string
 * @param filename - Filename for the downloaded file
 */
export function downloadHtml(htmlContent: string, filename: string): void {
  const blob = new Blob([htmlContent], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url); // Prevent memory leak
}

/**
 * Create a download button element for the visualization.
 *
 * @param graphData - Graph data to include in downloaded HTML
 * @returns Button element configured for download
 */
export function createDownloadButton(graphData: {
  nodes: any[];
  links: any[];
}): HTMLButtonElement {
  const button = document.createElement('button');
  button.className = 'netvis-download-btn';
  button.setAttribute('aria-label', 'Download HTML');

  // SVG download icon (no external dependencies)
  button.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
      <polyline points="7 10 12 15 17 10"/>
      <line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
  `;

  // Handle click - generate and download HTML
  button.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();

    const config: ExportConfig = {
      title: 'Network Visualization',
      width: '100%',
      height: 600,
      graphData: graphData,
    };

    const html = generateStandaloneHtml(config);
    const filename = generateFilename();
    downloadHtml(html, filename);
  });

  return button;
}

/**
 * Escape HTML special characters to prevent XSS.
 *
 * @param str - String to escape
 * @returns Escaped string safe for HTML insertion
 */
function escapeHtml(str: string): string {
  const htmlEscapes: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  };
  return str.replace(/[&<>"']/g, (char) => htmlEscapes[char]);
}

/**
 * Generate CSS styles for standalone HTML.
 */
function generateCss(): string {
  return `
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
        }
        .netvis-container {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }
        #netvis-graph {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .netvis-graph svg {
            width: 100%;
            height: 100%;
        }
        .netvis-node circle {
            stroke: #fff;
            stroke-width: 1.5px;
        }
        .netvis-link {
            stroke: #999;
            stroke-opacity: 0.6;
        }
        .netvis-node-label {
            font-size: 12px;
            pointer-events: none;
        }
  `;
}

/**
 * Get JavaScript bundle for standalone HTML.
 *
 * Returns the pre-built D3.js + NetVis rendering code bundle.
 * This is the same bundle used by Python's HTMLExporter.
 */
function getJsBundle(): string {
  return STANDALONE_BUNDLE;
}
