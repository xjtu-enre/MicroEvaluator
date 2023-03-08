<template>
  <div class="container-fluid py-4">
    <div class="row mb-4">
      <div class="col-lg-12 position-relative z-index-2">
        <div class="row">
          <div class="col-lg-3 col-md-6">
            <mini-statistics-card
                detail="<span class='text-success text-sm font-weight-bolder'>0.0145%(1/69)</span> of all projects"
                :title="{ text: 'My Projects', value: '1' }"
                :icon="{
              name: 'Pro',
              color: 'text-white',
              background: 'dark',
            }"
            />

            <div class="mt-5">
              <mini-statistics-card
                  :title="{ text: 'Average Score', value: '0.6481' }"
              :icon="{
              name: 'Score',
              color: 'text-white',
              background: 'primary',
            }"
              />
            </div>
            <div class="mt-5">
              <mini-statistics-card
                  :title="{ text: 'Average Loc', value: '107010' }"
                  :icon="{
              name: 'Loc',
              color: 'text-white',
              background: 'success',
            }"
              />
            </div>
          </div>
          <div class="col-lg-9 col-md-8">
            <reports-scatter-chart :scatterData="scatterData" :projectname="projectName" v-if="isShow"></reports-scatter-chart>
<!--            <scatter-chart :scatterData="scatterData" :metrics="metrics" :optnames="optnames" v-if="isShow"/>-->
          </div>
<!--          <div class="col-lg-4 col-md-6">-->
<!--            <bar-chart :maxcount="maxcount" :bardata="barData"/>-->
<!--          </div>-->
        </div>
      </div>
    </div>
    <div class="row justify-content-md-center">
      <div class="col-lg-12" v-if="isloading">
        <project-card
            :projects="projectData"
            @projects-refresh="refreshProject"
        />
      </div>
    </div>
  </div>
</template>
<script>
// import BarChart from "./components/charts/BarChart.vue";
// import ScatterChart from "./components/charts/ScatterChart.vue";
import ReportsScatterChart from "./components/charts/ReportsScatterChart.vue";
import ProjectCard from "./components/cards/ProjectCard.vue";
import MiniStatisticsCard from "./components/cards/MiniStatisticsCard.vue";
import {getCurentProject, getCurentProjectMetricData} from "../api/project"

export default {
  name: "dashboard-default",
  created() {
    this.refreshProject()
    this.getAllProjectMetricData()
    // this.getAllModuleMetricData()
  },
  data() {
    return {
      isShow: false,
      isloading: false,
      projectData: [],
      count: 0,
      maxcount: 100,
      barData: [['high ifn', 'low chm', 'low chd', 'low icf', 'high ecf', 'low scoh', 'high scop', 'low ccoh', 'high ccop', 'small number of modules'], [20, 20, 20, 20, 20, 20, 20, 20, 20]],
      scatterData:[],
      projectName:[],
        //   [['loc', 'loc_level', 'score', 'score_level', 'IFN', 'IFN_level', 'CHM', 'CHM_level', 'CHD', 'CHD_level', 'ICF',
        // 'ICF_level', 'ECF', 'ECF_level', 'ifn', 'ifn_level', 'chm', 'chm_level', 'chd', 'chd_level', 'projectname',
        // 'projectindex'], [10000, 'A', 0.2, 'A', 0.3, 'A', 0.4, 'A', 0.5,
        // 'A', 0.6, 'A', 0.7, 'A', 0.8, 'A', 0.9, 'A', 0.1, 'A', 'test',
        // 0], [5000, 'A', 0.2, 'B', 0.3, 'A', 0.4, 'A', 0.5,
        // 'A', 0.6, 'A', 0.7, 'A', 0.8, 'A', 0.9, 'A', 0.1, 'A', 'test11',
        // 0], [5000, 'A', 0.2, 'C', 0.3, 'A', 0.4, 'A', 0.5,
        // 'A', 0.6, 'A', 0.7, 'A', 0.8, 'A', 0.9, 'A', 0.1, 'A', 'test22',
        // 0]],
      metrics: [],
      optnames: ['dimension', 'metric']
    };
  },
  components: {
    // BarChart,
    MiniStatisticsCard,
    // ScatterChart,
    ProjectCard,
    ReportsScatterChart
  },
  methods: {
    // 查询当前用户下所有项目信息(之后要加上用户筛选)
    refreshProject() {
      getCurentProject().then((response) => {
        if (response.data.code == 200) {
          this.projectData = response.data.result;
          this.count = this.projectData.length
          this.isloading = true
        }
      });
    },
    // 查询score信息
    getAllProjectMetricData() {
      getCurentProjectMetricData().then((response) => {
        if (response.status == 200) {
          var data = JSON.parse(response.data);
          this.scatterData = data.scatterdata
          this.projectName = data.projectname
          console.log('data.scatterdata', data.scatterdata)
          console.log(data.metrics)
          this.metrics = data.metrics
          this.isShow = true
        }
      });
    },
  }
};
</script>
