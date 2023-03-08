<template>
  <div class="card">
    <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
      <div
          class="bg-gradient-success shadow-success border-radius-lg pt-4 pb-3"
      >
        <h6 class="text-white text-capitalize ps-3">Quality Distribution of Population</h6>
      </div>
    </div>
    <div class="card-body">
      <canvas id="scatter-chart" class="chart-canvas" height="100"></canvas>
      <!--      <select-card style="margin-bottom: 10px;" @change-opt2="handleChangeMetric"-->
      <!--                   :opts="metrics"-->
      <!--                   :optnames="optnames"></select-card>-->
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "ReportsScatterChart",
  props: {
    scatterData: Array,
    projectname: Array
  },
  mounted() {
    var ctx = document.getElementById('scatter-chart').getContext("2d");
    let chartStatus = Chart.getChart('scatter-chart');
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }

    new Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [{
          label: 'score',
          data: this.scatterData,
          backgroundColor: 'rgb(255, 99, 132)'
        }]
      },
      options: {
        tooltips: {
          callbacks: {
            label: function(t, d) {
              console.log(t)
              console.log(d)
             return 'label'
            }
          }
        }
      }
    })
  }
}
</script>

<style scoped>

</style>