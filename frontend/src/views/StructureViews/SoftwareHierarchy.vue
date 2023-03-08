<template>
  <div>
    <div class="card card-body mt-1">
      <div class="row">
        <div class="col-lg-4 mt-3">
          <h5 class="mb-1">Software Hierarchy</h5>
        </div>
        <div
            class="mx-auto mt-3 col-lg-4 col-md-6 my-sm-auto ms-sm-auto me-sm-0"
        >
          <dimension-navbar :dimension-nav="categoryNav" @change-dimension="changeDimension"></dimension-navbar>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import DimensionNavbar from "../Navbars/DimensionNavbar";

export default {
  name: "SoftwareHierarchy",
  components: {
    DimensionNavbar,
  },
  data() {
    return {
      categoryNav: ['Catelogue', 'Cluster']
    }
  },
  created() {
    this.$router.push({
      name: 'Cluster',
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