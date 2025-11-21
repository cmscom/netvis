import * as d3 from 'd3';
import { SimulationNodeDatum, SimulationLinkDatum } from 'd3';
import { Collors, Settings } from './settings';
import { convertToCategoryKey } from './utils/string';

export interface Node extends SimulationNodeDatum {
  id: string;
  [key: string]: any; // Additional properties can be added
}

export interface Link extends SimulationLinkDatum<Node> {
  source: string | Node;
  target: string | Node;
  [key: string]: any; // Additional properties can be added
}

export interface GraphOptions {
  nodes: Node[];
  links: Link[];
}

export interface GraphData {
  nodes: Node[];
  links: Link[];
}

/**
 * A function that adjusts the link positions between nodes to the edge of the node circle.
 *
 * @param d
 * @returns
 */
function adjustLinkPath(d: any) {
  const dx = d.target.x - d.source.x;
  const dy = d.target.y - d.source.y;
  const distance = Math.sqrt(dx * dx + dy * dy);

  // Get node radius (default to 5 if not specified)
  const sourceRadius = d.source.radius || 5;
  const targetRadius = d.target.radius || 5;

  const offsetXSource = (dx * sourceRadius) / distance;
  const offsetYSource = (dy * sourceRadius) / distance;
  const offsetXTarget = (dx * targetRadius) / distance;
  const offsetYTarget = (dy * targetRadius) / distance;

  const sourceX = d.source.x + offsetXSource;
  const sourceY = d.source.y + offsetYSource;
  const targetX = d.target.x - offsetXTarget;
  const targetY = d.target.y - offsetYTarget;

  return `M${sourceX},${sourceY} L${targetX},${targetY}`;
}

/**
 * Display Graph
 *
 * @param svg
 * @param param1
 * @returns
 */
function Graph(svg: any, { nodes, links }: { nodes: Node[]; links: Link[] }) {
  const markerId = `arrowhead-${Math.random().toString(36).substring(2, 8)}`;

  const g = svg.append('g');

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      'link',
      d3.forceLink(links).id((d: any) => {
        // Safely access id with null check
        const node = d as Node;
        return node && node.id ? String(node.id) : '';
      }),
    )
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(400, 400));

  const marker = svg
    .append('defs')
    .append('marker')
    .attr('id', markerId)
    .attr('viewBox', '0 0 10 10')
    .attr('refX', 10) // Arrow position adjustment (important)
    .attr('refY', 5)
    .attr('markerWidth', 10)
    .attr('markerHeight', 10)
    .attr('orient', 'auto'); // Standard 'auto' works fine
  marker
    .append('path')
    .attr('d', 'M 0 0 L 10 5 L 0 10 z') // Arrow shape
    .attr('fill', 'black'); // For visibility

  const link = g
    .selectAll('path')
    .data(links)
    .enter()
    .append('path')
    .attr('stroke', 'black')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', `url(#${markerId})`) // Reference arrow marker
    .attr('d', adjustLinkPath);

  const node = g
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g') // Add group element
    .classed('node-group', true);

  node
    .append('circle')
    .attr('r', (d: any) => {
      d.radius =
        (d.size / Settings.DEFAULT_NODE_SIZE > Settings.DEFAULT_NODE_SIZE
          ? d.size / Settings.DEFAULT_NODE_SIZE
          : Settings.DEFAULT_NODE_SIZE) || Settings.DEFAULT_NODE_SIZE;
      return d.radius;
    })
    .attr(
      'fill',
      (d: any) =>
        Collors[
          convertToCategoryKey(
            d.category,
            Settings.DEFAULT_COLOR,
          ) as keyof typeof Collors
        ],
    )
    .classed('circle', true);

  // Add text labels (initially hidden)
  node
    .append('text')
    .text((d: any) => (d.name ? d.name : d.id))
    .attr('y', -20) // Display above the node
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('display', 'none');

  // Node click event handling
  node
    .on('mouseover', function (this: SVGGElement, event: any, d: any) {
      console.log('mouseover', d);
      d3.select(this).select('text').style('display', 'block');
    })
    .on('mouseout', function (this: SVGGElement, event: any, d: any) {
      console.log('mouseout', d);
      if (!d3.select(this).classed('clicked')) {
        d3.select(this).select('text').style('display', 'none');
      }
    })
    .on('click', function (this: SVGGElement, event: any, d: any) {
      console.log('click', this, d); // Verify this points to the correct element
      const isClicked = d3.select(this).classed('clicked');
      console.log('isClicked:', isClicked); // Check current state
      d3.select(this).classed('clicked', !isClicked); // Toggle class
      d3.select(this)
        .select('text')
        .style('display', isClicked ? 'none' : 'block'); // Toggle visibility

      // Release drag fixing
      if (isClicked) {
        delete d.fx;
        delete d.fy;
        simulation.alpha(1).restart();
      }
    });

  simulation.on('tick', () => {
    link.attr('d', adjustLinkPath);
    // node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);
    node.attr('transform', (d: any) => `translate(${d.x},${d.y})`); // Move entire group
  });

  const width = 800;
  const height = 800;

  const zoom = d3
    .zoom()
    .scaleExtent([1, 40])
    .translateExtent([
      [-100, -100],
      [width + 90, height + 100],
    ])
    .on('zoom', zoomed);

  svg.call(zoom);

  function zoomed(event: any) {
    g.attr('transform', event.transform);
  }

  // Drag Event
  const drag = d3.drag().on('start', dragstart).on('drag', dragged);

  node.call(drag);

  function dragstart() {
    // Drag start handler (add logic as needed)
  }

  function dragged(event: any, d: any) {
    d.fx = clamp(event.x, 0, width);
    d.fy = clamp(event.y, 0, height);
    simulation.alpha(1).restart();
  }

  function clamp(x: any, lo: any, hi: any) {
    return x < lo ? lo : x > hi ? hi : x;
  }

  return svg.node();
}

/**
 * Render a graph into a container element.
 *
 * This function wraps the existing Graph() function to make it compatible
 * with both the widget and MIME renderer architectures.
 *
 * @param container - HTML element to render the graph into
 * @param data - Graph data with nodes and links
 */
export function renderGraph(container: HTMLElement, data: GraphData): void {
  // Validate data before rendering
  console.log('[NetVis] renderGraph called with data:', data);
  if (!data) {
    console.error('[NetVis] Error: data is null or undefined');
    throw new Error('GraphData is required');
  }
  if (!data.nodes) {
    console.error('[NetVis] Error: data.nodes is missing', data);
    throw new Error('GraphData must have nodes array');
  }
  if (!data.links) {
    console.error('[NetVis] Error: data.links is missing', data);
    throw new Error('GraphData must have links array');
  }
  console.log(
    `[NetVis] Rendering ${data.nodes.length} nodes and ${data.links.length} links`,
  );

  // Validate all nodes have id
  const missingIds = data.nodes.filter((n, i) => {
    if (!n.id) {
      console.error(`[NetVis] Node at index ${i} is missing id:`, n);
      return true;
    }
    return false;
  });
  if (missingIds.length > 0) {
    throw new Error(`${missingIds.length} nodes are missing 'id' field`);
  }

  // Create SVG element
  const svg = d3
    .select(container)
    .append('svg')
    .attr('width', 800)
    .attr('height', 800);

  // Call existing Graph function with the data
  Graph(svg, data);
}

// export default Graph;
