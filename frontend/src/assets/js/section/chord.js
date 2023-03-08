import * as d3 from 'd3';
// TODO 修改事件和nest
let figureData = {};

export const drawLegend = function () {
  const svg = d3
    .select('#legend')
    .append('svg')
    .attr('id', 'legendSvg')
    .attr('width', 300)
    .attr('height', 90);
  const gs = svg.append('g');
  gs.append('rect').attr('x', 0).attr('width', 250).attr('height', 90).attr('fill', 'white');
  // gs.append('text').attr('x', 0).attr('y', 15).text('切面图例表示');
  const colorList = ['rgba(219, 58, 52, 1.0)', 'rgba(23, 126, 137, 1.0)'];
  const textList = ['伴生', '原生'];
  let legendX = 30,
    legendY = 50;
  const marginX = 20,
    circleR = 20;
  for (let e = 0; e < colorList.length; e++) {
    const g = gs.append('g');
    g.append('circle')
      .attr('cx', legendX)
      .attr('cy', legendY)
      .attr('r', circleR)
      .attr('fill', colorList[e])
      .attr('stroke', 'black')
      .attr('stroke-width', '1px');
    g.append('text')
      .attr('x', legendX - circleR + 5)
      .attr('y', legendY + circleR + 15)
      .text(textList[e]);
    legendX += 2 * circleR + marginX;
  }
};

export const drawChart = function (nodes, edges, radioProps, sliderProps, zoomProps) {
  figureData = datas(nodes, edges);
  const {
    width,
    height,
    cantidades_isHonor,
    list_isHonor,
    list_isNotHonor,
    radio_isHonor,
    radio_isNotHonor,
    unions,
  } = figureData;
  console.log(cantidades_isHonor);
  console.log(radio_isHonor);
  console.log(radio_isNotHonor);
  const cantidades_isHonor_sum = Object.entries(cantidades_isHonor).map((d) =>
    d3.sum(Object.values(d[1])),
  );
  sliderProps.max = d3.max(cantidades_isHonor_sum);
  sliderProps.min = d3.min(cantidades_isHonor_sum);
  sliderProps.sliderValue = d3.min(cantidades_isHonor_sum);

  const svg = d3
    .select('#chart')
    .append('svg')
    .attr('id', 'chartSvg')
    .attr('viewBox', [-width / 2, -height / 2, width, height]);

  // 绘制箭头
  const defs = svg.append('defs');
  const arrowMarker = defs
    .append('marker')
    .attr('id', 'arrow')
    .attr('markerUnits', 'strokeWidth')
    .attr('markerWidth', '12')
    .attr('markerHeight', '12')
    .attr('viewBox', '0 0 12 12')
    .attr('refX', '6')
    .attr('refY', '6')
    .attr('orient', 'auto');

  const arrow_path = 'M2,2 L10,6 L2,10 L6,6 L2,2';
  arrowMarker.append('path').attr('d', arrow_path).attr('fill', '#000');

  const g = svg.append('g');

  const link = g
    .selectAll('link')
    .data(unions)
    .enter()
    .append('path')
    .style('stroke', (d) => d.color)
    .style('fill', 'none')
    .attr('class', 'link')
    .attr('list_relacion', (d) => d.list_relacion)
    .attr('opacity', (d) =>
      d.type === radioProps.radioValue &&
      d3.sum(Object.values(d.object_cantidad)) === sliderProps.sliderValue ?
        1 :
        0,
    )
    .attr('d', (d) => d.ruta)
    .attr('marker-end', 'url(#arrow)');
  console.log(link)

  const circle = g
    .selectAll('circle')
    .data(list_isNotHonor.concat(list_isHonor))
    .enter()
    .append('circle')
    .attr('r', (d) => d.radio)
    .attr('cx', (d) => d.x)
    .attr('cy', (d) => d.y)
    .attr('name', (d) => d.name)
    .attr('list_relacion', (d) => d.list_relacion)
    .attr('cursor', 'pointer')
    .attr('opacity', 1)
    .style('fill', (d) => d.color);
  console.log(circle)

  const text = g
    .selectAll('text')
    .data(list_isNotHonor.concat(list_isHonor))
    .enter()
    .append('text')
    .attr('dy', '.35em')
    .attr(
      'transform',
      (d) => `
              rotate(${(d.angulo * 180) / Math.PI})
              translate(${d.radio_general + d.traslado_texto})
              ${Math.cos(d.angulo) < 0 ? 'rotate(180)' : ''}
              `,
    )
    .attr('text-anchor', (d) => (Math.cos(d.angulo) < 0 ? 'end' : null))
    .attr('font-size', '10px')
    .attr('opacity', 1)
    .text((d) => d.name.split('.')[d.name.split('.').length - 1]);
  console.log(text)

  // 鼠标事件
  handleMouseEvent(radioProps.radioValue, sliderProps.sliderValue);

  const zoomed = function (event, d) {
    console.log(d)
    g.attr('transform', event.transform);
  };

  const zoom = d3
    .zoom()
    .extent([
      [-width / 2, -height / 2],
      [width, height],
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
      .call(zoom.transform, d3.zoomIdentity, d3.zoomTransform(g).invert([width / 2, height / 2]));
};

export const changeLinksByRadio = function (radioValue, sliderProps) {
  const cantidades_temp = Object.entries(
    radioValue === 1 ? figureData.cantidades_isHonor : figureData.cantidades_isNotHonor,
  ).map((d) => d3.sum(Object.values(d[1])));
  sliderProps.max = d3.max(cantidades_temp);
  sliderProps.min = d3.min(cantidades_temp);
  sliderProps.sliderValue = d3.min(cantidades_temp);
  changeLinksBySlider(radioValue, sliderProps.sliderValue);
  handleMouseEvent(radioValue, sliderProps.sliderValue);
};

export const changeLinksBySlider = function (radioValue, sliderValue) {
  const svg = d3.select('#chartSvg');
  svg
    .selectAll('.link')
    .style('opacity', 0)
    .filter((d) => {
      return d.type === radioValue && d3.sum(Object.values(d.object_cantidad)) === sliderValue;
    })
    .style('opacity', 1);
  handleMouseEvent(radioValue, sliderValue);
};

const datas = function (nodes, edges) {
  const width = 800,
    height = 800;
  const radio_max = 270,
    radio_min = 175;
  let radio_isHonor = 0,
    radio_isNotHonor = 0;

  // 点信息
  // const nodesNestArray = d3
  //   .nest()
  //   .key((d) => d.isHonor)
  //   .key((d) => d.packageName)
  //   .entries(nodes);
  const nodesNestArray = d3.groups(
    nodes,
    (d) => d.isHonor,
    (d) => d.packageName,
  );
  let nodesObject = {};
  nodesNestArray.forEach((e) => {
    nodesObject[e[0]] = e[1].map((d) => ({
      name: d[0],
      values: d[1],
    }));
  });
  if (nodesObject[1].length > nodesObject[0].length) {
    radio_isHonor = radio_max;
    radio_isNotHonor = radio_min;
  } else {
    radio_isHonor = radio_min;
    radio_isNotHonor = radio_max;
  }

  // 边信息
  // const edgesNestArray = d3
  //   .nest()
  //   .key((d) => d.sourceIsHonor)
  //   .key((d) => d.sourcePackageName)
  //   .rollup((d) =>
  //     d3
  //     .nest()
  //     .key((d) => d.targetIsHonor)
  //     .key((d) => d.targetPackageName)
  //     .entries(d)
  //     .map((e) => ({
  //       name: e.key,
  //       values: e.values.map((f) => f.key),
  //     })),
  //   )
  //   .entries(edges);
  const edgesNestArray = d3.rollups(
    edges,
    (v) =>
      d3.groups(
        v,
        (d) => d.targetIsHonor,
        (d) => d.targetPackageName,
      ),
    (d) => d.sourceIsHonor,
    (d) => d.sourcePackageName,
  );
  let edgesObject = {};
  edgesNestArray.forEach((d) => {
    edgesObject[d[0] === 0 ? 'isNotHonor' : 'isHonor'] = d[1].map((e) => ({
      name: e[0],
      values: e[1],
    }));
  });

  // 初始化
  const cantidad_isHonor = nodesObject[1].length,
    cantidad_isNotHonor = nodesObject[0].length;
  const color_isHonor = d3
      .scaleSequential()
      .domain([0, cantidad_isHonor])
      .interpolator(d3.interpolateHslLong('rgba(219, 58, 52, 1.0)', 'rgba(219, 58, 52, 1.0)')),
    color_isNotHonor = d3
      .scaleSequential()
      .domain([0, cantidad_isNotHonor])
      .interpolator(d3.interpolateRgb('rgba(23, 126, 137, 1.0)', 'rgba(23, 126, 137, 1.0)'));
  const increment_isHonor = (2 * Math.PI) / cantidad_isHonor,
    increment_isNotHonor = (2 * Math.PI) / cantidad_isNotHonor;
  const result_isHonor = generate_circulos(
      nodesObject[1],
      edgesObject.isHonor,
      radio_isHonor,
      15,
      color_isHonor,
      increment_isHonor,
      1,
    ),
    result_isNotHonor = generate_circulos(
      nodesObject[0],
      edgesObject.isNotHonor,
      radio_isNotHonor,
      15,
      color_isNotHonor,
      increment_isNotHonor,
      0,
    );

  // 边赋值
  const unions = [];
  edgesObject.isHonor.forEach((d) => {
    const source = result_isHonor.coordenadas[d.name];
    d.values.forEach((v) => {
      v[1].forEach((e) => {
        const target =
          v[0] === 0 ? result_isNotHonor.coordenadas[e[0]] : result_isHonor
            .coordenadas[e[0]];
        const ruta = linker({
          source_x: source.x,
          source_y: source.y,
          target_x: target.x,
          target_y: target.y,
          target_radio: target.radio,
        });
        const color = source.color;
        unions.push({
          ruta,
          color,
          type: 1,
          object_cantidad: result_isHonor.cantidades[d.name],
          list_relacion: [
            [source.name, 1],
            [target.name, 0],
          ],
        });
      });
    });
  });
  edgesObject.isNotHonor.forEach((d) => {
    const source = result_isNotHonor.coordenadas[d.name];
    d.values
      .filter((e) => e.name === 'isHonor')
      .forEach((v) => {
        v.values.forEach((e) => {
          const target =
            v.name === 'isNotHonor' ?
              result_isNotHonor.coordenadas[e] :
              result_isHonor.coordenadas[e];
          const ruta = linker({
            source_x: source.x,
            source_y: source.y,
            target_x: target.x,
            target_y: target.y,
            target_radio: target.radio,
          });
          const color = source.color;
          unions.push({
            ruta,
            color,
            type: 0,
            object_cantidad: result_isNotHonor.cantidades[d.name],
            list_relacion: [
              [source.name, 0],
              [target.name, 1],
            ],
          });
        });
      });
  });
  const list_isHonor = result_isHonor.resultado,
    list_isNotHonor = result_isNotHonor.resultado;
  const cantidades_isHonor = result_isHonor.cantidades,
    cantidades_isNotHonor = result_isNotHonor.cantidades;
  return {
    width,
    height,
    cantidades_isHonor,
    cantidades_isNotHonor,
    list_isHonor,
    list_isNotHonor,
    radio_isHonor,
    radio_isNotHonor,
    unions,
  };
};

const generate_circulos = function (
  origin_node_data,
  origin_edge_data,
  radio_data,
  text_data,
  escala_colores,
  increment_data,
  type,
) {
  const resultado = [];
  const cantidades = {};
  const coordenadas = {};
  let object_id = 0;
  origin_edge_data.forEach((d) => {
    const object = {};
    d.values.forEach((e) => {
      object[e[0]] = e[1].length;
    });
    cantidades[d.name] = object;
  });
  origin_node_data.forEach((d) => {
    let objeto_nuevo = {};
    objeto_nuevo.name = d.name;
    objeto_nuevo.angulo = object_id * increment_data;
    objeto_nuevo.id = object_id;
    objeto_nuevo.type = type;
    objeto_nuevo.x = radio_data * Math.cos(object_id * increment_data);
    objeto_nuevo.y = radio_data * Math.sin(object_id * increment_data);
    objeto_nuevo.radio = radio_data * Math.sin(Math.PI / origin_node_data.length) - 3;
    objeto_nuevo.color = escala_colores(object_id);
    objeto_nuevo.radio_general = radio_data;
    objeto_nuevo.traslado_texto = text_data;
    const temp = origin_edge_data.filter((e) => e.name === d.name)[0];
    objeto_nuevo.list_relacion = !temp ?
      temp :
      temp.values.map((e) => Object.values(e.values)).reduce((a, b) => a.concat(b));
    coordenadas[objeto_nuevo.name] = {
      x: objeto_nuevo.x,
      y: objeto_nuevo.y,
      radio: objeto_nuevo.radio,
      name: objeto_nuevo.name,
      color: escala_colores(object_id),
    };

    resultado.push(objeto_nuevo);
    object_id++;
  });
  return {
    cantidades,
    coordenadas,
    resultado,
  };
};

const handleMouseEvent = function (radioValue, sliderValue) {
  const svg = d3.select('#chartSvg');
  const circle = svg.selectAll('circle');
  const link = svg.selectAll('.link');
  const text = svg.selectAll('text');
  const tooltip = d3.select('#tooltip').append('div').attr('class', 'tool-tip').text('Nothing');
  const circleFilter = (d, e) => {
    // 是否显示
    let flag = true;
    if (e.name !== d.name) {
      flag = !d.list_relacion ? false : d.list_relacion.indexOf(e.name) >= 0;
      if (e.list_relacion) {
        flag = e.list_relacion.indexOf(d.name) >= 0 ? true : flag;
      }
    }
    return flag;
  };
  const pathFilter = (e) =>
    e.type === radioValue && d3.sum(Object.values(e.object_cantidad)) === sliderValue;
  circle
    .on('mouseover', (event, d) => {
      circle.filter((e) => !circleFilter(d, e)).attr('opacity', 0.1);
      text.filter((e) => !circleFilter(d, e)).attr('opacity', 0.1);
      link
        .style('opacity', 0)
        .filter((e) => pathFilter(e))
        .style('opacity', (e) =>
          !e.list_relacion.filter((f) => f[0] === d.name && f[1] === d.type).length ? 0.1 : 1,
        );
      tooltip.style('left', event.layerX + 25 + 'px').style('top', event.layerY + 70 + 'px');
      tooltip.style('visibility', 'visible').text(d.name);
    })
    .on('mouseout', function (event, d) {
      circle.filter((e) => !circleFilter(d, e)).attr('opacity', 1);
      text.filter((e) => !circleFilter(d, e)).attr('opacity', 1);
      link
        .style('opacity', 0)
        .filter((e) => pathFilter(e))
        .style('opacity', 1);
      tooltip.style('visibility', 'hidden');
    });
  const linkFilter = (d, e) => {
    return !d.list_relacion.filter((f) => f[0] === e.name && f[1] === e.type).length;
  };
  link
    .on('mouseover', (event, d) => {
      if (pathFilter(d)) {
        circle.filter((e) => linkFilter(d, e)).attr('opacity', 0.1);
        text.filter((e) => linkFilter(d, e)).attr('opacity', 0.1);
        link
          .style('opacity', 0)
          .filter((e) => pathFilter(e))
          .style('opacity', (e) => (e.list_relacion !== d.list_relacion ? 0.1 : 1));
      }
    })
    .on('mouseout', (event, d) => {
      circle.filter((e) => linkFilter(d, e)).attr('opacity', 1);
      text.filter((e) => linkFilter(d, e)).attr('opacity', 1);
      link
        .style('opacity', 0)
        .filter((e) => pathFilter(e))
        .style('opacity', 1);
    });
};

const linker = function (d) {
  const x0 = d.source_x,
    x1 = d.target_x;
  const y0 = d.source_y,
    y1 = d.target_y;
  const radio = d.target_radio;
  const path = d3.path();
  path.moveTo(x0, y0);
  const delta = radio / Math.sqrt(1.6);
  const dx = x1 - x0 > 0 ? x1 - delta : x1 + delta,
    dy = y1 - y0 > 0 ? y1 - delta : y1 + delta;
  path.quadraticCurveTo(x0 + (x1 - x0) * 0.25, y0 + (y1 - y0) * 0.75, dx, dy);
  return path.toString();
};
