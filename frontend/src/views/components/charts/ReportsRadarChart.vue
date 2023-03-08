<template>
  <div class="card my-4">
    <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
      <div
          class="bg-gradient-success shadow-success border-radius-lg pt-4 pb-3"
      >
        <h6 class="text-white text-capitalize ps-3">Quality Distribution in Module-Level</h6>
      </div>
    </div>
    <div class="card-body px-0 pb-2">
      <canvas id="radar-chart" class="chart-canvas" height="310"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "ReportsRadarChart",
  props:{
    radarData: Object,
    dim: String,
    // indicatorData: Array
  },
  watch: {
    dim(oldValue, newValue) {
      console.log(newValue)
      var ctx = document.getElementById('radar-chart').getContext("2d");
      let chartStatus = Chart.getChart('radar-chart');
      if (chartStatus != undefined) {
        chartStatus.destroy();
      }

      new Chart(ctx, {
        type: 'radar',
        data: {
          labels: this.radarData['indicator'],
          datasets: [{
            label: this.dim,
            data: this.radarData['radarValue'],
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
          }]
        },
        options: {
          responsive: true, // 设置图表为响应式，根据屏幕窗口变化而变化
          maintainAspectRatio: false,// 保持图表原有比例
          elements: {
            line: {
              borderWidth: 3 // 设置线条宽度
            }
          }
        }
      });
    }
  },
  mounted() {
    debugger
    var ctx = document.getElementById('radar-chart').getContext("2d");
    let chartStatus = Chart.getChart('radar-chart');
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }

    new Chart(ctx, {
      type: 'radar',
      data: {
        labels: this.radarData['indicator'],
        datasets: [{
          label: this.dim,
          data: this.radarData['radarValue'],
          fill: true,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgb(255, 99, 132)',
          pointBackgroundColor: 'rgb(255, 99, 132)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(255, 99, 132)'
        }]
      },
      options: {
        responsive: true, // 设置图表为响应式，根据屏幕窗口变化而变化
        maintainAspectRatio: false,// 保持图表原有比例
        elements: {
          line: {
            borderWidth: 3 // 设置线条宽度
          }
        }
      }
    });
  }
}
</script>

<style scoped>

</style>