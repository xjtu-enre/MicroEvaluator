<template>
  <div class="nav-wrapper position-relative end-0">
    <ul class="nav nav-pills nav-fill p-1" role="tablist">
      <li class="nav-item">
        <a
          class="nav-link mb-0 px-0 py-1 active active"
          data-bs-toggle="tab"
          role="tab"
          aria-selected="true"
          @click="goPackageSize"
          >PackageSize</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link mb-0 px-0 py-1"
          data-bs-toggle="tab"
          href="../../../examples/pages/account/billing.html"
          role="tab"
          aria-selected="false"
          @click="goSoftwareHierarchy"
          >SoftwareHierarchy</a
        >
      </li>
<!--      <li class="nav-item">-->
<!--        <a-->
<!--            class="nav-link mb-0 px-0 py-1"-->
<!--            data-bs-toggle="tab"-->
<!--            href="../../../examples/pages/account/billing.html"-->
<!--            role="tab"-->
<!--            aria-selected="false"-->
<!--            @click="goModuleCoupling"-->
<!--        >ModuleCoupling</a-->
<!--        >-->
<!--      </li>-->
    </ul>
  </div>
</template>

<script>
import setNavPills from "@/assets/js/nav-pills.js";

export default {
  name: "nav-strcuture",
  mounted() {
    setNavPills();
  },
  methods: {
    goPackageSize() {
      this.$router.push({
        'name': 'PackageSize'
      })
      this.$emit('tab-name', 'PackageSize')
    },
    goSoftwareHierarchy() {
      this.$router.push({
        'name': 'SoftwareHierarchy'
      })
      this.$emit('tab-name', 'SoftwareHierarchy')
    },
    goModuleCoupling() {
      this.$router.push({
        'name': 'ModuleCoupling'
      })
      this.$emit('tab-name', 'ModuleCoupling')
    }
  }
};
</script>
