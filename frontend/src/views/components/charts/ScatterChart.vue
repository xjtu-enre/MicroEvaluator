<template>
  <div>
    <div class="card">
      <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
        <div
            class="bg-gradient-success shadow-success border-radius-lg pt-4 pb-3"
        >
          <h6 class="text-white text-capitalize ps-3">Quality Distribution of Population</h6>
        </div>
      </div>
      <div class="card-body">
        <div id="scoregraph" style="height: 400px;margin-top: -70px;"></div>
        <select-card style="margin-bottom: 10px;" @change-opt2="handleChangeMetric"
                     :opts="metrics"
                     :optnames="optnames"></select-card>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import SelectCard from "../cards/SelectCard.vue";


export default {
  name: "ScatterChart",
  props: {
    'scatterData': Array,
    'metrics': Array,
    'optnames': Array
  },
  components: {
    SelectCard,
    // ChartHol derCard
  },
  // mounted只会在挂载的时候执行一次，故无法进行后续更新，此时使用watch进行图表的更新
  mounted() {
    console.log('this.scatterData', this.scatterData)
    this.drawScoreGraph(this.scatterData, 'score', 4);
  },
  data() {
    return {
      myChart: "",
      option: []
    };
  },
  watch: {
    scatterdata() {
      this.$nextTick(() => {
        console.log('hhhh', this.metrics)
        this.drawScoreGraph(this.scatterData, 'score', 4);
      })
    }
  },
  methods: {
    handleChangeMetric(metric, metricIndex) {
      this.drawScoreGraph(this.scatterData, metric, metricIndex);
    },
    drawScoreGraph(scatterData, metric, dimension_index) {
      // 初始化echarts实例
      var myChart = echarts.init(document.getElementById("scoregraph"), 'macarons');
      this.myChart = myChart
      var COLOR = [
        'rgb(0,100,0)',
        'rgb(144,238,144)',
        'rgb(255,215,0)',
        'rgb(220, 20, 60)'
      ];
      // 指定图表的配置项和数据
      this.option = {
        dataset: [{
          source: scatterData
        }
        ],
        visualMap: {
          // type: 'piecewise', //定义映射为离散型
          top: 'middle',
          // left: 'right',
          right: "auto",
          min: 0,
          max: 100,
          dimension: dimension_index, //series.data的第几个维度被映射
          seriesIndex: 0, //对第几个系列进行映射
          inRange: {
            color: COLOR //定义映射颜色列表
          },
          categories: ['A', 'B', 'C', 'D']
        },
        xAxis: {
          scale: true,
          name: 'Lines of code',//x轴的名称
          nameLocation: 'middle',
          nameTextStyle: {
            padding: [20, 0, 0, 0]    // 四个数字分别为上右下左与原位置距离
          },
          splitLine: { //网格线显示是否
            show: true
          },
          axisTick: {  //刻度线
            "show": false
          },
        },
        yAxis: {
          scale: true,
          name: metric, //y轴的名称
          nameLocation: 'middle',
          nameTextStyle: {
            padding: [0, 0, 30, 0]    // 四个数字分别为上右下左与原位置距离
          },
          splitLine: {
            show: true
          },
          axisTick: {  //刻度线
            "show": false
          }
        },
        tooltip: {
          showDelay: 0,
          formatter: function (params) {
            const stylestr = '<span style="background-color:rgb(144,238,144);display: inline-block;width: 10px;height: 10px;border-radius: 50%;margin-right:2px;"></span>';
            if (params.value.length > 1) {
              return '<div>' + params.value[0] + '<br/>' + stylestr + 'lines of code:' + params.value[1] + '<br/>' + stylestr + metric + ':' + params.value[dimension_index - 1] + '<br/>' + '</div>';
            }
          }
        },
        series: [
          {
            type: 'scatter',
            datasetIndex: 0,
            encode: {
              x: 'loc',
              y: metric
            },
            symbolSize: function (data) {
              if (data[2] == 'A') {
                return 20
              } else if (data[2] == 'B') {
                return 15
              } else if (data[2] == 'C') {
                return 10
              }
              return 5
            },
            emphasis: {
              focus: 'self'
            },
            //  设置节点样式
            itemStyle: {
              normal: {
                label: {
                  color: '#000',
                  show: true,
                  position: 'middle',
                  fontWeight: 'bolder',
                  formatter: function (params, ticket, callback) {
                    console.log(ticket)
                    console.log(callback)
                    // if (name_index == 12) {
                    //   return params.data[13]
                    // }
                    return ''
                  },
                },
              }
            }
          }],
      };
      myChart.setOption(this.option);

      //   // 绑定事件之前先解绑，否则会多次触发
      //   myChart.off('mouseover')
      //   // 监听鼠标悬浮事件，若维度是microservice，选择指标后，悬浮到某节点上会高亮显示其相关的节点，其余置灰
      //   var currentpro_index = []
      //   myChart.on('mouseover', 'series', function (params) {
      //     if (params.data.length == 14) {
      //       // 高亮与当前节点属于同一项目的节点
      //       for (let i = 1; i < inputdata.allData.length; i++) {
      //         if (inputdata.allData[i][13] == params.data[13]) {
      //           currentpro_index.push(i - 1)
      //         }
      //       }
      //       console.log(currentpro_index)
      //       // 当前节点同一项目下的节点,高亮显示需要结合emphasis使用
      //       myChart.dispatchAction({
      //         type: 'highlight',
      //         seriesIndex: 0,
      //         dataIndex: currentpro_index
      //       });
      //     }
      //   }),
      //       myChart.on('mouseout', 'series', function (params) {
      //         if (params.data.length == 14) {
      //           // 取消之前高亮的图形
      //           myChart.dispatchAction({
      //             type: 'downplay',
      //             seriesIndex: 0,
      //             dataIndex: currentpro_index
      //           });
      //           currentpro_index = []
      //         }
      //       })
    }
  }
}
</script>

<style scoped>

</style>