<template>
  <div class="card z-index-2">
    <div
      class="card-header p-0 position-relative mt-n4 mx-3 z-index-2 bg-transparent"
    >
      <div
        class="border-radius-lg py-3 pe-1"
        :class="`bg-gradient-${color} shadow-${color}`"
      >
        <slot />
      </div>
    </div>
    <div class="card-body">
      <h6 class="mb-0">{{ title }}</h6>
<!--      <p class="text-sm" v-html="subtitle"></p>-->
<!--      <hr class="dark horizontal" />-->
<!--      <div class="d-flex" style="float: right" v-if="isScatter">-->

<!--&lt;!&ndash;        <i class="material-icons text-sm my-auto me-1">schedule</i>&ndash;&gt;-->
<!--&lt;!&ndash;        <p class="mb-0 text-sm">{{ update }}</p>&ndash;&gt;-->
<!--      </div>-->
    </div>
  </div>
</template>

<script>
export default {
  name: "ChartHolderCard",
  props: {
    title: {
      type: String,
      default: "",
    },
    // isScatter: {
    //   type: Boolean,
    //   default: false,
    // },
    // update: {
    //   type: String,
    //   default: "",
    // },
    color: {
      type: String,
      default: "primary",
    },
  },
};
</script>
