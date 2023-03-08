<template>
  <div>
<!--    <select-card style="margin-bottom: 8px" :opts="opts" :optnames="optnames"></select-card>-->
<!--    <chart-holder-card title="Hot-Spots of Architecture Corruption" color="">-->
      <div id="hotmap" style="height: 200px"></div>
<!--    </chart-holder-card>-->
  </div>
</template>

<script>
import * as echarts from "echarts";
// import ChartHolderCard from "../cards/ChartHolderCard.vue";

export default {
  name: "HotMapComponent",
  mounted() {
    this.myChart = echarts.init(document.getElementById("hotmap"), 'macarons');
    this.setOption(this.mapdata)
  },
  props: {
    'mapdata': Array,
  },
  // components: {
  //   ChartHolderCard,
  //   SelectCard
  // },
  data() {
    return {
      myChart: "",
      option: [],
    };
  },
  watch: {
    mapdata() {
      this.$nextTick(() => {
        this.myChart = echarts.init(document.getElementById("hotmap"), 'macarons');
        this.setOption(this.mapdata)
      })
    }
  },
  methods: {
    setOption(mapdata) {
      console.log(mapdata)
      this.option = {
        title: {
          text: '',
        },
        tooltip: {
          position: 'top'
        },
        // grid: {
        //   height: '50%',//控制热力图纵向宽度占比
        //   top: '10%'//热力图距离上部百分比
        // },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 10
          },
          {
            start: 0,
            end: 10
          }
        ],
        xAxis: {
          type: 'category',
          data: mapdata[0],
          splitArea: {
            show: true
          },
          axisLabel: {
            // 坐标轴刻度标签的显示间隔
            interval: 1,
            // 标签倾斜的角度
            rotate: 25
          }
        },
        yAxis: {
          type: 'category',
          data: mapdata[1],
          splitArea: {
            show: true
          }
        },
        visualMap: {
          show: false,
          min: -1,
          max: 2,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%',
          inRange: {
            color: ['red', 'white']
          },
          outOfRange: {
            color: ['rgba(0, 0, 0, 0.5)']
          }
        },
        series: [
          {
            type: 'heatmap',
            data: mapdata[2],
            label: {
              normal: {
                show: true,
                formatter: function (params) {
                  console.log(params)
                  // if (params.data[2] == -1) {
                    return ''
                  // }
                }
              }
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 2,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.option && this.myChart.setOption(this.option);
      this.myChart.off('click');
      this.myChart.on('click',(params)=>{
        this.$emit('click-hot', params.name)
      })
    },
  }
}
</script>

<style scoped>

</style>
