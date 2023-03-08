import * as d3 from 'd3';
import * as echarts from 'echarts';
import Trie from './dataStructure';

export const drawChart = function (
  componentKey,
  currentKey,
  nodes,
  edges,
  checkboxGroupProps,
  echartsProps,
  selectProps,
  sourceProps,
  switchProps,
  zoomProps,
) {
  sunburst(
    componentKey,
    currentKey,
    nodes,
    edges,
    checkboxGroupProps,
    echartsProps,
    selectProps,
    sourceProps,
    switchProps,
    zoomProps,
  );
};

const isOriColor = d3
  .scaleOrdinal()
  .domain([1, 2, 3, 4, 5, 6, 7])
  .range(['#5390D9', '#4EA8DE', '#48BFE3', '#56CFE1', '#64DFDF', '#72EFDD', '#80FFDB']),
  isNotOriColor = d3
  .scaleOrdinal()
  .domain([1, 2, 3, 4, 5, 6, 7])
  .range(['#9d0208', '#d00000', '#dc2f02', '#e85d04', '#f48c06', '#faa307', '#FFBA08']);

const sunburst = function (
  componentKey,
  currentKey,
  nodes,
  edges,
  checkboxGroupProps,
  echartsProps,
  selectProps,
  sourceProps,
  switchProps,
  zoomProps,
) {
  const colorList = ['#5390d9', '#9d0208'];
  const drawLegend = (() => {
    const svg = d3
      .select('#legend')
      .append('svg')
      .attr('id', 'legendSvg')
      .attr('width', 300)
      .attr('height', 90);
    const gs = svg.append('g');
    gs.append('rect').attr('x', 0).attr('width', 250).attr('height', 90).attr('fill',
    'white');
    // gs.append('text').attr('x', 0).attr('y', 15).text('切面图例表示');
    const handleChange = (colorArray, textArray) => {
      gs.selectAll('g').remove();
      let legendX = 30,
        legendY = 50;
      const marginX = 20,
        circleR = 20;
      for (let e = 0; e < colorArray.length; e++) {
        const g = gs.append('g');
        g.append('circle')
          .attr('cx', legendX)
          .attr('cy', legendY)
          .attr('r', circleR)
          .attr('fill', colorArray[e])
          .attr('stroke', 'black')
          .attr('stroke-width', '1px');
        g.append('text')
          .attr('x', legendX - circleR + 5)
          .attr('y', legendY + circleR + 15)
          .text(textArray[e]);
        legendX += 2 * circleR + marginX;
      }
    };
    return handleChange;
  })();
  drawLegend(colorList, ['原生', '伴生']);
  const map = d3.rollup(
    nodes,
    (v) => [...new Set(v.map((e) => e.File))],
    (d) => d.packageName,
    (d) => d.isHonor,
  );
  const fileMap = d3.groups(
      nodes,
      (d) => d.isHonor,
      (d) => d.File,
  );
  const width = 800;
  const radius = width / 2;
  const root = partition(buildPackageHierarchy(nodes), radius);
  root.each((e) => {
    e.current = {
      x0: e.x0,
      x1: e.x1,
      y0: e.y0,
      y1: e.y1,
    };
    let temp = map.get(e.data.qualifiedName);
    if (temp) {
      temp = temp.get(e.data.isOri ? 0 : 1);
      if (temp) {
        e.data.file = temp.map((d) => {
          d = d.replaceAll('/', '.');
          const regex = new RegExp(
            `.*.(${e.data.qualifiedName}.*).${d.split('.').slice(-1)}`);
          return regex.exec(d)[1];
        });
      }
    }
  });
  const arc = d3
    .arc()
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle(1 / radius)
    .padRadius(radius)
    .innerRadius((d) => Math.sqrt(d.y0))
    .outerRadius((d) => Math.sqrt(d.y1) - 1);
  const chordRadius = Math.sqrt(root.y1);
  const ribbon = d3.ribbonArrow().radius(chordRadius);

  const objectByNameArray = [{}, {}];
  root
    .descendants()
    .slice(1)
    .filter((e) => e.depth >= 2)
    .forEach((e) => (objectByNameArray[e.data.isOri ? 0 : 1][e.data.qualifiedName] = e));
  const [chords, edgesData, fileEdges] = buildEdges(edges, objectByNameArray);
  const data = buildRelations(root, chords);

  const breadCrumb = (() => {
    const [breadcrumbWidth, breadcrumbHeight] = [70, 40];
    const [width, height] = [300, 45];
    const limit = 4;
    const breadCrumbPoints = function (d, i, end) {
      const tipWidth = 5;
      const points = [];
      points.push('0,0');
      points.push(`${breadcrumbWidth},0`);
      if (!end) {
        points.push(`${breadcrumbWidth + tipWidth},${breadcrumbHeight / 2}`);
      }
      points.push(`${breadcrumbWidth},${breadcrumbHeight}`);
      points.push(`0,${breadcrumbHeight}`);
      if (i > 0) {
        // Leftmost breadcrumb; don't include 6th vertex.
        points.push(`${tipWidth},${breadcrumbHeight / 2}`);
      }
      return points.join(' ');
    };
    const svg = d3
      .select('#breadCrumb')
      .append('svg')
      .style('font', '12px sans-serif')
      .attr('viewBox', `0 0 ${width} ${height}`);

    const handleChange = (data, isOri, depth) => {
      const length = data.length - 1;
      svg.attr('viewBox', `0 0 ${width} ${data.length <= limit ? 45 : 90}`);
      svg.selectAll('g').remove();
      const g = svg
        .selectAll('g')
        .data(data)
        .join('g')
        .attr('transform', (d, i) =>
          i < limit ?
          `translate(${i * breadcrumbWidth}, 0)` :
          `translate(${(i % 4) * breadcrumbWidth}, 50)`,
        );

      g.append('polygon')
        .attr('points', (d, i) => breadCrumbPoints(d, i, i === length))
        .attr('fill', (d, i) =>
          isOri ? isOriColor(depth - length + i) : isNotOriColor(depth - length + i),
        )
        .attr('stroke', 'white');

      g.append('text')
        .attr('x', (breadcrumbWidth + 10) / 2)
        .attr('y', breadcrumbHeight / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .text((d) => d);
    };
    return handleChange;
  })();

  const tooltip = d3.select('#chart').append('div').attr('class', 'tooltip');
  const svg = d3
    .select('#chart')
    .append('svg')
    .attr('id', '#sunburst')
    .attr('viewBox', `${-radius} ${-radius} ${width} ${width}`)
    .style('font', '12px sans-serif');
  const g = svg.append('g');
  data.forEach(
    (d) =>
    (d.flag =
      d.x0 > 0.5 * Math.PI && d.x0 < 1.5 * Math.PI && d.x1 > 0.5 * Math.PI && d.x1 < 1.5 * Math
      .PI ?
      true :
      false),
  );
  const buildArcs = function (selection, arcsData) {
    return selection
      .append('g')
      .selectAll('path')
      .data(arcsData)
      .enter()
      .append('path')
      .attr('fill', (d) => (d.data.isOri ? isOriColor(d.depth) : isNotOriColor(d.depth)))
      .attr('d', arc)
      .each(function (d, i) {
        const firstArcSection = /(^.+?)L/;
        let newArc = firstArcSection.exec(d3.select(this).attr('d'))[1];
        newArc = newArc.replace(/,/g, ' ');

        if (d.flag) {
          const startLoc = /M(.*?)A/;
          const middleLoc = /A(.*?)0 [0-1] 1/;
          const endLoc = /0 [0-1] 1 (.*?)$/;
          const newStart = endLoc.exec(newArc)[1];
          const newEnd = startLoc.exec(newArc)[1];
          const middleSec = middleLoc.exec(newArc)[1];
          newArc = 'M' + newStart + 'A' + middleSec + '0 0 0 ' + newEnd;
        }
        g.append('path')
          .attr('class', 'hiddenDonutArcs')
          .attr('id', 'arcs_' + i)
          .attr('d', newArc)
          .style('fill', 'none');
      });
  };
  const arcs = buildArcs(g, data);
  // 绘制文件旭日图
  const drawFile = (data, tempEdges, color, fileNamesFunc) => {
    const [fileNodes, fileEdges] = buildFileData(data, tempEdges);
    fileNodes
      .descendants()
      .slice(1)
      .filter((d) => !d.children)
      .forEach(fileNamesFunc);
    svg.attr('viewBox', [-165, 0, width, width]);
    const defs = svg.append('defs');
    const arrowMarker = defs
      .append('marker')
      .attr('id', 'arrow')
      .attr('markerUnits', 'strokeWidth')
      .attr('markerWidth', '6')
      .attr('markerHeight', '6')
      .attr('viewBox', '0 0 6 6')
      .attr('refX', '3')
      .attr('refY', '3')
      .attr('orient', 'auto');
    const arrow_path = 'M1,1 L5,3 L1,5 L3,3 L1,1';
    arrowMarker.append('path').attr('d', arrow_path).attr('fill', '#000');
    const g = svg.append('g');
    const padding = 15;
    const packData = d3
      .pack()
      .size([width * 0.8, width * 0.8])
      .padding(padding)(fileNodes)
      .descendants()
      .slice(1);
    const packDataObject = {};
    packData.filter((d) => !d.children).forEach((d) => (packDataObject[d.data.id] = d));
    const nodeGroups = g
      .selectAll('.nodeGroup')
      .data(packData)
      .join((group) => {
        const enter = group.append('g').attr('class', 'nodeGroup');
        enter.append('circle').attr('class', 'packCircle');
        enter.append('path').attr('class', 'packLabelPath');
        enter
          .append('text')
          .attr('class', 'packText')
          .append('textPath')
          .attr('class', 'packTextPath');
        return enter;
      })
      .attr('id', (d) => d.data.id);
    nodeGroups
      .selectAll('.packCircle')
      .attr('id', (d) => `circle_${d.data.id}`)
      .attr('cx', (d) => d.x)
      .attr('cy', (d) => d.y)
      .attr('r', (d) => d.r)
      .attr('fill', (d) => (d.children ? 'white' : color(d)))
      .attr('stroke', (d) => (d.depth === 1 ? colorList[d.data.isOri ? 0 : 1] : 'black'))
      .attr('stroke-width', (d) => (d.depth === 1 ? 1 : 0.5));
    const drawPath = (d) =>
      `M${d.x - d.r - 1},${d.y} A${d.r},${d.r} 0 0 1 ${d.x + d.r + 1},${d.y}`;
    nodeGroups
      .selectAll('.packLabelPath')
      .attr('id', (d) => `path_${d.data.id}`)
      .attr('d', drawPath)
      .attr('stroke-width', 0)
      .attr('fill', 'none');
    nodeGroups
      .selectAll('.packTextPath')
      .attr('id', (d) => `text_${d.data.id}`)
      .attr('letter-spacing', -0.5)
      .attr('fill', '#333333')
      .attr('font-size', (d) => (d.depth !== 1 ? (!d.children ? 0 : 10) : 15))
      .attr('startOffset', '50%')
      .style('text-anchor', 'middle')
      .attr('xlink:href', (d) => `#path_${d.data.id}`)
      .text((d) => d.data.name);

    const selectPoints = (src, dest) => {
      const axisObject = {
        x: src.x >= dest.x,
        y: src.y >= dest.y,
      };
      const sources = [{
            x: src.x + (!axisObject.x ? src.r : -src.r),
            y: src.y,
          },
          {
            x: src.x,
            y: src.y + (!axisObject.y ? src.r : -src.r),
          },
        ],
        targets = [{
            x: dest.x + (axisObject.x ? dest.r : -dest.r),
            y: dest.y,
          },
          {
            x: dest.x,
            y: dest.y + (axisObject.y ? dest.r : -dest.r),
          },
        ];
      const result = [];
      sources.forEach((e, index0) => {
        targets.forEach((d, index1) => {
          result.push([index0, index1, Math.sqrt(Math.pow(e.x - d.x, 2) + Math.pow(e
            .y - d.y, 2))]);
        });
      });
      const minArray = d3.min(result, (d, i) => [i, d[2]]);
      return [sources[result[minArray[0]][0]], targets[result[minArray[0]][1]]];
    };
    const drawLine = (data) => {
      const [source, target] = selectPoints(
        packDataObject[data.source],
        packDataObject[data.target],
      );
      const lineGenerator = d3
        .line()
        .x((d) => d[0])
        .y((d) => d[1])
        .curve(d3.curveBundle);
      const cpx1 = source.x + 0.25 * (target.x - source.x);
      const cpx2 = target.x - 0.25 * (target.x - source.x);
      const cpy1 = source.y + 0.75 * (target.y - source.y);
      const cpy2 = target.y - 0.75 * (target.y - source.y);
      const lineArray = [
        [source.x, source.y],
        [cpx1, cpy1],
        [cpx2, cpy2],
        [target.x, target.y],
      ];
      const path = lineGenerator;
      return path(lineArray);
    };
    const linkGroups = g
      .selectAll('.linkGroup')
      .data(fileEdges)
      .join((group) => {
        const enter = group.append('g').attr('class', 'linkGroup');
        enter.append('path').attr('class', 'linkPath');
        return enter;
      });
    linkGroups
      .selectAll('.linkPath')
      .attr('id', (d) => `${d.source}-${d.target}`)
      .attr('d', drawLine)
      .style('fill', 'none')
      .style('stroke', 'red')
      .style('stroke-width', '2')
      .attr('marker-end', 'url(#arrow)');
    const changeBySelect = (fileEdgeValue, fileRelationValue) => {
      nodeGroups
        .filter((d) => !d.children)
        .on('mouseover', (event, v) => {
          const idArray = [];
          fileRelationValue.forEach((e) => {
            fileEdgeValue.forEach((d) => {
              const temp = v.data.relation[e][d];
              if (temp.length) {
                idArray.push(...temp);
              }
            });
          });
          // console.log(idArray);
          nodeGroups
            .filter((d) => !d.children)
            .attr('opacity', 0.1)
            .filter((d) => idArray.indexOf(d.data.id) !== -1 || d.data.id === v.data.id)
            .attr('opacity', 1);
          linkGroups.attr('opacity', 0);
          if (idArray.length) {
            linkGroups
                .filter((d) => d.source === v.data.id || d.target === v.data.id)
                .attr('opacity', 1);
          }
          tooltip.transition().duration(200).style('opacity', 1);
          tooltip
              .html(`${v.data.name}`)
              .style('left', event.pageX + 5 + 'px')
              .style('top', event.pageY - 28 + 'px');
        })
        .on('mouseout', () => {
          nodeGroups.attr('opacity', 1);
          linkGroups.attr('opacity', 1);
          tooltip.transition().duration(500).style('opacity', 0);
        })
        .on('click', (event, v) => {
          let [file, isOri] = v.data.id.split('_');
          file = file.replaceAll('.', '/');
          isOri = parseInt(isOri);
          const fileArray = fileMap.filter((e) => e[0] === isOri)[0][1],
              filePattern = new RegExp(`.*${file}..*`);
          let fileResult = fileArray.filter((e) => filePattern.exec(e[0]))[0][1];
          const tempArray = fileResult.map((e) => e._id);
          let idRelations = tempEdges
              .map((e) => e.idDirection)
              .reduce((a, b) => a.concat(b))
              .map((e) => e.split('->'))
              .filter((e) => e.filter((d) => tempArray.includes(parseInt(d))).length)
              .reduce((a, b) => a.concat(b));
          idRelations = Array.from(new Set(idRelations)).map((d) => parseInt(d));
          idRelations = Array.from(new Set([...tempArray, ...idRelations]));
          const nodeResult = nodes.filter((e) => idRelations.includes(e._id)),
              edgeResult = edges.filter(
                  (e) => idRelations.includes(e.source) && idRelations.includes(e.target),
              );
          echartsProps.echartsNodes = nodeResult;
          echartsProps.echartsEdges = edgeResult;
          componentKey.value = 'echarts';
        });
    };
    const {
      fileEdgeValue,
      fileRelationValue
    } = checkboxGroupProps;
    changeBySelect(fileEdgeValue, fileRelationValue);
    checkboxGroupProps.handleFileEdgeChange = (value) => {
      changeBySelect(value, fileRelationValue);
    };
    checkboxGroupProps.handleFileRelationChange = (value) => {
      changeBySelect(fileEdgeValue, value);
    };
  };
  const handleClick = (event, e) => {
    currentKey = 'file';
    g.attr('display', 'none');
    const temp = fileEdges.filter(
      (d) =>
      (e.data.file.indexOf(d.source) !== -1 && d.sourceIsOri === (e.data.isOri ? 0 : 1)) ||
      (e.data.file.indexOf(d.target) !== -1 && d.targetIsOri === (e.data.isOri ? 0 : 1)),
    );
    const colorList = ['#ff1818', '#ffc300', '#5463ff'];
    const textObject = {
      in_package: '包内',
      out_package: '包外',
      out_organization: '跨组织',
    };
    selectProps.fileTypes = Object.entries(textObject).map((d) => ({
      value: d[0],
      label: d[1],
    }));
    console.log(selectProps.fileTypes);
    selectProps.fileNamesObject = Object.fromEntries(Object.keys(textObject).map((d) => [d,
    []]));
    drawLegend(colorList, Object.values(textObject));
    const color = (d) => {
      if (d.data.isOri === e.data.isOri) {
        if (d.data.qualifiedName.includes(e.data.qualifiedName)) {
          return colorList[0];
        }
        return colorList[1];
      }
      return colorList[2];
    };
    const fileNamesFunc = (d) => {
      const index = (() => {
        if (d.data.isOri === e.data.isOri) {
          if (d.data.qualifiedName.includes(e.data.qualifiedName)) {
            return 0;
          }
          return 1;
        }
        return 2;
      })();
      selectProps.fileNamesObject[Object.entries(textObject)[index][0]].push({
        value: d.data.qualifiedName,
      });
    };
    debugger
    drawFile(e.data, temp, color, fileNamesFunc);
  };
  arcs
    .filter((d) => d.data.file)
    .attr('cursor', 'pointer')
    .on('click', handleClick);
  const ribbons = g
    .append('g')
    .selectAll('path')
    .data(chords)
    .join('path')
    .attr('d', ribbon)
    .style('mix-blend-mode', 'multiply')
    .attr('fill', (d) =>
      d.source.isOri ? isOriColor(d.source.depth) : isNotOriColor(d.source.depth),
    )
    .attr('display', 'none');

  const nameFilter = (d) => {
    const angle = Math.abs(d.x1 - d.x0);
    const r = [Math.sqrt(d.y0) + Math.sqrt(d.y1)] / 2;
    const arcLength = 2 * r * angle;
    const textLength = d.data.name.length * 10.5;
    return textLength < arcLength;
  };

  const texts = g
    .append('g')
    .selectAll('.donutText')
    .data(data)
    .enter()
    .append('text')
    .attr('class', 'donutText')
    .attr('dy', (d) =>
      d.flag ? -[Math.sqrt(d.y1) - Math.sqrt(d.y0)] / 2 : [Math.sqrt(d.y1) - Math.sqrt(d.y0)] / 2,
    )
    .append('textPath')
    .attr('startOffset', '50%')
    .style('text-anchor', 'middle')
    .attr('xlink:href', function (d, i) {
      return '#arcs_' + i;
    })
    .text((d) => (nameFilter(d) ? d.data.name : null));

  edgesData.forEach((e) => {
    sourceProps.sourceObject[e[0]] = e[1]
      .sort((a, b) => a[0] - b[0])
      .map((d) => ({
        value: d[0],
      }));
  });
  sourceProps.sourceData = Object.keys(sourceProps.sourceObject).map((e) => ({
    value: e,
  }));
  const keys = Object.keys(sourceProps.sourceObject);
  sourceProps.source = d3.min(keys);
  sourceProps.target = d3.min(keys);

  const arcFilter1 = (e, d, checkboxValue) => {
    let flag = false;
    for (let v of checkboxValue) {
      const temp = {
        isOri: d.data.isOri,
        qualifiedName: d.data.qualifiedName,
      };
      flag = e.data.relation[v].indexOf(JSON.stringify(temp)) !== -1;
      if (flag) {
        break;
      }
    }
    return flag;
  };

  const arcFilter2 = (e, d, source, target, nodeCheckedValue) => {
    const flag = !nodeCheckedValue ?
      true :
      (e.depth === parseInt(target) && d.depth === parseInt(source)) ||
      (e.depth === parseInt(source) && d.depth === parseInt(target));
    return flag;
  };

  const ribbonFilter = (e, d, checkboxValue) => {
    let flag = false;
    const object = {
      in: ['source', 'target'],
      out: ['target', 'source'],
    };
    for (let v of checkboxValue) {
      const temp = JSON.stringify({
        isOri: d[object[v][0]].isOri,
        qualifiedName: d[object[v][0]].qualifiedName,
      });
      flag =
        e.data.relation[v].indexOf(temp) !== -1 &&
        d[object[v][1]].qualifiedName === e.data.qualifiedName &&
        d[object[v][1]].isOri === e.data.isOri;
      if (flag) {
        break;
      }
    }
    return flag;
  };

  const legendFilter = (e) => {
    if (legnedArray.length) {
      for (let d of legnedArray) {
        if (e.source.isOri === d[0] && e.target.isOri === d[1]) {
          return true;
        }
      }
      return false;
    }
    return true;
  };

  let legnedArray = [];

  const changeBySelect = function (checkboxValue, sourceProps, switchProps) {
    const {
      source,
      target,
      isChanged
    } = sourceProps;
    const ribbonFunc = () => {
      ribbons
        .attr('display', 'none')
        .filter((d) => d.source.depth === parseInt(source) && d.target.depth === parseInt(
          target))
        .filter(legendFilter)
        .attr('display', 'block')
        .attr('opacity', 1);
    };
    const nodesFunc = function (selection) {
      selection
        .filter((d) => d.depth >= 2)
        .on('mouseover', (event, e) => {
          const mouseOverEvent = function (selection) {
            selection
              .attr('opacity', 0.1)
              .filter(
                (d) =>
                (arcFilter1(e, d, checkboxValue) &&
                  arcFilter2(e, d, source, target, switchProps.nodeCheckedValue)) ||
                (d.data.qualifiedName === e.data.qualifiedName && d.data.isOri === e.data
                  .isOri),
              )
              .attr('opacity', '1');
          };
          breadCrumb(e.data.qualifiedName.split('.'), e.data.isOri, e.depth);
          mouseOverEvent(arcs);
          mouseOverEvent(texts);
          ribbons
            .attr('display', 'none')
            .filter(
              (d) => d.source.depth === parseInt(source) && d.target.depth === parseInt(
                target),
            )
            .filter(legendFilter)
            .attr('display', 'block')
            .attr('opacity', 0.1)
            .filter((d) => ribbonFilter(e, d, checkboxValue))
            .attr('opacity', 1);
        })
        .on('mouseout', () => {
          arcs.attr('opacity', 1);
          texts.attr('opacity', 1);
          ribbonFunc();
        });
    };
    if (isChanged) {
      drawCount(
        chords.filter(
          (d) => d.source.depth === parseInt(source) && d.target.depth === parseInt(target),
        ),
        source,
        target,
      );
    }
    ribbonFunc();
    nodesFunc(arcs);
    nodesFunc(texts);
    ribbons
      .on('mouseover', (event, e) => {
        const mouseOverEvent = function (selection) {
          selection
            .attr('opacity', 0.1)
            .filter(
              (d) =>
              (d.data.qualifiedName === e.source.qualifiedName &&
                d.data.isOri === e.source.isOri) ||
              (d.data.qualifiedName === e.target.qualifiedName &&
                d.data.isOri === e.target.isOri),
            )
            .attr('opacity', 1);
        };
        if (e.source.depth === parseInt(source) && e.target.depth === parseInt(target)) {
          mouseOverEvent(arcs);
          mouseOverEvent(texts);
          ribbons
            .attr('display', 'none')
            .filter(
              (d) => d.source.depth === parseInt(source) && d.target.depth === parseInt(
                target),
            )
            .filter(legendFilter)
            .attr('display', 'block')
            .attr('opacity', (d) =>
              JSON.stringify(d.source) === JSON.stringify(e.source) &&
              JSON.stringify(d.target) === JSON.stringify(e.target) ?
              1 :
              0.1,
            );
          tooltip.transition().duration(200).style('opacity', 1);
          tooltip
            .html(
              `${e.source.qualifiedName} -> ${e.target.qualifiedName} <br> value:${e.value}`)
            .style('left', event.pageX + 5 + 'px')
            .style('top', event.pageY - 28 + 'px');
        }
      })
      .on('mouseout', () => {
        arcs.attr('opacity', 1);
        texts.attr('opacity', 1);
        ribbonFunc();
        tooltip.transition().duration(500).style('opacity', 0);
      });
  };

  const drawCount = (data, source, target) => {
    let types = [];
    data.forEach((e) => types.push(...e.value.map((d) => d[0])));
    types = Array.from([...new Set(types)]);
    const yAxisData = types;
    const groupData = d3.rollups(
      data,
      (v) => v.map((x) => x.value.map((d) => d[0])),
      (e) => e.source.isOri,
      (e) => e.target.isOri,
    );
    const groupDataObject = {};
    groupData.forEach((e) => {
      e[1].forEach((d) => {
        const groupbyType = d3.group(
          d[1].reduce((a, b) => a.concat(b)),
          (x) => x,
        );
        const keys = [...groupbyType.keys()];
        groupDataObject[`${e[0] ? '原生' : '伴生'}->${d[0] ? '原生' : '伴生'}`] = yAxisData.map(
          (v) => {
            return keys.indexOf(v) !== -1 ? groupbyType.get(v).length : 0;
          },
        );
      });
    });
    const chartDom = document.getElementById('count');
    let myChart = echarts.getInstanceByDom(chartDom);
    if (myChart == null) {
      myChart = echarts.init(chartDom);
    }
    myChart.hideLoading();
    const option = {
      title: {
        text: '包依赖统计',
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      legend: {
        orient: 'vertical',
        x: 'left',
        y: 'bottom',
      },
      grid: {
        containLabel: true,
      },
      xAxis: {
        type: 'value',
        axisLabel: {
          show: false,
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLine: {
          show: false,
        },
      },
      yAxis: {
        type: 'category',
        data: yAxisData,
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLine: {
          show: false,
        },
        nameTextStyle: {
          fontSize: 4,
        },
      },
      series: Object.entries(groupDataObject).map((d) => ({
        name: d[0],
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'self',
        },
        data: d[1],
      })),
    };
    // 图例控制选取
    myChart.on('legendselectchanged', (params) => {
      const object = {};
      object['原生'] = true;
      object['伴生'] = false;
      const temp = [];
      Object.entries(params.selected).forEach((e) => {
        const sourceIsOri = object[e[0].split('->')[0]];
        const targetIsOri = object[e[0].split('->')[1]];
        if (e[1]) {
          temp.push([sourceIsOri, targetIsOri]);
        }
      });
      legnedArray = temp;
      ribbons.attr('display', 'none');
      if (temp.length) {
        ribbons
          .filter((d) => d.source.depth === parseInt(source) && d.target.depth === parseInt(
            target))
          .filter(legendFilter)
          .attr('display', 'block')
          .attr('opacity', 1);
      }
    });
    option && myChart.setOption(option, true);
  };

  changeBySelect(checkboxGroupProps.checkboxValue, sourceProps, switchProps);
  sourceProps.handleSourceChange = (value) => {
    sourceProps.source = value;
    sourceProps.target = sourceProps.sourceObject[value][0].value;
    sourceProps.isChanged = true;
    changeBySelect(checkboxGroupProps.checkboxValue, sourceProps, switchProps);
  };
  sourceProps.handleTargetChange = (value) => {
    sourceProps.target = value;
    sourceProps.isChanged = true;
    changeBySelect(checkboxGroupProps.checkboxValue, sourceProps, switchProps);
  };
  checkboxGroupProps.handleCheckboxChange = (value) => {
    sourceProps.isChanged = false;
    changeBySelect(value, sourceProps, switchProps);
  };
  switchProps.handleNodeCheckedChange = (value) => {
    sourceProps.isChanged = false;
    switchProps.nodeCheckedValue = value;
    changeBySelect(checkboxGroupProps.checkboxValue, sourceProps, switchProps);
  };
  switchProps.handleEdgeStrokeChange = (value) => {
    ribbons.attr('stroke', value ? '#333333' : 'none');
  };

  const zoomed = function (event, d) {
    console.log(d)
    g.attr('transform', event.transform);
  };

  const zoom = d3
    .zoom()
    .extent([
      [-width / 2, -width / 2],
      [width, width],
    ])
    .scaleExtent([0.3, 1.5])
    .on('zoom', zoomed);
  svg.call(zoom);

  zoomProps.zoomAbled = () => {
    zoomProps.disabled = !zoomProps.disabled;
    svg.call(zoom);
  };
  zoomProps.zoomDisabled = () => {
    zoomProps.disabled = !zoomProps.disabled;
    svg.on('.zoom', null);
  };
  zoomProps.zoomReset = () =>
    svg
    .transition()
    .duration(750)
    .call(zoom.transform, d3.zoomIdentity, d3.zoomTransform(g).invert([width / 2, width / 2]));
};

const partition = function (nodes, radius) {
  const root = d3
    .hierarchy(nodes)
    .sum((d) => d.value)
    .sort((a, b) => b.value - a.value);
  return d3.partition().size([2 * Math.PI, radius * radius])(root);
};

const buildPackageHierarchy = function (nodes) {
  const treeArray = [{
      name: '原生',
      children: new Trie(true),
      isOri: true,
      id: '原生',
    },
    {
      name: '伴生',
      children: new Trie(false),
      isOri: false,
      id: '伴生',
    },
  ];

  const groupby = d3.groups(
    nodes,
    (e) => e.isHonor,
    (e) => e.packageName,
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

const buildFileData = function (data, edges) {
  // 0: true 原生 1: false 伴生
  // TODO 使只有单一一个圆的合二为1
  const treeArray = [{
      name: '原生',
      children: new Trie(true),
      isOri: true,
      id: '原生',
    },
    {
      name: '伴生',
      children: new Trie(false),
      isOri: false,
      id: '伴生',
    },
  ];
  const tempArray = Array.from(
    new Set([
      ...edges.map((d) =>
        JSON.stringify({
          name: d.source,
          isOri: d.sourceIsOri,
        }),
      ),
      ...edges.map((d) =>
        JSON.stringify({
          name: d.target,
          isOri: d.targetIsOri,
        }),
      ),
    ]),
  ).map((d) => JSON.parse(d));
  tempArray.forEach((d) => {
    treeArray[d.isOri].children.insert(d.name);
  });
  treeArray.forEach((d) => {
    d.children = d.children.fileResult();
  });
  const hierarchyData = d3
    .hierarchy({
      name: 'root',
      children: treeArray,
    })
    .sum((d) => d.value)
    .sort((a, b) => b.value - a.value);
  const filterFunc = (key, d, e) => {
    return d[key] === e.data.qualifiedName && d[`${key}IsOri`] === (e.data.isOri ? 0 : 1);
  };
  hierarchyData.each((e) => {
    if (!e.children) {
      const relation = {
        in_package: {},
        out_package: {},
        out_organization: {},
      };
      const object = {
        in: ['target', 'source'],
        out: ['source', 'target'],
      };
      Object.keys(object).forEach((v) => {
        const temp = edges.filter((d) => filterFunc(object[v][0], d, e));
        const relationFunc = function (key, func) {
          relation[key][v] = [
            ...temp.filter(func).map((d) =>
              `${d[object[v][1]]}_${d[`${object[v][1]}IsOri`]}`),
          ];
        };
        const relationFilter = (d, flags) => {
          const [flag0, flag1, flag2] = flags;
          if (d[`${object[v][1]}IsOri`] === e.data.isOri) {
            if (
              d[`${object[v][1]}`].split('.').slice(0, -1) ===
              e.data.qualifiedName().split('.').slice(0, -1)
            ) {
              return flag0;
            }
            return flag1;
          }
          return flag2;
        };
        Object.keys(relation).forEach((value, index) => {
          const flags = Array(Object.keys(relation).length).fill(false);
          flags[index] = true;
          relationFunc(value, (d) => relationFilter(d, flags));
        });
      });
      e.data.relation = relation;
    }
  });
  const links = edges.map((d) => ({
    source: `${d.source}_${d.sourceIsOri}`,
    target: `${d.target}_${d.targetIsOri}`,
    value: d.value,
  }));
  return [hierarchyData, links];
};

const buildEdges = function (edges, objectByNameArray) {
  const nestPackageEdges = d3.rollups(
      edges,
      (v) => {
        const value = d3.rollups(
          v,
          (f) => f.length,
          (e) => e.value,
        );
        v.forEach((x) => {
          x.packageValue = value;
        });
        return v;
      },
      (d) => d.sourceIsHonor,
      (d) => d.sourcePackageName,
      (d) => d.targetIsHonor,
      (d) => d.targetPackageName,
    ),
    nestFileEdges = d3.rollups(
      edges,
      (v) => {
        const value = d3.rollups(
          v,
          (f) => f.length,
          (e) => e.value,
        );
        v.forEach((x) => {
          const typeArray = ['source', 'target'];
          typeArray.forEach((type) => {
            x[`${type}File`] = new RegExp(
              `.*.(${x[`${type}PackageName`]}.*).${x[`${type}File`].split('.').slice(-1)}`,
            ).exec(x[`${type}File`].replaceAll('/', '.'))[1];
          });
          x.fileValue = value;
        });
        return v;
      },
      (d) => d.sourceIsHonor,
      (d) => d.sourceFile,
      (d) => d.targetIsHonor,
      (d) => d.targetFile,
    );
  let newFileEdges = [],
    newPackageEdges = [];
  const convert = function (array, store, type) {
    array.forEach((e) => {
      if (Array.isArray(e[1])) {
        convert(e[1], store, type);
      } else {
        store.push({
          source: e[`source${type}`],
          target: e[`target${type}`],
          sourceIsOri: e.sourceIsHonor,
          targetIsOri: e.targetIsHonor,
          value: e[`${type === 'File' ? 'file' : 'package'}Value`],
        });
      }
    });
  };
  convert(nestFileEdges, newFileEdges, 'File');
  convert(nestPackageEdges, newPackageEdges, 'PackageName');
  newFileEdges = Array.from(new Set(newFileEdges.map((e) => JSON.stringify(e)))).map((e) =>
    JSON.parse(e),
  );
  newPackageEdges = Array.from(new Set(newPackageEdges.map((e) => JSON.stringify(e)))).map((e) =>
    JSON.parse(e),
  );
  const edgesPackageData = [];
  newPackageEdges.forEach((e) => {
    const source = objectByNameArray[e.sourceIsOri][e.source];
    const target = objectByNameArray[e.targetIsOri][e.target];
    if (source && target) {
      edgesPackageData.push({
        source: {
          qualifiedName: source.data.qualifiedName,
          startAngle: source.x0,
          endAngle: source.x1,
          depth: source.depth,
          isOri: source.data.isOri,
        },
        target: {
          qualifiedName: target.data.qualifiedName,
          startAngle: target.x0,
          endAngle: target.x1,
          depth: target.depth,
          isOri: target.data.isOri,
        },
        value: e.value,
      });
    }
  });
  const nestPackageEdgesByDepth = d3.groups(
    edgesPackageData,
    (d) => d.source.depth,
    (d) => d.target.depth,
  );
  return [edgesPackageData, nestPackageEdgesByDepth, newFileEdges];
};

const buildRelations = function (nodes, edges) {
  const filterFunc = (key, d, e) => {
    return d[key].qualifiedName === e.data.qualifiedName && d[key].isOri === e.data.isOri;
  };
  const nodesData = nodes.descendants().slice(1);
  nodesData.forEach((e) => {
    if (e.depth >= 2) {
      const relation = {
        in: [],
        out: [],
      };
      const object = {
        in: ['target', 'source'],
        out: ['source', 'target'],
      };
      Object.keys(object).forEach((v) => {
        relation[v] = edges
          .filter((d) => filterFunc(object[v][0], d, e))
          .map((d) =>
            JSON.stringify({
              isOri: d[object[v][1]].isOri,
              qualifiedName: d[object[v][1]].qualifiedName,
            }),
          );
      });
      e.data.relation = relation;
    }
  });
  return nodesData;
};
