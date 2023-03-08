<template>
  <div class="dialog-wrap" v-if="visable">
    <div class="dialog-body">
      <div class="card">
        <div class="card-header pb-0 px-3">
          <h6 class="mb-0">Root Cause</h6>
        </div>
        <div class="card-body pt-4 p-3">
          <ul class="list-group">
            <li
                class="list-group-item border-0 d-flex p-4 mb-2 mt-3 bg-gray-100 border-radius-lg" v-for="(item,index) in showData" :key="index">
              <div class="d-flex flex-column">
                <h6 class="mb-3 text-sm">{{ item.type }}</h6>
                <div id="scrollbar" style="background-color: '#F2F2F2'">
                  <a-tree
                      :expanded-keys="iExpandedKeys"
                      :auto-expand-parent="autoExpandParent"
                      :tree-data="item.entities"
                      @expand="onExpand"
                      :replace-fields="{children:'children', key:'id', value: 'id', title: 'label'}"
                  >
                  </a-tree>
                </div>
              </div>
            </li>
          </ul>
          <div style="width: 40%;margin: auto;">
            <material-button
                class="mt-4"
                variant="gradient"
                color="success"
                fullWidth
                size="lg"
                @click="cancel"
            >Cancel
            </material-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MaterialButton from "../material/MaterialButton.vue";
import {getCauseEntitiesData} from "../../../api/project";

export default {
  name: "billing-card",
  props: {
    visable: {  // 数据显示隐藏
      type: Boolean,
      default: false,
    }
  },
  components: {
    MaterialButton,
  },
  data() {
    return {
      showData: [],
      defaultData: [],
      expandedKeys: [],
      searchVal: "",
      searchValue: "",
      iExpandedKeys: [],
      autoExpandParent: false,
      testData: []
    }
  },
  created() {
    this.getTreeData();
  },
  methods: {
    cancel(e) {
      console.log(e)
      this.$emit('visible-change')
    },

    getTreeData() {
      // debugger
      // this.defaultData = [];
      // for (let i = 0; i < this.testdata.length; i++) {
      //   console.log(this.testdata)
      //   let temp = this.testdata[i]
      //   this.defaultData.push(JSON.parse(JSON.stringify(temp)))
      //   this.showData = [...this.defaultData];
      //   this.recursionData(this.defaultData);//将每一层数据都赋上title的slot,以高亮显示搜索字段
      //   // this.setThisExpandedKeys(temp)
      //   // console.log(temp.id)
      // }
      // 调用获取数据的接口
      getCauseEntitiesData().then((res) => {
        if (res.status == 200) {
          var data = JSON.parse(res.data);
          console.log(data['causes'])
          this.showData = data.causes
        }
      })
    }
    // ,
    // recursionData(node) {
    //   node.forEach(item => {
    //     item.scopedSlots = {title: 'label'}
    //     if (item.children && item.children.length) {
    //       this.recursionData(item.children)
    //     }
    //   })
    // }
    // ,
    // setThisExpandedKeys(node) {
    //   //只展开一级目录
    //   if (node.children && node.children.length > 0) {
    //     this.iExpandedKeys.push(node.id)
    //     //下方代码放开注释则默认展开所有节点
    //
    //     // for (let a = 0; a < node.children.length; a++) {
    //     //   this.setThisExpandedKeys(node.children[a])
    //     // }
    //   }
    // }
    ,
    onExpand(expandedKeys) {
      this.iExpandedKeys = expandedKeys
      this.autoExpandParent = false
    }
  }
};
</script>
<style scoped lang="scss">

.dialog-wrap {
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.418);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 122;
}

.dialog-body {
  background-color: #fff;
  border-radius: 20px;
  left: 50%;
  top: 10%;
  height: 100px;
  position: absolute;
  transform: translate(-50%, -50%);
  width: 55%
}

#scrollbar {
  height: 120px;
  //width: 80%;
  overflow-y: auto
}
</style>

