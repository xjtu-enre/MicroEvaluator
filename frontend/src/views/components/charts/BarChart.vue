<template>
  <chart-holder-card
      title="Proportion of risk causes"
      color=""
  >
    <div id="barchart" style="height: 485px;"></div>
  </chart-holder-card>
</template>

<script>
import * as echarts from 'echarts';
import ChartHolderCard from "../cards/ChartHolderCard.vue";

export default {
  name: "barComponent",
  components: {
    ChartHolderCard,
  },
  props: {
    bardata: Array,
    maxcount: Number,
  },
  mounted() {
    this.drawPieChart(this.bardata[0], this.bardata[1], this.maxcount);
  },
  watch: {
    countdata() {
      this.$nextTick(() => {
        this.drawPieChart(this.bardata[0], this.bardata[1], this.maxcount);
      })
    }
  },
  methods: {
    drawPieChart(metrics, countdata, maxcount) {
      var myChart = echarts.init(document.getElementById("barchart"), 'macarons');
      var option;
      // const reasons = ['功能内聚', '演化历史', '结构依赖', '语义依赖', '项目特征']
      option = {
        title: {
          text: '',
          left: 'center'
        },
        // legend: {
        //   show: true,
        //   top: 'bottom',
        //   data: reasons
        // },
        angleAxis: {
          type: 'category',
          data: metrics
        },
        tooltip: {
          formatter: function (params) {
            const id = params.dataIndex;
            return (
                metrics[id] +
                '<br>count：' +
                countdata[id] +
                '<br>sum：' +
                maxcount +
                '<br>ratio：' +
                ((countdata[id] / maxcount) * 100).toFixed(2) + '%'
            );
          }
        },
        radiusAxis: {
          max: maxcount
        },
        grid: {
          top: 100
        },
        polar: {
          center: ['50%', '50%']
        },
        series: [
          {
            type: 'bar',
            data: countdata,
            coordinateSystem: 'polar',
          }
        ]
      };
      if (option && typeof option === 'object') {
        myChart.setOption(option);
      }

    }
  }
}
</script>

<style scoped>

</style>
