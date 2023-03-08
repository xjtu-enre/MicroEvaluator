<template>
  <div
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="dashboard"
          navText="Dashboard"
        >
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5"></i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse
            :aria-controls="''"
            v-bind:collapse="false"
            collapseRef="ControlView"
            navText="Knowledge Base"
        >
<!--          <template v-slot:icon>-->
<!--            <i class="material-icons-round opacity-10 fs-5"></i>-->
<!--          </template>-->
        </sidenav-collapse>
      </li>
<!--      <li class="nav-item">-->
<!--        <sidenav-collapse-->
<!--          url="#"-->
<!--          :aria-controls="''"-->
<!--          v-bind:collapse="false"-->
<!--          collapseRef="sign-in"-->
<!--          navText="SignIn"-->
<!--        >-->
<!--          <template v-slot:icon>-->
<!--            <i class="material-icons-round opacity-10 fs-5"></i>-->
<!--          </template>-->
<!--        </sidenav-collapse>-->
<!--      </li>-->
<!--      <li class="nav-item">-->
<!--        <sidenav-collapse-->
<!--          url="#"-->
<!--          :aria-controls="''"-->
<!--          v-bind:collapse="false"-->
<!--          collapseRef="sign-up"-->
<!--          navText="SignUp"-->
<!--        >-->
<!--          <template v-slot:icon>-->
<!--            <i class="material-icons-round opacity-10 fs-5"></i>-->
<!--          </template>-->
<!--        </sidenav-collapse>-->
<!--      </li>-->
    </ul>
    <div class="sidenav-footer position-absolute w-100 bottom-0">
      <div class="mx-3">
        <a
          class="btn mt-4 w-100"
          :class="`bg-gradient-${this.$store.state.color}`"
          href="https://github.com/zyy20009619/MicroEvaluator"
          >Github</a
        >
      </div>
    </div>
<!--    href="https://www.creative-tim.com/product/vue-material-dashboard-2-pro"-->
  </div>
</template>
<script>
import SidenavCollapse from "./SidenavCollapse.vue";

export default {
  name: "SidenavList",
  props: {
    cardBg: String
  },
  data() {
    return {
      title: "Soft UI Dashboard PRO",
      controls: "dashboardsExamples",
      isActive: "active"
    };
  },
  components: {
    SidenavCollapse
  }
};
</script>
