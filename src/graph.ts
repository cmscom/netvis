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

function Graph(svg: any, { nodes, links }: { nodes: Node[]; links: Link[] }) {
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      'link',
      d3.forceLink(links).id((d: any) => (d as Node).id),
    )
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(400, 400));

  const link = svg
    .selectAll('line')
    .data(links)
    .enter()
    .append('line')
    .attr('stroke', 'black');

  const node = svg
    .selectAll('circle')
    .data(nodes)
    .enter()
    .append('circle')
    .attr(
      'r',
      (d: any) =>
        (d.size / Settings.DEFAULT_NODE_SIZE > Settings.DEFAULT_NODE_SIZE
          ? d.size / Settings.DEFAULT_NODE_SIZE
          : Settings.DEFAULT_NODE_SIZE) || Settings.DEFAULT_NODE_SIZE,
    )
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

  simulation.on('tick', () => {
    link
      .attr('x1', (d: any) => (d.source as Node).x)
      .attr('y1', (d: any) => (d.source as Node).y)
      .attr('x2', (d: any) => (d.target as Node).x)
      .attr('y2', (d: any) => (d.target as Node).y);

    node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);
  });

  const width = 800;
  const height = 800;

  // Zoom Event

  // const x = d3.scaleLinear().domain([0, width]).range([0, width]);
  // const y = d3.scaleLinear().domain([0, height]).range([0, height]);

  // const xAxis = d3
  //   .axisBottom(x)
  //   .ticks((width / height) * 10) //
  //   .tickSize(height)
  //   .tickPadding(8 - height);

  // const yAxis = d3
  //   .axisRight(y)
  //   .ticks(10)
  //   .tickSize(width)
  //   .tickPadding(8 - width);

  // const gX = svg.append('g').call(xAxis);
  // const gY = svg.append('g').call(yAxis);

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
    svg.attr('transform', event.transform);
    // gX.call(xAxis.scale(event.transform.rescaleX(x)));
    // gY.call(yAxis.scale(event.transform.rescaleY(y)));
  }

  // Drag Event
  const drag = d3.drag().on('start', dragstart).on('drag', dragged);

  node.call(drag).on('click', click);

  function dragstart() {
    // d3.select(this).classed('fixed', true);
  }

  function dragged(event: any, d: any) {
    d.fx = clamp(event.x, 0, width);
    d.fy = clamp(event.y, 0, height);
    simulation.alpha(1).restart();
  }

  function clamp(x: any, lo: any, hi: any) {
    return x < lo ? lo : x > hi ? hi : x;
  }

  function click(event: any, d: any) {
    delete d.fx;
    delete d.fy;
    // d3.select(this).classed('fixed', false);
    simulation.alpha(1).restart();
  }

  return svg.node();
}

export default Graph;
