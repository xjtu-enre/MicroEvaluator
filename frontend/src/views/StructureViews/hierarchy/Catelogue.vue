<template>
  <div>
    <div class="row">
<!--      <div class="col-lg-4 col-md-4 mt-4">-->
<!--        <div class="card card-body" style="padding: 30px">-->
<!--          <div id="mchart"></div>-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="col-lg-3 col-md-6 mt-4">-->
<!--        <div class="card card-body">-->
<!--          <p-collapse title="图例" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">-->
<!--            <div id="legend"></div>-->
<!--          </p-collapse>-->
<!--          <p-collapse title="包查询" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">-->
<!--            <select name="file" v-model="file"-->
<!--                    class="selectOpt" style="margin-top: 10px;margin-left: -20px">-->
<!--              <option value="isDefault">please select file</option>-->
<!--              <option v-for="(item, index) in treemapdata" :key="index">-->
<!--                {{ item }}-->
<!--              </option>-->
<!--            </select>-->
<!--          </p-collapse>-->
<!--        </div>-->
<!--      </div>-->
      <div class="col-lg-6 col-md-6 mt-4">
        <div class="card card-body">
          <div id="schart"></div>
        </div>
      </div>
      <div class="col-lg-6 col-md-6 mt-4">
        <div class="card card-body">
          <p-collapse title="change frequency" headColor="#151515" bgColor="#fff" isCollapse="true" style="color:black;">
            <div id="slegend" style="margin-top: 20px"></div>
          </p-collapse>
          <!--          <p-collapse title="描述" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">tttt</p-collapse>-->
<!--          <p-collapse title="文件查询" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">-->
<!--            <select name="file" v-model="file"-->
<!--                    class="selectOpt" style="margin-top: 10px;margin-left: -20px">-->
<!--              <option value="isDefault">please select file</option>-->
<!--              <option v-for="(item, index) in fileData[0]" :key="index">-->
<!--                {{ item.value }}-->
<!--              </option>-->
<!--            </select>-->
<!--          </p-collapse>-->
          <p-collapse title="Clusters" headColor="#151515" bgColor="#fff" :isCollapse="true" style="color:black;">
            <div id="clusters" style="width: 310px; height: 260px"></div>
          </p-collapse>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getCatalogueDatasList, getCatalogueTreeMapDatas} from "../../../api/project";
import {drawsChart, drawRootClusters, getData, drawLegend, drawNodeClusters} from "../../../assets/js/heirarchy/sCirclePack";
import PCollapse from "../../components/panel/PCollapse";
import {drawmChart, drawmLegend} from "../../../assets/js/heirarchy/mCirclePack";

export default {
  name: "Catelogue",
  components: {PCollapse},
  data() {
    return {
      // replaceFields: {
      //   children: 'children',
      //   key: 'id',
      //   title: 'name',
      //   value: 'qualifiedName',
      // },
      // selectedItem: "",
      // selectOptions: [],
      file: "isDefault",
      node1: {},
      node2: {},
      activeKey: '1',
      allowClear: true,
      expandIconPosition: 'right',
      catelogueData: [],
      treeData: [],
      fileData: [],
      treemapdata: [],
      panels: ['图例', '描述', '文件查询', 'Clusters']
    }
  },
  created() {
    getCatalogueDatasList().then((res) => {
      console.log('getCatalogueDatasList', res)
      if (res.data.code == 200) {
        this.catelogueData = res.data.result[0];
      }
    }),
    getCatalogueTreeMapDatas().then((res) => {
      this.treeData = res.data.result[0];
    });
  },
  watch: {
    node1() {
      console.log(this.node1)
      this.$nextTick(() => {
        if (this.node1.value.height === 1) {
          drawNodeClusters(this.node1.value);
        } else if (this.node1.value.height === 2) {
          drawRootClusters(this.catelogueData);
        }
      })
    },
    catelogueData(){
      console.log('catelogueData')
      this.$nextTick(() => {
        this.fileData = getData(this.catelogueData);
        drawLegend();
        drawRootClusters(this.catelogueData);
        drawsChart(this.catelogueData, this.node1);
      })
    },
    treeData(){
      drawmLegend();
      this.treemapdata = drawmChart(this.treeData, this.node2);
    }
  },
}
</script>

<style scoped>
</style>