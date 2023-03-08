<template>
  <div class="Collapse" :style="{ backgroundColor: bgColor, width: width }">
    <div class="CollapseHead" :style="{
        color: headColor,
        borderLeftColor: borderColor,
      }" @click="collapse = !collapse">
      <span>{{ title }}</span>
      <span style="float: right">
        <i v-if="collapse" class="el-icon-arrow-down"></i>
        <i v-else class="el-icon-arrow-right"></i>
      </span>
    </div>
    <collapseTransition>
      <div v-if="collapse">
        <slot></slot>
      </div>
    </collapseTransition>

  </div>
</template>

<script>
import CollapseTransition from './PCollapse'
export default {
  name: "Collapse",
  components: {
    CollapseTransition
  },
  props: {
    title: {
      type: String,
      default: "标题",
    },
    headColor: {
      type: String,
      default: "green",
    },
    borderColor: {
      type: String,
      default: "green",
    },
    bgColor: {
      type: String,
      default: "rgba(41, 41, 41, 0.589)", //浅黑
    },
    width: {
      type: String,
      default: "100%",
    },
    isCollapse: {
      type: Boolean,
      default: true,
    },
  },
  data () {
    return {
      collapse: this.isCollapse,
    };
  },
  computed: {},
  created () { },
  mounted () { },
  filters: {},
  methods: {},
  watch: {},
};
</script>

<style  scoped>
.Collapse {
  margin: 10px 0;
  color: white;
  background-color: rgba(41, 41, 41, 0.589);
  padding: 10px;
}
.CollapseHead {
  line-height: 25px;
  border-left: 3px solid;
  font-weight: bold;
  padding-left: 10px;
  font-size: 15px;
  caret-color: transparent;
}
.el-icon-arrow-down {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-top: 2px solid forestgreen;
  border-right: 2px solid forestgreen;
  transform: rotate(135deg);
  transition: all ease .1s;
}
.el-icon-arrow-right {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-top: 2px solid forestgreen;
  border-right: 2px solid forestgreen;
  transform: rotate(45deg);
  transition: all ease .1s;
}
</style>
