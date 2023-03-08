<template>
  <div>
    <div id="linechart" style="height: 400px"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: "LineChartComponent",
  props: {
    'linedata': Array,
    'projectname': String
  },
  data() {
    return {
      myChart: "",
      option: []
    }
  },
  // mounted只会在挂载的时候执行一次，故无法进行后续更新，此时使用watch进行图表的更新
  mounted() {
    this.myChart = echarts.init(document.getElementById("linechart"), 'macarons');
    this.setOption()
  },
  watch: {
    linedata() {
      this.$nextTick(() => {
        if (this.linedata) {
          this.myChart = echarts.init(document.getElementById("linechart"), 'macarons');
          this.setOption()
        }
      })
    }
  },
  methods: {
    setOption() {
      this.option = {
        dataset: [{
          source: this.linedata
        }],
        title: {
          text: this.projectname,
          left: '1%'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {},
        toolbox: {
          show: true,
          feature: {
            // dataZoom: {
            //   yAxisIndex: 'none'
            // },
            dataView: {readOnly: false},
            magicType: {type: ['line', 'bar']},
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
        },
        yAxis: {},
        series: [
          // {
          //   name: 'IFN',
          //   type: 'line',
          //   datasetIndex: 0,
          //   encode: {
          //     x: 'version',
          //     y: 'IFN'
          //   },
          // },
          // {
          //   name: 'CHM',
          //   type: 'line',
          //   datasetIndex: 0,
          //   encode: {
          //     x: 'version',
          //     y: 'CHM'
          //   },
          // }, {
          //   name: 'CHD',
          //   type: 'line',
          //   datasetIndex: 0,
          //   encode: {
          //     x: 'version',
          //     y: 'CHD'
          //   },
          {
            name: 'SMQ',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'SMQ'
            },
          },
          // {
          //   name: 'CMQ',
          //   type: 'line',
          //   datasetIndex: 0,
          //   encode: {
          //     x: 'version',
          //     y: 'CMQ'
          //   },
          // },
          {
            name: 'ICF',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'ICF'
            },
          }, {
            name: 'ECF',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'ECF'
            }
          }, {
            name: 'REI',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'REI'
            }
          }, {
            name: 'SPREAD',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'SPREAD'
            }
          }, {
            name: 'FOCUS',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'FOCUS'
            }
          }, {
            name: 'score',
            type: 'line',
            datasetIndex: 0,
            encode: {
              x: 'version',
              y: 'score'
            }
          }
        ]
      };
      this.myChart.setOption(this.option);
    }
  }
}
</script>

<style scoped>
</style>
