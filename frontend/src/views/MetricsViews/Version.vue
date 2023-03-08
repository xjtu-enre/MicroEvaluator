<template>
  <div class="container-fluid py-4">
    <div class="row mb-4">
      <div class="row mb-4" v-if="isexpand">
        <div class="col-lg-12 mt-4">
          <div class="card">
          <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
            <div
                class="bg-gradient-danger shadow-danger border-radius-lg pt-4 pb-3"
            >
              <h6 class="text-white text-capitalize ps-3">Hotspot Display</h6>
            </div>
          </div>
          <div class="card-body">
            <!--          <report-hot-map-chart></report-hot-map-chart>-->
            <hot-map-chart :mapdata="mapdata" :optnames="optnames" :opts="opts" @click-hot="identifyCause"></hot-map-chart>
            <billing-card :visable="visible" @visible-change="changeVisable"></billing-card>
          </div>
          </div>
        </div>
      </div>
      <div class="col-lg-12 mt-4">
        <div class="card mt-4">
          <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
            <div
                class="bg-gradient-success shadow-success border-radius-lg pt-4 pb-3"
            >
              <h6 class="text-white text-capitalize ps-3">Quality Change Curve</h6>
            </div>
          </div>
          <div class="card-body">
            <div style="float: right;margin-top: 20px">
              <material-button color="success" size="sm" variant="outline" @click="hotspotDispaly"
              >View Hotspot</material-button
              >
            </div>
            <div class="col-12" v-if="isshow">
              <reports-line-chart :linedata="linedata"></reports-line-chart>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12" v-if="isloading">
        <version-project-card :versiondata="versiondata" :projectname="projectname"></version-project-card>
      </div>
    </div>
  </div>
</template>

<script>
import {getLineData, getVersionData, getHotMapData} from "../../api/project";
// import ChartHolderCard from "../components/cards/ChartHolderCard.vue";
// import LineChart from "../components/charts/LineChart";
import ReportsLineChart from "../components/charts/ReportsLineChart";
// import InvoiceCard from "../components/cards/InvoiceCard.vue";
import HotMapChart from "../components/charts/HotMapChart";
// import ReportHotMapChart from "../components/charts/ReportHotMapChart";
import VersionProjectCard from "../components/cards/VersionProjectCard";
import BillingCard from "../components/cards/BillingCard";
import MaterialButton from "../components/material/MaterialButton.vue";

export default {
  name: "tables",
  components: {
    // ChartHolderCard,
    // LineChart,
    // InvoiceCard,
    ReportsLineChart,
    HotMapChart,
    BillingCard,
    // ReportHotMapChart,
    VersionProjectCard,
    MaterialButton
  },
  data() {
    return {
      visible: false,
      isexpand: false,
      versiondata: [],
      isloading: false,
      isshow: false,
      linedata: [],
      //     ['version', 'score', 'SMQ', 'ODD', 'IDD', 'SPREAD', 'FOUCUS', 'ICF', 'ECF', 'REI', 'CHM', 'CHD'],
      //   ['v1', 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0.8],
      //   ['v2', 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0.8]
      // ],
      // mapdata: [['a', 'b', 'c', 'd', 'e', 'f'], ['ifn', 'chm'], [[0, 0, 1], [0, 1, 0.8], [0, 2, 0.5], [0, 3, 0.2], [0, 4, 0.5], [0, 5, 0.2]]],
      mapdata: [],
      optnames: ['Origin', 'End'],
      opts: [{
        'opt1': 'v1',
        'opt2': ['v2', 'v3', 'v4']
      }, {
        'opt1': 'v2',
        'opt2': ['v3', 'v4']
      }, {
        'opt1': 'v3',
        'opt2': ['v4']
      }],
      projectname: ''
    }
  },
  created() {
    getVersionData(this.$route.query.projectid).then((response) => {
      if (response.data.code == 200) {
        this.versiondata = response.data.result;
        this.projectname = this.$route.query.projectname
        this.isloading = true
      }
    });
    getLineData().then((response) => {
      debugger
      if (response.status == 200) {
        debugger
        var data = JSON.parse(response.data);
        this.linedata = data.linedata
        // this.mapdata = data.hotmapdata
        this.isshow = true
      }
    });
  },
  methods: {
    identifyCause() {
      console.log('visible', this.visible)
      this.visible = !this.visible
      console.log('visible1', this.visible)
    },
    changeVisable() {
      this.visible = false
    },
    hotspotDispaly(){
      getHotMapData().then((response) => {
        if (response.status == 200) {
          var data = JSON.parse(response.data);
          this.mapdata = data.hotmapdata
          this.isexpand = true
        }
      });
    }
  }
};
</script>
<style scoped lang="scss">

.dialog-wrap {
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.418);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 122;
}

.dialog-body {
  background-color: #fff;
  border-radius: 20px;
  left: 50%;
  top: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
  width: 30%
}
</style>