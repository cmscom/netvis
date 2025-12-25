/**
 * HTML Export functionality for download button in JupyterLab.
 *
 * This module provides client-side HTML generation and download capabilities
 * for exporting NetVis graphs as standalone HTML files.
 */

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
  const graphData = config.graphData;

  // Serialize graph data as JSON
  const jsonData = JSON.stringify(graphData);

  // Generate inline CSS
  const css = generateCss();

  // Generate inline JavaScript (D3.js rendering code)
  const js = generateJs();

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
 * Generate JavaScript code for standalone HTML.
 * This is a minimal D3.js-based graph renderer.
 */
function generateJs(): string {
  // For the standalone export, we need to include the D3.js bundle
  // In the actual implementation, this would be loaded from the build
  return `
        // NetVis standalone renderer
        var netvis = (function() {
            // Minimal graph rendering (placeholder for full D3.js bundle)
            function renderGraph(container, data) {
                if (!container) return;

                const width = container.clientWidth || 800;
                const height = container.clientHeight || 600;

                // Create SVG
                const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('width', width);
                svg.setAttribute('height', height);
                svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
                container.appendChild(svg);

                // Simple force-directed layout simulation
                const nodes = data.nodes || [];
                const links = data.links || [];

                // Initialize node positions
                nodes.forEach(function(node, i) {
                    node.x = node.x || width / 2 + (Math.random() - 0.5) * 200;
                    node.y = node.y || height / 2 + (Math.random() - 0.5) * 200;
                });

                // Draw links
                const linkGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                linkGroup.setAttribute('class', 'netvis-links');
                svg.appendChild(linkGroup);

                links.forEach(function(link) {
                    const source = nodes.find(function(n) { return n.id === link.source || n.id === link.source.id; });
                    const target = nodes.find(function(n) { return n.id === link.target || n.id === link.target.id; });
                    if (source && target) {
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        line.setAttribute('class', 'netvis-link');
                        line.setAttribute('x1', source.x);
                        line.setAttribute('y1', source.y);
                        line.setAttribute('x2', target.x);
                        line.setAttribute('y2', target.y);
                        line.setAttribute('stroke', '#999');
                        line.setAttribute('stroke-opacity', '0.6');
                        linkGroup.appendChild(line);
                    }
                });

                // Draw nodes
                const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                nodeGroup.setAttribute('class', 'netvis-nodes');
                svg.appendChild(nodeGroup);

                nodes.forEach(function(node) {
                    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    g.setAttribute('class', 'netvis-node');
                    g.setAttribute('transform', 'translate(' + node.x + ',' + node.y + ')');

                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('r', 8);
                    circle.setAttribute('fill', node.color || '#69b3a2');
                    circle.setAttribute('stroke', '#fff');
                    circle.setAttribute('stroke-width', '1.5');
                    g.appendChild(circle);

                    if (node.name || node.label) {
                        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                        text.setAttribute('class', 'netvis-node-label');
                        text.setAttribute('dx', '12');
                        text.setAttribute('dy', '4');
                        text.textContent = node.name || node.label;
                        g.appendChild(text);
                    }

                    nodeGroup.appendChild(g);
                });
            }

            return {
                renderGraph: renderGraph
            };
        })();
  `;
}
