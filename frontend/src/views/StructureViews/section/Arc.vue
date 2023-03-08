<template>
  <div class="row">
    <div class="col-lg-10 col-md-6 mt-4">
      <div class="card card-body">
        <div id="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
  import { drawChart } from '../../../assets/js/section/arc';
  import {getSectionNodesList, getSectionEdgesList} from "../../../api/project";

  export default ({
    name: 'SectionArc',
    data() {
      return {
        nodeDatas: [],
        edgeDatas: [],
      }
    },
    watch: {
      edgeDatas() {
        this.$nextTick(() => {
          if (this.edgeDatas && this.nodeDatas){
            console.log(this.edgeDatas)
            console.log(this.nodeDatas)
            drawChart(this.nodeDatas, this.edgeDatas);
          }
        })
      }
    },
    created() {
      getSectionNodesList().then((res) => {
        this.nodeDatas = res.data.result;
      });
      getSectionEdgesList().then((res) => {
        this.edgeDatas = res.data.result;
      });
    }
  });
</script>

<style></style>
