<template>
  <div>
    <div
        class="page-header min-height-300 border-radius-xl mt-4"
        style="
        background-image: url('https://images.unsplash.com/photo-1531512073830-ba890ca4eba2?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
      "
    >
      <span class="mask bg-gradient-success opacity-6"></span>
    </div>
    <div class="card card-body mx-3 mx-md-4 mt-n6 mb-4">
      <div class="row gx-4">
        <div class="col-auto">
          <div class="avatar avatar-xl position-relative">
            <img
                src="@/assets/img/logos/java.png"
                alt="profile_image"
                class="shadow-sm w-100 border-radius-lg"
            />
          </div>
        </div>
        <div class="col-auto my-auto">
          <div class="h-100">
            <h5 class="mb-1">{{ projectname }}</h5>
            <p class="mb-0 font-weight-normal text-sm">{{ version }} / {{ loc }}</p>
          </div>
        </div>
        <div
            class="mx-auto mt-3 col-lg-6 col-md-6 my-sm-auto ms-sm-auto me-sm-0"
        >
          <dimension-navbar :dimensionNav="metricNav" @change-dimension="handleChangeDim"></dimension-navbar>
        </div>
      </div>
    </div>
    <metric-deatil :version="version" :dim="dim" :metricdata="metricdata"  v-if="isshow"></metric-deatil>
  </div>
</template>

<script>
import DimensionNavbar from "../Navbars/DimensionNavbar";
import MetricDeatil from "./MetricDeatil";
import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";
import {getMetricData} from "../../api/project";

export default {
  name: "profile-overview",
  data() {
    return {
      isshow: false,
      projectname: '',
      version: '',
      loc: 0,
      dim: '',
      alldata: [],
      metricNav: [],
      metricdata: [],
      showMenu: false,
    };
  },
  components: {
    MetricDeatil,
    DimensionNavbar,
    // DefaultProjectCard,
    // RadarChart,
  },
  created() {
    console.log('this.$route', this.$route.query)
    this.projectname = this.$route.query.projectname
    this.version = this.$route.query.version
    this.loc = this.$route.query.loc
    getMetricData().then((response) => {
      if (response.status == 200) {
        this.alldata = JSON.parse(response.data);
        this.metricNav = Object.keys(this.alldata)
        this.dim = this.metricNav[0]
        this.metricdata = this.alldata[this.dim]
        this.isshow = true
      }
    });
  },
  mounted() {
    this.$store.state.isAbsolute = true;
    setNavPills();
    setTooltip();
  },
  beforeUnmount() {
    this.$store.state.isAbsolute = false;
  },
  // watch: {
  //   dim(oldValue, newValue) {
  //     this.metricdata = this.alldata[newValue]
  //   }
  // },
  methods: {
    handleChangeDim(dimension){
      console.log('dim', dimension)
      this.dim = dimension
      this.metricdata = this.alldata[this.dim]
      console.log('this.metricdata', this.metricdata)
    }
  }
};
</script>
