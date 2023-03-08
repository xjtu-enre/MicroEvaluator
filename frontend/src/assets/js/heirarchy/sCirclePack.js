import * as d3 from 'd3';
import * as $ from 'jquery';
import * as echarts from 'echarts';

export const getData = function (datas) {
  const fileData = [],
    categoryData = {};
  fileData.push({
    value: 'root',
  });
  categoryData['root'] = [];
  datas.children.map(function (data) {
    fileData.push({
      value: data.name,
      label: data.name.replace(/^(.*)android\//i, ''),
    });
    categoryData[data.name] = (function () {
      const arr = [];
      Object.keys(data.relation).forEach(function (key) {
        arr.push(key);
      });
      return arr;
    })();
  });
  return [fileData, categoryData];
};

const figureData = function (datas) {
  let barData = [];
  const result = datas.children.map(function (data) {
    return {
      id: data.id.toString(),
      name: data.name,
      color: data.color,
      children: (function () {
        let arr = [];
        Object.keys(data.relation).forEach(function (key) {
          arr.push({
            id: `${data.id}_${key}`,
            name: `${data.name}/${key}`,
            size: data.value / 10,
            // relation: (function () {
            //   let temp = [];
            //   Object.keys(data.relation[key]).forEach(function (s) {
            //     temp.push({
            //       operate: s,
            //       number: data.relation[key][s],
            //     });
            //   });
            //   return temp;
            // })(),
          });
          Object.keys(data.relation[key]).forEach(function (s) {
            barData.push({
              id: `${data.id}_${key}`,
              operate: s,
              number: data.relation[key][s],
            });
          });
        });
        return arr;
      })(),
    };
  });
  return [result, barData];
};

export const drawsChart = function (temp, params) {
  // TODO bootstrap的popover
  const tooltip = d3
    .select('body')
    .selectAll('#schart')
    .append('div')
    .attr('class', 'tooltip')
    .style('text-align', 'center')
    .style('display', 'block')
    .style('position', 'absolute')
    .style('opacity', '0')
    .style('font-size', '1rem')
    .style('background', 'rgba(255,255,255,0.9)')
    .style('padding', '0.1rem 0.5rem')
    .style('color', 'grey')
    .style('border-radius', '5px')
    .style('border', '1px solid grey')
    .style('pointer-events', 'none');
  // 初始化
  let [data, barData] = figureData(temp);
  const [padding, width, height] = [0, 400, 500];
  const [centerX, centerY] = [width / 2 + 15, height / 2];
  const canvas = d3
    .select('#schart')
    .append('canvas')
    .attr('id', 'canvas')
    .attr('width', width)
    .attr('height', height);
  const context = canvas.node().getContext('2d');
  context.clearRect(0, 0, width, height);
  const hiddenCanvas = d3
    .select('#schart')
    .append('canvas')
    .attr('id', 'hiddenCanvas')
    .attr('width', width)
    .attr('height', height)
    .style('display', 'none');
  const hiddenContext = hiddenCanvas.node().getContext('2d');
  hiddenContext.clearRect(0, 0, width, height);

  // 创建比例尺
  const mainTextColor = [74, 74, 74], //"#4A4A4A",
    titleFont = 'Oswald',
    bodyFont = 'Merriweather Sans';
  const heightColorArray = [
    '#f8f9fa',
    '#e9ecef',
    '#dee2e6',
    '#ced4da',
    '#adb5bd',
    '#6c757d',
    '#495057',
    '#343a40',
    '#212529',
  ];
  // const circleColorArray = ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654'];
  // height越高，颜色越深
  const colorScaleByDepth = d3
    .scaleOrdinal()
    .domain([...Array(heightColorArray.length).keys()].reverse())
    .range(heightColorArray);
  const colorBar = d3
    .scaleOrdinal()
    .domain(['nochange', 'delete', 'insert'])
    .range(['#EFB605', '#E3690B', '#CF003E']);
  const diameter = Math.min(width * 0.9, height * 0.9);
  const commaFormat = d3.format(',');
  const zoomInfo = {
    centerX: centerX,
    centerY: centerY,
    scale: 1,
  };
  let colToCircle = {};
  let nodes = d3.pack().padding(1).size([diameter, diameter])(
    d3
    .hierarchy({
      name: 'root',
      children: data,
    })
    .sum((d) => d.size)
    .sort((a, b) => b.size - a.size),
  );

  // circle pack图数据
  let root = nodes,
    focus = root;
  nodes = root.descendants().slice(0);
  let nodeByName = {};
  nodes.forEach(function (d, i) {
    console.log(i)
    nodeByName[d.data.name] = d;
  });
  let nodeCount = nodes.length;

  // bar图数据
  const barDataMax = d3.rollups(
    barData,
    (v) => d3.max(v, (e) => e.number),
    (d) => d.id,
  );
  const barDataSum = d3.rollups(
    barData,
    (v) => d3.sum(v, (e) => e.number),
    (d) => d.id,
  );
  barData = d3.groups(barData, (d) => d.id);
  let dataById = {};
  barData.forEach((d, i) => {
    dataById[d[0]] = i;
  });
  // 非叶子结点数据
  let IDbyName = {};
  nodes.forEach(function (node) {
    IDbyName[node.data.name] = node.data.id;
  });
  // 画图
  const elementsPerBar = 7,
    barChartHeight = 0.7,
    barChartHeightOffset = 0.15;

  function drawCanvas(chosenContext, hidden) {
    chosenContext.fillStyle = '#fff';
    chosenContext.rect(0, 0, width, height);
    chosenContext.fill();
    let node = null;
    for (let i = 0; i < nodeCount; i++) {
      node = nodes[i];
      if (hidden) {
        if (node.color === undefined) {
          node.color = genColor();
          colToCircle[node.color] = node;
        }
        chosenContext.fillStyle = node.color;
      } else {
        chosenContext.fillStyle = node.children ?
          node.data.color ?
          node.data.color :
          colorScaleByDepth(node.depth) :
          'white';
      }
      const nodeX = (node.x - zoomInfo.centerX) * zoomInfo.scale + centerX,
        nodeY = (node.y - zoomInfo.centerY) * zoomInfo.scale + centerY,
        nodeR = node.r * zoomInfo.scale;
      if (i === 4) scaleFactor = node.value / (nodeR * nodeR);

      chosenContext.beginPath();
      chosenContext.arc(nodeX, nodeY, nodeR, 0, 2 * Math.PI, true);
      chosenContext.fill();
      // 画bar图
      if (node.data.id in dataById) {
        if ((node.data.id.lastIndexOf(currentID, 0) == 0) & !hidden) {
          let drawTitle = true,
            fontSizeTitle = Math.round(nodeR / 10);
          if (fontSizeTitle < 8) {
            drawTitle = false;
          }
          if (drawTitle & showText) {
            chosenContext.font =
              (fontSizeTitle * 0.5 <= 5 ? 0 : Math.round(fontSizeTitle * 0.5)) + 'px ' + bodyFont;
            chosenContext.fillStyle = 'rgba(191,191,191,' + textAlpha + ')'; //"#BFBFBF";
            chosenContext.textAlign = 'center';
            chosenContext.textBaseline = 'middle';
            chosenContext.fillText(
              'Total ' + commaFormat(barDataSum[dataById[node.data.id]][1]),
              nodeX,
              nodeY + -0.75 * nodeR,
            );
            const titleText = getLines(
              chosenContext,
              (function () {
                return node.data.name.split('/').pop();
              })(),
              nodeR * 2 * 0.7,
              fontSizeTitle,
              titleFont,
            );
            //Loop over all the pieces and draw each line
            titleText.forEach(function (txt, iterator) {
              chosenContext.font = fontSizeTitle + 'px ' + titleFont;
              chosenContext.fillStyle =
                'rgba(' +
                mainTextColor[0] +
                ',' +
                mainTextColor[1] +
                ',' +
                mainTextColor[2] +
                ',' +
                textAlpha +
                ')';
              chosenContext.textAlign = 'center';
              chosenContext.textBaseline = 'middle';
              chosenContext.fillText(txt, nodeX, nodeY + (-0.65 + iterator * 0.125) * nodeR);
            });
          }
          const barScale = d3
            .scaleLinear()
            .domain([0, barDataMax[dataById[node.data.id]][
            1]]) //max value of bar charts in circle
            .range([0, nodeR]);
          const bars = barData[dataById[node.data.id]][1],
            eachBarHeight =
            ((1 - barChartHeightOffset) * 2 * nodeR * barChartHeight) / elementsPerBar,
            barHeight = eachBarHeight * 0.8;
          let drawLabelText = true;
          const fontSizeLabels = Math.round(nodeR / 18);
          if (fontSizeLabels < 6) drawLabelText = false;
          let drawValueText = true;
          const fontSizeValues = Math.round(nodeR / 22);
          if (fontSizeValues < 6) drawValueText = false;
          if (Math.round(barHeight) > 1) {
            for (let j = 0; j < bars.length; j++) {
              let bar = bars[j];
              bar.width = isNaN(bar.number) ? 0 : barScale(bar.number);
              bar.barPiecePosition =
                nodeY +
                barChartHeightOffset * 2 * nodeR +
                j * eachBarHeight -
                barChartHeight * nodeR;
              //Draw the bar
              chosenContext.beginPath();
              chosenContext.fillStyle = colorBar(bar.operate);
              chosenContext.fillRect(
                nodeX + -nodeR * 0.3,
                bar.barPiecePosition,
                bar.width,
                barHeight,
              );
              chosenContext.fill();
              if (drawLabelText & showText) {
                chosenContext.font = fontSizeLabels + 'px ' + bodyFont;
                chosenContext.fillStyle =
                  'rgba(' +
                  mainTextColor[0] +
                  ',' +
                  mainTextColor[1] +
                  ',' +
                  mainTextColor[2] +
                  ',' +
                  textAlpha +
                  ')';
                chosenContext.textAlign = 'right';
                chosenContext.textBaseline = 'middle';
                chosenContext.fillText(
                  bar.operate,
                  nodeX + -nodeR * 0.35,
                  bar.barPiecePosition + 0.5 * barHeight,
                );
              } //if
              if (drawValueText & showText) {
                chosenContext.font = fontSizeValues + 'px ' + bodyFont;
                var txt = commaFormat(bar.number);
                //Check to see if the bar is big enough to place the text inside it
                //If not, place the text outside the bar
                var textWidth = chosenContext.measureText(txt).width;
                var valuePos = textWidth * 1.1 > bar.width - nodeR * 0.03 ? 'left' : 'right';

                //Calculate the x position of the bar value label
                bar.valueLoc =
                  nodeX +
                  -nodeR * 0.3 +
                  bar.width +
                  (valuePos === 'left' ? nodeR * 0.03 : -nodeR * 0.03);

                //Draw the text
                chosenContext.fillStyle =
                  valuePos === 'left' ?
                  'rgba(51,51,51,' + textAlpha + ')' :
                  'rgba(255,255,255,' + textAlpha + ')'; //#333333 or white
                chosenContext.textAlign = valuePos;
                chosenContext.textBaseline = 'middle';
                chosenContext.fillText(txt, bar.valueLoc, bar.barPiecePosition + 0.5 * barHeight);
              } //if
            }
          }
        }
      }
    }
    let counter = 0;
    for (let i = 0; i < nodeCount; i++) {
      node = nodes[i];
      const nodeX = (node.x - zoomInfo.centerX) * zoomInfo.scale + centerX,
        nodeY = (node.y - zoomInfo.centerY) * zoomInfo.scale + centerY,
        nodeR = node.r * zoomInfo.scale;
      if ((typeof node.parent !== 'undefined') & (typeof node.children !== 'undefined')) {
        if (
          (node.data.name !== 'root') &
          !hidden &
          showText &
          kids.includes(node.data.name) &
          textFocus
        ) {
          //Calculate the best font size for the non-leaf nodes
          const fontSizeTitle = Math.round(nodeR / 10);
          if (fontSizeTitle > 0.04) {
            drawCircularText(
              chosenContext,
              node.data.name,
              fontSizeTitle,
              titleFont,
              nodeX,
              nodeY,
              nodeR,
              rotationText[counter],
              0,
            );
          }
        } //if
        counter = counter + 1;
      } //if
    }
  }

  function getParamsValue(node) {
    debugger
    params.value =
      node.height === 1 ?
      {
        height: 1,
        datas: node.children.map((e) => barData[dataById[e.data.id]]),
      } :
      {
        height: node.height,
      };
  }

  // 点击事件
  let currentID = '',
    // oldID = '',
    kids = ['root'];
  data.forEach(function (data) {
    kids.push(data.name);
  });
  const clickFunction = function (e) {
    const mouseX = e.offsetX,
      mouseY = e.offsetY;
    const col = hiddenContext.getImageData(mouseX, mouseY, 1, 1).data;
    const colString = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')';
    let node = colToCircle[colString];
    if (node) {
      //If the same node is clicked twice, set it to the top (root) level
      if (focus === node) node = root;
      getParamsValue(node);

      //Save the names of the circle itself and first children
      //Needed to check which arc titles to show
      kids = [node.data.name];
      if (typeof node.children !== 'undefined') {
        for (let i = 0; i < node.children.length; i++) {
          kids.push(node.children[i].data.name);
        } //for i
      } //if

      //Perform the zoom
      zoomToCanvas(node);
    } //if -> node
  };
  document.getElementById('canvas').addEventListener('click', clickFunction);

  // 鼠标移动事件
  let nodeOld = root;
  const mousemoveFunction = function (e) {
    const mouseX = e.offsetX,
      mouseY = e.offsetY;
    const col = hiddenContext.getImageData(mouseX, mouseY, 1, 1).data;
    //Our map uses these rgb strings as keys to nodes.
    const colString = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')';
    let node = colToCircle[colString];
    tooltip.style('opacity', 0);
    if (node !== nodeOld) {
      if (node) {
        if (node.depth !== 0) {
          const nodeX = (node.x - zoomInfo.centerX) * zoomInfo.scale + centerX,
            nodeY = (node.y - zoomInfo.centerY) * zoomInfo.scale + centerY,
            nodeR = node.r * zoomInfo.scale;
          //Position the wrapper right above the circle
          // $("[data-toggle='popover']").tooltip('show');
          tooltip
            .style('opacity', '1')
            .style('top', nodeY - nodeR)
            .style('left', nodeX + (padding * 5) / 4)
            .html(node.data.name);
        } //if -> typeof node.ID !== "undefined"
      } //if -> node
    }
  };
  document.getElementById('canvas').addEventListener('mousemove', mousemoveFunction);

  // zoom事件

  let ease = d3.easeCubicInOut,
    interpolator = null,
    duration = 1500,
    timeElapsed = 0, //Starting duration
    vOld = [focus.x, focus.y, focus.r * 2.05];

  function zoomToCanvas(focusNode) {
    $('#canvas').css('pointer-events', 'none');
    //Remove all previous popovers - if present
    // $('.popoverWrapper').remove();
    // $('.popover').each(function () {
    //   $('.popover').remove();
    // });
    if (focusNode === focus) {
      currentID = '';
    } else {
      if (typeof IDbyName[focusNode.data.name] !== 'undefined') {
        const temp = IDbyName[focusNode.data.name];
        const index = temp.indexOf('_');
        currentID = index === -1 ? temp : temp.substring(0, index);
      } else {
        currentID = 'root';
      }
    }
    focus = focusNode;
    textFocus = focus.depth == 1;
    const v = [focus.x, focus.y, focus.r * 2.05];
    interpolator = d3.interpolateZoom(vOld, v);
    duration = Math.max(1500, interpolator
    .duration); //Interpolation gives back a suggested duration
    timeElapsed = 0; //Set the time elapsed for the interpolateZoom function to 0
    showText = false; //Don't show text during the zoom
    vOld = v; //Save the "viewport" of the next state as the next "old" state
    stopTimer = false;
    animate();
  }

  function interpolateZoom(dt) {
    if (interpolator) {
      timeElapsed += dt;
      let t = ease(timeElapsed / duration);

      //Set the new zoom variables
      zoomInfo.centerX = interpolator(t)[0];
      zoomInfo.centerY = interpolator(t)[1];
      zoomInfo.scale = diameter / interpolator(t)[2];

      //After iteration is done remove the interpolater and set the fade text back into motion
      if (timeElapsed >= duration) {
        interpolator = null;
        showText = true;
        fadeText = true;
        timeElapsed = 0;
        drawCanvas(hiddenContext, true);
      } //if -> timeElapsed >= duration
    } //if -> interpolator
  }

  let showText = true, //Only show the text while you're not zooming
    textAlpha = 1, //After a zoom is finished fade in the text;
    textFocus = false,
    fadeText = false,
    fadeTextDuration = 750;
  //Function that fades in the text - Otherwise the text will be jittery during the zooming
  function interpolateFadeText(dt) {
    if (fadeText) {
      timeElapsed += dt;
      textAlpha = ease(timeElapsed / fadeTextDuration);
      if (timeElapsed >= fadeTextDuration) {
        //Enable click & mouseover events again
        $('#canvas').css('pointer-events', 'auto');

        fadeText = false; //Jump from loop after fade in is done
        stopTimer = true; //After the fade is done, stop with the redraws / animation
      } //if
    } //if
  }

  let nextCol = 1;

  function genColor() {
    let ret = [];
    if (nextCol < 16777215) {
      ret.push(nextCol & 0xff); // R
      ret.push((nextCol & 0xff00) >> 8); // G
      ret.push((nextCol & 0xff0000) >> 16); // B

      nextCol += 100; // This is exagerated for this example and would ordinarily be 1.
    }
    let col = 'rgb(' + ret.join(',') + ')';
    return col;
  }

  function getLines(ctx, text, maxWidth, fontSize, titleFont) {
    const words = text.split(' '),
      lines = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
      const word = words[i];
      ctx.font = fontSize + 'px ' + titleFont;
      const width = ctx.measureText(currentLine + ' ' + word).width;
      if (width < maxWidth) {
        currentLine += ' ' + word;
      } else {
        lines.push(currentLine);
        currentLine = word;
      }
    }
    lines.push(currentLine);
    return lines;
  }

  const rotationText = [
    -14, 4, 23, -18, -10.5, -20, 20, 20, 46, -30, -25, -20, 20, 15, -30, -15, -45, 12, -15, -16,
    15,
    15, 5, 18, 5, 15, 20, -20, -25,
  ]; //The rotation of each arc text

  //Adjusted from: http://blog.graphicsgen.com/2015/03/html5-canvas-rounded-text.html
  function drawCircularText(
    ctx,
    text,
    fontSize,
    titleFont,
    centerX,
    centerY,
    radius,
    startAngle,
    kerning,
  ) {
    ctx.textBaseline = 'alphabetic';
    ctx.textAlign = 'center'; // Ensure we draw in exact center
    ctx.font = fontSize + 'px ' + titleFont;
    ctx.fillStyle = 'rgba(255,255,255,' + textAlpha + ')';

    startAngle = startAngle * (Math.PI / 180); // convert to radians
    text = text.split('').reverse().join(''); // Reverse letters

    //Rotate 50% of total angle for center alignment
    for (let j = 0; j < text.length; j++) {
      let charWid = ctx.measureText(text[j]).width;
      startAngle += (charWid + (j == text.length - 1 ? 0 : kerning)) / radius / 2;
    } //for j

    ctx.save(); //Save the default state before doing any transformations
    ctx.translate(centerX, centerY); // Move to center
    ctx.rotate(startAngle); //Rotate into final start position

    //Now for the fun bit: draw, rotate, and repeat
    for (let j = 0; j < text.length; j++) {
      let charWid = ctx.measureText(text[j]).width / 2; // half letter
      //Rotate half letter
      ctx.rotate(-charWid / radius);
      //Draw the character at "top" or "bottom" depending on inward or outward facing
      ctx.fillText(text[j], 0, -radius);
      //Rotate half letter
      ctx.rotate(-(charWid + kerning) / radius);
    } //for j

    ctx.restore(); //Restore to state as it was before transformations
  }

  function animate() {
    let dt = 0;
    const t = d3.timer(function (elapsed) {
      if (!stopTimer) {
        interpolateZoom(elapsed - dt);
        interpolateFadeText(elapsed - dt);
        dt = elapsed;
        drawCanvas(context, false);
        return stopTimer;
      }
      t.stop();
    });
  }

  function searchBox(node) {
    if ((node !== '') & (typeof node !== 'undefined')) {
      const item = nodeByName[node];
      getParamsValue(item);
      zoomToCanvas(item);
    }
  }

  let stopTimer = false;
  let scaleFactor = 1;
  console.log(scaleFactor)
  zoomToCanvas(root);
  drawCanvas(hiddenContext, true);
  animate();
  return searchBox;
};

export const drawLegend = function () {
  const svg = d3
      .select('#slegend')
      .append('svg')
      .attr('id', 'legendSvg')
      .attr('width', 250)
      .attr('height', 50);
  const gs = svg.append('g');
  gs.append('rect').attr('x', 0).attr('width', 250).attr('height', 50).attr('fill', 'white');
  // gs.append('text').attr('x', 0).attr('y', 15).text('代码修改频率');
  const colorList = ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654'];
  const textList = ['<50', '<100', '<500', '<1000', '>1000'];
  let legendX = 25,
      legendY = 17;
  const marginX = 18,
      circleR = 15;
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
        .attr('x', legendX - circleR)
        .attr('y', legendY + circleR + 15)
        .text(textList[e]);
    legendX += 2 * circleR + marginX;
  }
};
export const drawRootClusters = function (datas) {
  const clusters = d3
    .groups(datas.children, (d) => d.color)
    .sort((a, b) => a[1].length - b[1].length);
  const colorType = ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654'];
  const textScale = d3
    .scaleOrdinal()
    .domain(colorType)
    .range(['<50', '<100', '<500', '<1000', '>1000']);
  const yAxisData = clusters.map((d) => textScale(d[0]));
  const seriesData = clusters.map((d) => d[1].length);
  const colorData = clusters.map((d) => d[0]);
  const chartDom = document.getElementById('clusters');
  let myChart = echarts.getInstanceByDom(chartDom);
  if (myChart == null) {
    myChart = echarts.init(chartDom);
  }
  myChart.hideLoading();
  const option = {
    title: {
      text: '',
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
    series: [{
      type: 'bar',
      itemStyle: {
        color: (params) => colorData[params.dataIndex],
      },
      label: {
        show: true,
        position: 'right',
      },
      data: seriesData,
    }, ],
  };
  option && myChart.setOption(option, true);
};

export const drawNodeClusters = function (datas) {
  const categoryType = ['nochange', 'delete', 'insert'];
  const colorBar = d3.scaleOrdinal().domain(categoryType).range(['#EFB605', '#E3690B',
  '#CF003E']);
  const yAxisData = datas.datas.map((e) => e[0].split('_')[1]);
  const seriesData = {};
  categoryType.forEach((e) => {
    seriesData[e] = datas.datas.map((d) =>
      !d[1].filter((c) => c.operate === e).length ?
      0 :
      d[1].filter((c) => c.operate === e)[0].number,
    );
  });
  const chartDom = document.getElementById('clusters');
  let myChart = echarts.getInstanceByDom(chartDom);
  if (myChart == null) {
    myChart = echarts.init(chartDom);
  }
  myChart.hideLoading();
  const option = {
    title: {
      text: '',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        // Use axis to trigger tooltip
        type: 'shadow', // 'shadow' as default; can also be 'line' or 'shadow'
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
    series: categoryType.map((e) => ({
      name: e,
      type: 'bar',
      stack: 'total',
      label: {
        show: false,
      },
      itemStyle: {
        color: colorBar(e),
      },
      emphasis: {
        focus: 'series',
      },
      data: seriesData[e],
    })),
  };
  option && myChart.setOption(option, true);
};
