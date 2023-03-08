<template>
  <div class="row">
    <div class="col-md-8">
      <report-hot-map-chart></report-hot-map-chart>
    </div>
    <div class="col-md-4">
      <billing-card/>
    </div>
  </div>
</template>

<script>
import BillingCard from "../components/cards/BillingCard.vue";
import ReportHotMapChart from "../components/charts/ReportHotMapChart.vue";


export default {
  name: "HotMap",
  components: {
    BillingCard,
    ReportHotMapChart
  },
}
</script>

<style scoped>

</style>