<template>
  <div style="height: 450px">
    <div id="columnchart" style="height: 100%"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "dataShowComponent",
  props: {
    detailShowName: String,
    chartData: Array
  },
  created() {
    console.log(this.detailShowName)
    console.log(this.chartData)
  },
  data() {
    return {
      myChart: "",
      option: []
    };
  },
  // mounted只会在挂载的时候执行一次，故无法进行后续更新，此时使用watch进行图表的更新
  mounted() {
    this.myChart = echarts.init(document.getElementById("columnchart"));
    this.setOption()
  },
  watch: {
    chartData() {
      this.$nextTick(() => {
        if (this.chartData) {
          this.myChart = echarts.init(document.getElementById("columnchart"));
          this.setOption()
        }
      })
    }
  },
  methods: {
    setOption() {
      this.option = {
        dataset: [{
          source: this.chartData
        }
        ],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        toolbox: {
          feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        grid: {
          bottom: '25%'
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 30
          },
          {
            start: 0,
            end: 30
          }
        ],
        xAxis: [
          {
            type: 'category',
            axisLabel: {
              // 坐标轴刻度标签的显示间隔(在类目轴中有效哦)
              interval: 0,
              // 标签倾斜的角度
              rotate: 35
            }
          }
        ],
        yAxis: [
          {
            name: this.detailShowName,
          }
        ],
        series: [
          {
            name: this.detailShowName,
            type: 'bar',
            datasetIndex: 0,
            encode: {
              x: 'module',
              y: this.detailShowName
            }
          }
        ]
      }
      this.option && this.myChart.setOption(this.option);
    }
  },
};
</script>

<style scoped>
</style>
