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

  // 各ノードが持つ半径を取得（存在しない場合はデフォルト値を設定）
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
      d3.forceLink(links).id((d: any) => (d as Node).id.toString()),
    )
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(400, 400));

  const marker = svg
    .append('defs')
    .append('marker')
    .attr('id', markerId)
    .attr('viewBox', '0 0 10 10')
    .attr('refX', 10) // 矢印の位置調整（重要）
    .attr('refY', 5)
    .attr('markerWidth', 10)
    .attr('markerHeight', 10)
    .attr('orient', 'auto'); // 通常の 'auto' でもOK
  marker
    .append('path')
    .attr('d', 'M 0 0 L 10 5 L 0 10 z') // 矢印の形
    .attr('fill', 'black'); // 見やすく

  const link = g
    .selectAll('path')
    .data(links)
    .enter()
    .append('path')
    .attr('stroke', 'black')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', `url(#${markerId})`) // 矢印のIDを指定
    .attr('d', adjustLinkPath);

  const node = g
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g') // グループ要素を追加
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

  // テキスト（最初は非表示）を追加
  node
    .append('text')
    .text((d: any) => (d.name ? d.name : d.id))
    .attr('y', -20) // ノードの上に表示
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('display', 'none');

  // ノードのクリックイベントを統合
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
      console.log('click', this, d); // thisが正しい要素を指しているか確認
      const isClicked = d3.select(this).classed('clicked');
      console.log('isClicked:', isClicked); // 現在の状態を確認
      d3.select(this).classed('clicked', !isClicked); // クラスのトグル
      d3.select(this)
        .select('text')
        .style('display', isClicked ? 'none' : 'block'); // 表示状態をトグル

      // ドラッグ解除の処理
      if (isClicked) {
        delete d.fx;
        delete d.fy;
        simulation.alpha(1).restart();
      }
    });

  simulation.on('tick', () => {
    link.attr('d', adjustLinkPath);
    // node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);
    node.attr('transform', (d: any) => `translate(${d.x},${d.y})`); // グループ全体を移動
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
    // ドラッグ開始時の処理（必要に応じて追加）
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

export default Graph;
