<template>
  <div id="radar" style="height: 320px"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: "RadarComponent",
  props: {
    radarData: Array,
    indicatorData: Array,
  },
  mounted() {
    this.drawRadar();
  },
  data() {
    return {
      myChart: "",
      option: []
    };
  },
  watch: {
    indicatorData() {
      this.$nextTick(() => {
        this.drawRadar();
      })
    }
  },
  methods: {
    drawRadar() {
      // 初始化echarts实例
      var myChart = echarts.init(document.getElementById("radar"), 'macarons');
      var option;
      option = {
        title: {
          text: ''
        },
        // legend: {
        //   data: this.planNum,
        //   left: '0',
        //   top: '10%'
        // },
        radar: {
          indicator: this.indicatorData,
          center: ['50%', '50%'],
          radius: 120,
          startAngle: 90,
          splitNumber: 4,
          shape: 'circle',
          axisName: {
            formatter: '【{value}】',
            color: '#428BD4'
          },
          splitArea: {
            areaStyle: {
              color: ['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
              shadowColor: 'rgba(0, 0, 0, 0.2)',
              shadowBlur: 10
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(211, 253, 250, 0.8)'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(211, 253, 250, 0.8)'
            }
          }
        },
        grid: {
          top: '20%'
        },
        series: [
          {
            type: 'radar',
            data: this.radarData,
            emphasis: {
              lineStyle: {
                width: 4
              }
            },
            label: {
              normal: {
                show: true,
                formatter:function(params) {
                  return params.value;
                }
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    }
  }
}
</script>

<style scoped>

</style>
