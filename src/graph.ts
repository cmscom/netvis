import * as d3 from 'd3';
import { SimulationNodeDatum, SimulationLinkDatum } from 'd3';

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
    .attr('r', 5)
    .attr('fill', 'red');

  simulation.on('tick', () => {
    link
      .attr('x1', (d: any) => (d.source as Node).x)
      .attr('y1', (d: any) => (d.source as Node).y)
      .attr('x2', (d: any) => (d.target as Node).x)
      .attr('y2', (d: any) => (d.target as Node).y);

    node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);
  });
  return svg.node();
}

export default Graph;
