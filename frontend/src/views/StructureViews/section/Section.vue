<template>
  <div class="row">
    <div class="col-lg-12 col-md-6 mt-4">
      <div class="card card-body">
        <div id="chart" style="height: 768px"></div>
      </div>
    </div>
  </div>
</template>

<script>
import {drawChart} from '../../../assets/js/section/section';
import {getSectionEdgesList, getSectionNodesList} from "../../../api/project";

export default ({
  name: 'SectionD3Chart',
  props: {
    nodes: {
      type: Object,
    },
    edges: {
      type: Object,
    },
  },
  data() {
    return {
      nodeDatas: [],
      edgeDatas: [],
    }
  },
  created() {
    getSectionNodesList().then((res) => {
      this.nodeDatas = res.data.result;
    });
    getSectionEdgesList().then((res) => {
      this.edgeDatas = res.data.result;
    });
  },
  watch: {
    edgeDatas() {
      this.$nextTick(() => {
        if (this.edgeDatas && this.nodeDatas) {
          drawChart(this.nodeDatas, this.edgeDatas);
          ;
        }
      })
    }
  }
});
</script>

<style></style>
