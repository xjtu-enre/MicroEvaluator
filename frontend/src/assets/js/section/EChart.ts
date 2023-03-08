// import * as echarts from 'echarts';
// import { scaleOrdinal } from 'd3';
//
// const DATATYPES = {
//   CATEGORY: ['Class', 'Interface', 'Method', 'Variable'],
//   ACCESSIBILITY: ['Default', 'Private', 'Protected', 'Public'],
// };
// const SYMBOLTYPES = ['circle', 'rect', 'triangle', 'diamond'];
// const symbolScale = scaleOrdinal().domain(DATATYPES.ACCESSIBILITY).range(SYMBOLTYPES);
//
// const getTooltip = function (data) {
//   let str = '';
//   for (const [key, val] of Object.entries(data.data)) {
//     if (key !== 'accessibility' && val !== null) {
//       str += `${key} : ${val}`;
//       str += '<br>';
//     }
//   }
//   return str;
// };
//
// const figureEChartsData = function (nodes, edges) {
//   const datas = nodes.map(function (node) {
//     const nodeOption = {
//       name: node._id.toString(),
//       category: node.category,
//       symbol: symbolScale(node.accessibility),
//       symbolSize: 30,
//       label: {
//         show: false,
//       },
//       itemStyle: {
//         borderColor: '#fff',
//         borderWidth: 1,
//         shadowBlur: node.isHonor === 1 ? 10 : 0,
//         opacity: node.isShow ? 1 : 0,
//       },
//       cursor: node.isShow ? 'pointer' : 'auto',
//       tooltip: {
//         show: node.isShow,
//         trigger: 'item',
//         formatter: function (params) {
//           return getTooltip(params.data);
//         },
//       },
//       data: {
//         nodeName: node.name,
//         isHonor: node.isHonor,
//         mode: node.mode_type,
//         accessibility: node.accessibility,
//         static: node.static,
//         global: node._global,
//       },
//       isShow: node.isShow,
//     };
//     nodeOption['emphasis'] = node.isShow
//       ? {
//           focus: 'adjacency',
//           lineStyle: {
//             width: 10,
//           },
//         }
//       : {
//           disabled: false,
//         };
//     return nodeOption;
//   });
//   const legendData = getLegendData(nodes);
//   const links = edges.map(function (link) {
//     const linkOption = {
//       source: link.source.toString(),
//       target: link.target.toString(),
//       value: link.value,
//       tooltip: {
//         show: link.isShow,
//         trigger: 'item',
//         formatter: function (params) {
//           return params.data.value;
//         },
//       },
//       lineStyle: {
//         cursor: link.isShow ? 'pointer' : 'auto',
//         opacity: link.isShow ? 1 : 0,
//       },
//       isShow: link.isShow,
//     };
//     linkOption['emphasis'] = link.isShow
//       ? {
//           focus: 'adjacency',
//           lineStyle: {
//             width: 10,
//           },
//         }
//       : {
//           disabled: false,
//         };
//     return linkOption;
//   });
//   return [datas, legendData, links];
// };
//
// const getLegendData = function (data) {
//   const categoryTemp = data.filter((e) => e.isShow).map((e) => e.category),
//     accessibilityTemp = data.filter((e) => e.isShow).map((e) => e.accessibility);
//   const categoryData = [...new Set(categoryTemp)].map((e) => ({ name: e })),
//     accessibilityData = [...new Set(accessibilityTemp)].map((e) => ({ name: e })),
//     isHonorData = [{ name: 'isHonor' }];
//   const result = {
//     categoryData,
//     accessibilityData,
//     isHonorData,
//     categories: categoryData.concat(accessibilityData).concat(isHonorData),
//   };
//   return result;
// };
//
// const drawLegend = function (datas) {
//   const categoryLegend = [
//     {
//       data: datas.categoryData,
//       icon: 'roundRect',
//       x: '0%',
//       y: '10%',
//     },
//   ];
//   const accessibilityLegend = [];
//   for (let i = 0; i < datas.accessibilityData.length; i++) {
//     const accessibilityType = datas.accessibilityData[i].name;
//     accessibilityLegend.push({
//       data: [accessibilityType],
//       icon: symbolScale(accessibilityType),
//       itemStyle: {
//         color: '#00bfff',
//       },
//       x: new String(5 * i) + '%',
//       y: '15%',
//     });
//   }
//   const isHonorLegend = [
//     {
//       data: ['isHonor'],
//       icon: 'roundRect',
//       itemStyle: {
//         borderColor: '#fff',
//         borderWidth: 1,
//         shadowBlur: 10,
//       },
//       x: '0%',
//       y: '20%',
//     },
//   ];
//   const result = categoryLegend.concat(accessibilityLegend).concat(isHonorLegend);
//   return result;
// };
//
// export const getData = function (datas) {
//   let nodes = [];
//   Object.values(
//     d3
//       .nest()
//       .key((e) => e.category)
//       .entries(datas),
//   ).forEach((e) => (nodes = nodes.concat(e.values)));
//   console.log(nodes);
//   const modeArr = [];
//   datas.forEach((e) => {
//     e.mode_type.forEach((d) => {
//       modeArr.push(d);
//     });
//   });
//   return {
//     modeData: [...new Set(modeArr)].map((e) => ({
//       value: e,
//     })),
//     nodes,
//   };
// };
//
// export const draw = function (mode, data1, data2) {
//   if (mode === '') {
//     data1.forEach((e) => {
//       e.isShow = true;
//     });
//     data2.forEach((e) => {
//       e.isShow = true;
//     });
//   } else {
//     data1.forEach((e) => {
//       e.isShow = e.mode_type.indexOf(mode) !== -1;
//     });
//     data2.forEach((e) => {
//       e.isShow = e.mode_type === mode;
//     });
//   }
//   drawChart(data1, data2);
// };
//
// const drawChart = function (data1, data2) {
//   const [datas, legendData, links] = figureEChartsData(data1, data2);
//   const chartDom = document.getElementById('chart')!;
//   let mychart = echarts.getInstanceByDom(chartDom);
//   if (mychart == null) {
//     mychart = echarts.init(chartDom);
//   }
//   mychart.hideLoading();
//   const option = {
//     title: {
//       text: '依赖切面环状关系图',
//       top: 'top',
//       left: 'left',
//     },
//     tooltip: {
//       trigger: 'item',
//     },
//     legend: drawLegend(legendData),
//     animationDurationUpdate: 1500,
//     animationEasingUpdate: 'quinticInOut',
//     series: [
//       {
//         type: 'graph',
//         layout: 'circular',
//         circular: {
//           rotateLabel: true,
//         },
//         roam: true,
//         legendHoverLink: false,
//         data: datas,
//         links,
//         categories: legendData.categories,
//         lineStyle: {
//           color: 'source',
//           curveness: 0.3,
//         },
//         edgeSymbol: ['none', 'arrow'],
//         edgeSymbolSize: 6,
//         itemStyle: {
//           borderCap: 'butt',
//         },
//       },
//     ],
//   };
//   mychart.setOption(option);
//
//   const colorScale = {};
//   for (let i = 0; i < legendData.categoryData.length; i++) {
//     colorScale[legendData.categoryData[i].name] = mychart.getOption().color[i];
//   }
//
//   const forceDom = document.getElementById('force');
//   let myForce = echarts.getInstanceByDom(forceDom);
//   if (myForce == null) {
//     myForce = echarts.init(forceDom);
//   }
//   myForce.hideLoading();
//   const forceSeries = {
//     type: 'graph',
//     layout: 'force',
//     label: {
//       formatter: (params) => params.data.data.nodeName,
//       position: 'bottom',
//     },
//     roam: true,
//     draggable: true,
//     scaleLimit: {
//       min: 0.4,
//       max: 2,
//     },
//     force: {
//       edgeLength: 15,
//       repulsion: 300,
//     },
//     lineStyle: {
//       color: 'source',
//       curveness: 0.3,
//     },
//     emphasis: {
//       focus: 'adjacency',
//       lineStyle: {
//         width: 10,
//       },
//     },
//     edgeSymbol: ['none', 'arrow'],
//     edgeSymbolSize: 6,
//   };
//   drawForce(myForce, forceSeries, { data: [], links: [], categories: [] });
//   const legendStack = [];
//   // TODO 点击小类效果不好
//   mychart.on('legendselectchanged', function (params) {
//     let nodes = datas;
//     let edges = links;
//     let temp: string[] | undefined = [];
//     if (params.selected[params.name]) {
//       temp = legendStack.pop();
//       temp.splice(temp.indexOf(params.name), 1);
//     } else {
//       temp = Object.keys(params.selected).filter((d) => !params.selected[d]);
//       legendStack.push(temp);
//     }
//     console.log(temp);
//     temp.forEach((e) => {
//       if (DATATYPES.CATEGORY.indexOf(e) !== -1) {
//         nodes = nodes.filter((d) => d.category !== e);
//       } else if (e.indexOf('isHonor') !== -1) {
//         nodes = nodes.filter((d) => d.data.isHonor !== 1);
//       } else {
//         nodes = nodes.filter((d) => d.data.accessibility !== e);
//       }
//     });
//     const categoryData = legendData.categoryData
//         .map((e) => e.name)
//         .filter((e) => [...new Set(nodes.map((e) => e.category))].indexOf(e) === -1),
//       accessibilityData = legendData.accessibilityData
//         .map((e) => e.name)
//         .filter((e) => [...new Set(nodes.map((e) => e.data.accessibility))].indexOf(e) === -1);
//     const state = {
//       categoryData,
//       accessibilityData,
//     };
//     Object.keys(state).forEach((e) => {
//       if (state[e].length) {
//         state[e].forEach((d) => {
//           params.selected[d] = false;
//           mychart.dispatchAction({
//             type: 'legendUnSelect',
//             name: `${d}`,
//           });
//         });
//       } else {
//         DATATYPES[e.substring(0, e.indexOf('Data')).toUpperCase()].forEach((d) => {
//           params.selected[d] = true;
//           mychart.dispatchAction({
//             type: 'legendSelect',
//             name: `${d}`,
//           });
//         });
//       }
//     });
//     const nodesData = nodes.map((e) => e.name);
//     edges = edges.filter(
//       (e) => nodesData.indexOf(e.source) !== -1 && nodesData.indexOf(e.target) !== -1,
//     );
//     mychart.setOption({
//       series: [
//         {
//           data: nodes,
//           links: edges,
//         },
//       ],
//     });
//     drawForce(myForce, forceSeries, { data: [], links: [], categories: [] });
//   });
//   let focus;
//   mychart.on('mouseover', (params) => {
//     if (params.data.isShow) {
//       {
//         const chartOptionData = mychart.getOption().series[0].data,
//           chartOptionLinks = mychart.getOption().series[0].links;
//         const nowData = chartOptionData.filter((e) => e.isShow),
//           nowLinks = chartOptionLinks.filter((e) => e.isShow);
//         focus = params;
//         if (params.dataType === 'node') {
//           let nodes = [];
//           nowLinks.forEach((e) => {
//             if (e.source === params.name || e.target === params.name) {
//               nodes.push(e.source);
//               nodes.push(e.target);
//             }
//           });
//           nodes = [...new Set(nodes)];
//           nodes = nowData.filter((e) => nodes.indexOf(e.name) > -1);
//           nodes.forEach((e) => {
//             e.itemStyle.color = colorScale[e.category];
//             e.label.show = true;
//             e.symbolSize = 15;
//           });
//           const edges = nowLinks.filter(
//             (e) => e.source === params.name || e.target === params.name,
//           );
//           const categories = [...new Set(nodes.map((e) => e.category))];
//           const property = {
//             data: nodes,
//             links: edges,
//             categories,
//           };
//           drawForce(myForce, forceSeries, property);
//         } else {
//           const nodes = [];
//           nodes.push(nowData.filter((e) => e.name === params.data.source)[0]);
//           nodes.push(nowData.filter((e) => e.name === params.data.target)[0]);
//           nodes.forEach((e) => {
//             e.itemStyle.color = colorScale[e.category];
//             e.label.show = true;
//             e.symbolSize = 15;
//           });
//           const edges = nowLinks.filter(
//             (e) => e.source === params.data.source && e.target === params.data.target,
//           );
//           const categories = [...new Set(nodes.map((e) => e.category))];
//           const property = {
//             data: nodes,
//             links: edges,
//             categories,
//           };
//           drawForce(myForce, forceSeries, property);
//         }
//         let dataIndex = 0;
//         myForce.on('mouseover', (params) => {
//           if (params.dataType === 'node') {
//             for (let i = 0; i < chartOptionData.length; i++) {
//               if (chartOptionData[i].name === params.name) {
//                 dataIndex = i;
//                 break;
//               }
//             }
//             mychart.dispatchAction({ type: 'showTip', seriesIndex: 0, dataIndex });
//             if (params.name === focus.name) {
//               mychart.dispatchAction({
//                 type: 'highlight',
//                 seriesIndex: 0,
//                 dataType: params.dataType,
//                 dataIndex,
//               });
//             } else {
//               if (focus.dataType === 'edge') {
//                 dataIndex = focus.dataIndex;
//               } else {
//                 for (let i = 0; i < chartOptionLinks.length; i++) {
//                   if (
//                     (chartOptionLinks[i].source === params.name &&
//                       chartOptionLinks[i].target === focus.name) ||
//                     (chartOptionLinks[i].source === focus.name &&
//                       chartOptionLinks[i].target === params.name)
//                   ) {
//                     dataIndex = i;
//                     break;
//                   }
//                 }
//               }
//               // edge tooltip显示不了
//               mychart?.dispatchAction({
//                 type: 'highlight',
//                 seriesIndex: 0,
//                 dataType: 'edge',
//                 dataIndex,
//               });
//             }
//           } else {
//             mychart?.dispatchAction({
//               type: 'highlight',
//               seriesIndex: 0,
//               dataType: 'edge',
//               dataIndex: focus.dataIndex,
//             });
//           }
//         });
//         myForce?.on('mouseout', (params) => {
//           if (params.dataType === 'node') {
//             mychart?.dispatchAction({ type: 'hideTip', seriesIndex: 0, dataIndex });
//             mychart?.dispatchAction({
//               type: 'downplay',
//               seriesIndex: 0,
//               dataIndex,
//               dataType: params.name === focus.name ? 'node' : 'edge',
//             });
//           } else {
//             mychart?.dispatchAction({
//               type: 'downplay',
//               seriesIndex: 0,
//               dataIndex,
//               dataType: 'edge',
//             });
//           }
//         });
//       }
//     }
//   });
// };
//
// const drawForce = function (myChart, series, property) {
//   series = { ...series, ...property };
//   const option = {
//     animationDuration: 1500,
//     animationEasingUpdate: 'quinticInOut',
//     series: [series],
//   };
//   option && myChart.setOption(option);
// };
