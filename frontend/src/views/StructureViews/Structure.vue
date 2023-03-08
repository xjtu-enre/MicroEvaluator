<template>
  <div class="container-fluid mt-4">
    <div class="row align-items-center">
      <div class="col-lg-4">
        <nav-structure @tab-name="changeTab"/>
      </div>
    </div>
    <div>
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavStructure from "../Navbars/StructureNavbar.vue";

export default {
  name: "Structure",
  components: {
    NavStructure
  },
  data() {
    return {
      toName: {}
    }
  },
  methods: {
    changeTab(tabName) {
      this.$router.push({
        name: tabName
      })
    },
  },
  created() {
    this.$router.push({
      name: 'PackageSize',
    })
  },
};
</script>
