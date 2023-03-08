<template>
  <div>
    <div class="card card-body mt-4">
      <div class="col-auto my-auto">
        <div class="h-100">
          <h5 class="mb-1">Module Coupling</h5>
        </div>
      </div>
      <div
          class="mx-auto mt-3 col-lg-4 col-md-6 my-sm-auto ms-sm-auto me-sm-0"
      >
        <dimension-navbar :dimension-nav="categoryNav" @change-dimension="changeDimension"></dimension-navbar>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import DimensionNavbar from "../Navbars/DimensionNavbar";

export default {
  name: "ModuleCoupling",
  components: {
    DimensionNavbar,
  },
  data() {
    return {
      // categoryNav: ['SunBurst', 'Chord', 'Section']
      categoryNav: ['SunBurst', 'Chord']
    }
  },
  created() {
    this.$router.push({
      name: 'SunBurst',
    })
  },
  methods: {
    changeDimension(dimension) {
      this.$router.push({
        name: dimension
      })
    }
  }
}
</script>

<style scoped>

</style>