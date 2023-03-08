<template>
  <div class="chart">
    <canvas id="line-chart" class="chart-canvas" height="100"></canvas>
  </div>
</template>
<script>
import Chart from "chart.js/auto";

export default {
  name: "ReportsLineChart",
  props: {
    linedata: Array
  },
  mounted() {
    var ctx = document.getElementById('line-chart').getContext("2d");
    let chartStatus = Chart.getChart('line-chart');
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }

    new Chart(ctx, {
      type: "line",
      data: {
        labels: this.linedata[0],
        datasets: [
          {
            label: 'score',
            data: this.linedata[1],
            fill: false,
            borderColor: '#009966', // 设置线的颜色
            tension: 0.1
          },
          {
            label: 'SMQ',
            data: this.linedata[2],
            fill: false,
            borderColor: '#66FF00', // 设置线的颜色
            tension: 0.1
          },{
            label: 'ODD',
            data: this.linedata[3],
            fill: false,
            borderColor: '#00CC33', // 设置线的颜色
            tension: 0.1
          },{
            label: 'IDD',
            data: this.linedata[4],
            fill: false,
            borderColor: '#66FF66', // 设置线的颜色
            tension: 0.1
          },{
            label: 'SPREAD',
            data: this.linedata[5],
            fill: false,
            borderColor: '#66FFCC', // 设置线的颜色
            tension: 0.1
          },{
            label: 'FOCUS',
            data: this.linedata[6],
            fill: false,
            borderColor: '#66CCCC', // 设置线的颜色
            tension: 0.1
          },{
            label: 'ICF',
            data: this.linedata[7],
            fill: false,
            borderColor: '#99FF99', // 设置线的颜色
            tension: 0.1
          },{
            label: 'ECF',
            data: this.linedata[8],
            fill: false,
            borderColor: '#00CC99', // 设置线的颜色
            tension: 0.1
          },{
            label: 'REI',
            data: this.linedata[9],
            fill: false,
            borderColor: '#33CCCC', // 设置线的颜色
            tension: 0.1
          }
          // ,{
          //   label: 'CHM',
          //   data: this.linedata[10],
          //   fill: false,
          //   borderColor: '#00FFFF', // 设置线的颜色
          //   tension: 0.1
          // },{
          //   label: 'CHD',
          //   data: this.linedata[11],
          //   fill: false,
          //   borderColor: '#99FFFF', // 设置线的颜色
          //   tension: 0.1
          // },
        ],
      },
    })
  }
};
</script>
