import * as echarts from 'echarts';

const getTooltipFormatter = function () {
  return function (params) {
    const value = params.value;
    const treePathInfo = params.treePathInfo;
    let treePath = [];
    for (let i = 1; i < treePathInfo.length; i++) {
      treePath.push(treePathInfo[i].name);
    }
    return [
      '<div class="tooltip-title">' + echarts.format.encodeHTML(treePath.join('.')) +
      '</div><br>',
      value[3] === 1 ? 'File Count: &nbsp;&nbsp;' + value[2] : 'ChangeLoc: &nbsp;&nbsp;' +
        value[2],
    ].join('');
  };
};

const createSeriesOption = function () {
  return {
    type: 'treemap',
    tooltip: {
      formatter: getTooltipFormatter(),
    },
    leafDepth: 2,
    upperLabel: {
      show: true,
      height: 30,
    },
    levels: [{
      itemStyle: {
        borderColor: '#555',
        borderWidth: 4,
        gapWidth: 4,
      },
    },
      {
        colorSaturation: [0.3, 0.6],
        itemStyle: {
          borderColorSaturation: 0.7,
          gapWidth: 2,
          borderWidth: 2,
        },
      },
      {
        colorSaturation: [0.3, 0.5],
        itemStyle: {
          borderColorSaturation: 0.6,
          gapWidth: 1,
        },
      },
      {
        colorSaturation: [0.3, 0.5],
      },
    ],
  };
};

const modes = ['LOC', 'FILE'];

export const drawChart = function (data) {
  const treeData = data.children;
  const dataId = [];
  const chartDom = document.getElementById('chart');
  let mychart = echarts.getInstanceByDom(chartDom);
  if (mychart == null) {
    mychart = echarts.init(chartDom);
  }
  mychart.hideLoading();

  const buildData = function buildData(mode, originList, basePath) {
    let out = [];
    for (let i = 0; i < originList.length; i++) {
      let node = originList[i];
      const path = basePath ? basePath + '.' + node.name : node.name;
      node.id = path;
      if (mode === 0) {
        dataId.push({
          value: path,
        });
      }
      let newNode = cloneNodeInfo(node);
      if (!newNode) {
        continue;
      }
      out[i] = newNode;
      let value = newNode.value;
      if (mode === 1) {
        let tmp = value[1];
        value[1] = value[0];
        value[0] = tmp;
      }
      if (node.children) {
        newNode.children = buildData(mode, node.children, path);
      }
    }
    return out;
  };

  const cloneNodeInfo = function (node) {
    if (!node) {
      return;
    }
    const newNode = {};
    newNode.name = node.name;
    newNode.id = node.id;
    newNode.value = (node.value || []).slice();
    return newNode;
  };

  const option = {
    tooltip: {},
    roam: false,
    legend: {
      data: modes,
      selectedMode: 'single',
      top: 55,
      itemGap: 5,
      borderRadius: 5,
    },
    series: modes.map(function (mode, idx) {
      const seriesOpt = createSeriesOption();
      seriesOpt.name = mode;
      seriesOpt.data = buildData(idx, treeData, '');
      return seriesOpt;
    }),
  };
  mychart.setOption(option);
  mychart.on('click', function (params) {
    console.log(params);
  });
  return dataId;
};

export const selectCallback = function (value) {
  console.log(value)
  const chartDom = document.getElementById('chart');
  const mychart = echarts.getInstanceByDom(chartDom);
  return mychart;
};
