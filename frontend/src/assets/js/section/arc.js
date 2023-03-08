import * as d3 from 'd3';
import Trie from './dataStructure';
// import {concatInternalOptions} from "echarts/types/src/model/internalComponentCreator";

// TODO 交互事件

export const drawChart = function (nodes, edges) {
  sunburst(nodes, edges);
};

// const breadcrumb = function () {
//   const [breadcrumbWidth, breadcrumbHeight] = [75, 30];
//   const svg = d3
//     .select('#chart')
//     .create('svg')
//     .attr('viewBox', `0 0 ${breadcrumbWidth * 10} ${breadcrumbHeight}`)
//     .style('font', '12px sans-serif')
//     .style('margin', '5px');

//   const g = svg
//     .selectAll('g')
//     .data(icicle.sequence)
//     .join('g')
//     .attr('transform', (d, i) => `translate(${i * breadcrumbWidth}, 0)`);
// };

const sunburst = function (nodes, edges) {
  const [width, height] = [800, 800];
  const root = partition(nodes, width, height);
  const leafObjectArray = [{}, {}];
  root
    .descendants()
    .slice(1)
    .filter((e) => !e.data.children)
    .forEach((e) => {
      leafObjectArray[e.data.isOri ? 1 : 0][e.data.qualifiedName] = e;
    });
  const isOriColor = d3
      .scaleOrdinal()
      .domain([1, 2, 3, 4, 5, 6, 7])
      .range(['#9d0208', '#d00000', '#dc2f02', '#e85d04', '#f48c06', '#faa307', '#FFBA08']),
    isNotOriColor = d3
      .scaleOrdinal()
      .domain([1, 2, 3, 4, 5, 6, 7])
      .range(['#5390D9', '#4EA8DE', '#48BFE3', '#56CFE1', '#64DFDF', '#72EFDD', '#80FFDB']);
  const edgesData = [];
  buildEdges(edges).forEach((e) => {
    const source = leafObjectArray[e.sourceIsOri][e.source];
    const target = leafObjectArray[e.targetIsOri][e.target];
    if (source && target) {
      edgesData.push(
        linker({
          source,
          target,
        }),
      );
    }
  });

  const translate_y = 300;

  const svg = d3
    .select('#chart')
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .style('font', '12px sans-serif');

  const segment = svg
    .append('g')
    .attr('transform', `translate(0, ${translate_y})`)
    .selectAll('rect')
    .data(root.descendants().slice(1))
    .join('rect')
    .attr('fill', (d) => (d.data.isOri ? isOriColor(d.depth) : isNotOriColor(d.depth)))
    .attr('x', (d) => d.x0)
    .attr('y', (d) => d.y0)
    .attr('width', (d) => d.x1 - d.x0)
    .attr('height', (d) => d.y1 - d.y0);
  console.log(segment)

  const arc = svg
    .append('g')
    .attr('transform', `translate(0, ${translate_y})`)
    .selectAll('path')
    .data(edgesData)
    .join('path')
    .attr('fill', 'none')
    .attr('stroke', '#000')
    .attr('class', 'link')
    .attr('d', (d) => d);
  console.log(arc)
};

const partition = function (nodes, width, height) {
  return d3
    .partition()
    .padding(1)
    .size([width, height / 3])(
      d3
        .hierarchy(buildHierarchy(nodes))
        .sum((d) => d.value)
        .sort((a, b) => b.value - a.value),
    );
};

const buildHierarchy = function (nodes) {
  const treeArray = [{
    name: 'isOri',
    children: new Trie(true),
    isOri: true,
  },
    {
      name: 'isNotOri',
      children: new Trie(false),
      isOri: false,
    },
  ];
  const groupby = d3.groups(
    nodes,
    (d) => d.isHonor,
    (d) => d.packageName,
  );
  groupby.forEach((e) => {
    e[1].forEach((d) => {
      treeArray[e[0]].children.insert(d[0]);
    });
  });
  treeArray.forEach((e) => {
    e.children = e.children.result();
  });
  return {
    name: 'root',
    children: treeArray,
  };
};

const buildEdges = function (edges) {
  return Array.from(
    new Set(
      edges.map((e) =>
        JSON.stringify({
          source: e.sourcePackageName,
          target: e.targetPackageName,
          sourceIsOri: e.sourceIsHonor,
          targetIsOri: e.targetIsHonor,
        }),
      ),
    ),
  ).map((e) => JSON.parse(e));
};

const linker = function (d) {
  const x0 = (d.source.x0 + d.source.x1) / 2,
    x1 = (d.target.x0 + d.target.x1) / 2;
  const y = 33.5;
  return `
    M ${x0} ${y}
    A 1 0.95 0 0 ${x1 < x0 ? 0 : 1} ${x1} ${y}`;
};
