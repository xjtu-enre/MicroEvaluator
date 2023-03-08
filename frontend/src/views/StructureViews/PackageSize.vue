<template>
  <div>
    <div class="row">
      <div class="col-lg-12 col-md-6 mt-4">
        <div class="card card-body">
          <div id="chart" style="height: 1000px"></div>
        </div>
      </div>
      <!--      <div class="col-lg-2 col-md-6 mt-4">-->
      <!--        <div class="card card-body">-->
      <!--          <p-collapse title="包查询" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">-->
      <!--            <select id="file" name="file" v-model="file"-->
      <!--                    class="selectOpt" style="margin-top: 10px;margin-left: -20px;" @click="selectItem">-->
      <!--              <option value="isDefault">please select file</option>-->
      <!--              <option v-for="(item, index) in selectOptions" :key="index">-->
      <!--                {{ item.value }}-->
      <!--              </option>-->
      <!--            </select>-->
      <!--          </p-collapse>-->
      <!--        </div>-->
      <!--      </div>-->
      <div class="col-lg-2 col-md-6 mt-4">
        <div class="card card-body">
          <p-collapse title="包查询" headColor="#151515" bgColor="#fff" :isCollapse="false" style="color:black;">
            <select id="file" name="file" v-model="file"
                    class="selectOpt" style="margin-top: 10px;margin-left: -5px;" @click="selectItem">
              <option value="isDefault">please select file</option>
              <option v-for="(item, index) in selectOptions" :key="index">
                {{ item.value }}
              </option>
            </select>
          </p-collapse>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {selectCallback, drawChart} from '../../assets/js/heirarchy/treeMap';
import {getCatalogueTreeMapDatas} from "../../api/project";
// import PCollapse from "../components/panel/PCollapse";

export default {
  name: "PackageSize",
  // components: {PCollapse},
  watch: {
    selectedItem() {
      this.$nextTick(() => {
        console.log('hhhh')
        selectCallback(this.selectedItem);
      })
    }
  },
  created() {
    getCatalogueTreeMapDatas().then((res) => {
      if (res.data.code == 200) {
        this.selectOptions = drawChart(res.data.result[0]);
      }
    })
  },
  methods: {
    selectItem() {
      this.selectedItem = document.getElementById('file').value;
    },
    data() {
      return {
        selectOptions: [],
        selectedItem: "",
        activeKey: 1,
        allowClear: true,
        expandIconPosition: 'right',
        file: "isDefault"
      }
    }
  },
  data() {
    return {
      selectOptions: [],
      selectedItem: "",
      activeKey: 1,
      allowClear: true,
      expandIconPosition: 'right',
      file: "isDefault"
    }
  }
}
</script>

<style>
.panels {
  position: fixed !important;
  bottom: 0;
  right: -20px;
  width: 350px;
  /*max-height: calc(100vh - 2 * var(--stage-padding));*/
  overflow-y: auto;
  /*padding: var(--stage-padding);*/
  scrollbar-width: thin;
}
</style>