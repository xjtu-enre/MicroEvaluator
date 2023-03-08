<template>
  <div>
    <div class="row mt-4">
      <div class="col-lg-5 col-md-6">
        <reports-radar-chart :radarData="metricdata['radardata']" :dim="dim"></reports-radar-chart>
      </div>
      <div class="col-lg-7 col-md-6">
        <transaction-card/>
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-lg-12 col-md-8 mt-5" v-for="(item, index) in metricdata['columndata']['columnValue']" :key="index">
        <chart-holder-card
            :title="metricdata['columndata']['indicator'][index]"
            color="success"
        >
          <reports-bar-chart
              :id="index"
              :chart="{
                  labels: metricdata['modules'],
                  datasets: {
                    label: metricdata['columndata']['indicator'][index],
                    data: item,
                  },
                }"
          />
        </chart-holder-card>
      </div>
    </div>
  </div>
</template>

<script>
// import MaterialButton from "../components/material/MaterialButton.vue";
// import TransactionCard from "../components/cards/TransactionCard";
// import InvoiceCard from "../components/cards/InvoiceCard";
// import DefaultProjectCard from "../components/cards/DefaultProjectCard.vue";
import ChartHolderCard from "../components/cards/ChartHolderCard.vue";
import ReportsBarChart from "../components/charts/ReportsBarChart.vue"
import ReportsRadarChart from "../components/charts/ReportsRadarChart.vue"
import TransactionCard from "../components/cards/TransactionCard.vue"
// import {getTreeData} from "../../api/project";

export default {
  name: "MetricDeatil",
  components: {
    // TransactionCard,
    // InvoiceCard,
    // MaterialButton,
    // DefaultProjectCard,
    ChartHolderCard,
    ReportsBarChart,
    ReportsRadarChart,
    TransactionCard
  },
  props: {
    version: String,
    dim: String,
    // indicatorData: Array,
    metricdata: Object,
  },
  data() {
    return {
      // isshow: false,
      // treedata: []
    }
  },
}
</script>

<style scoped>
</style>