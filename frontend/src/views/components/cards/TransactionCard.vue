<template>
  <div class="card h-98 mb-4">
    <div class="card-header pb-0 px-3">
      <div class="row">
        <div class="col-md-6">
          <h6 class="mb-0">Class-level and Method-level Results</h6>
        </div>
        <!--        <div class="col-md-6 d-flex justify-content-end align-items-center">-->
        <!--          <i class="far fa-calendar-alt me-2" aria-hidden="true"></i>-->
        <!--          <small>23 - 30 March 2020</small>-->
        <!--        </div>-->
      </div>
    </div>
    <div class="card-body pt-4 p-3">
      <a-input-search
          v-model:value="searchValue"
          style="margin-bottom: 8px"
          placeholder="Search"
      />
      <div id="scrollbar">
        <div v-if="isshow">
          <a-tree
              :expanded-keys="iExpandedKeys"
              :auto-expand-parent="autoExpandParent"
              :tree-data="showData"
              @expand="onExpand"
              :replace-fields="{children:'children', key:'id', value: 'id', title: 'label'}"
          >
            <template  v-slot:dropdown>
        <span v-if="label.indexOf(searchValue) > -1">
          {{ label.substr(0, label.indexOf(searchValue)) }}
          <span style="color: #f50">{{ searchValue }}</span>
          {{ label.substr(label.indexOf(searchValue) + searchValue.length) }}
        </span>
              <span v-else>{{ label }}</span>
            </template>
          </a-tree>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getTreeData} from "../../../api/project";

export default {
  name: "transaction-card",
  components: {
    // MaterialButton,
  },
  // props: {
  //   treeData: Array,
  //   isshow: Boolean
  // },
  data() {
    return {
      isshow: false,
      treedata: [],
      showData: [],
      defaultData: [],
      expandedKeys: [],
      searchVal: "",
      searchValue: "",
      iExpandedKeys: [],
      autoExpandParent: true,
      testData: [
        {
          id: '1',
          label: '中国',
          level: '1',
          children: [
            {
              id: '2',
              label: '山东',
              level: '2',
              children: [
                {
                  id: '4',
                  label: '济南',
                  level: '3',
                  children: [
                    {
                      id: '5',
                      label: '槐荫区',
                      level: '4'
                    },
                    {
                      id: '6',
                      label: '市中区',
                      level: '4'
                    },
                    {
                      id: '7',
                      label: '历城区',
                      level: '4'
                    },
                    {
                      id: '8',
                      label: '历下区',
                      level: '4'
                    },
                  ]
                }
              ]
            },
            {
              id: '3',
              label: '河北',
              level: '2',
              children: [
                {
                  id: '9',
                  label: '廊坊',
                  level: '3'
                }
              ]
            }
          ]
        }
      ],
    }
  },
  created() {
    getTreeData().then((response) => {
      if (response.status == 200) {
        var tmpdata = JSON.parse(response.data);
        console.log('treedata', tmpdata)
        this.treedata = tmpdata.treedata
        for (let i = 0; i < this.treedata.length; i++) {
          let temp = this.treedata[i]
          this.defaultData.push(JSON.parse(JSON.stringify(temp)))
          this.showData = [...this.defaultData];
          this.recursionData(this.defaultData);//将每一层数据都赋上title的slot,以高亮显示搜索字段
          this.setThisExpandedKeys(temp)
          // console.log(temp.id)
        }
        this.isshow = true
      }
    });
  },
  methods: {
    getTreeData() {
      debugger
      this.defaultData = [];
      for (let i = 0; i < this.treeData.length; i++) {
        console.log(this.treeData)
        let temp = this.treeData[i]
        this.defaultData.push(JSON.parse(JSON.stringify(temp)))
        this.showData = [...this.defaultData];
        this.recursionData(this.defaultData);//将每一层数据都赋上title的slot,以高亮显示搜索字段
        // this.setThisExpandedKeys(temp)
        // console.log(temp.id)
      }
      //调用获取数据的接口
      getTreeData().then((res) => {
        for (let i = 0; i < res.result.length; i++) {
          let temp = res.result[i]
          this.defaultData.push(JSON.parse(JSON.stringify(temp)))
          this.showData = [...this.defaultData];
          this.recursionData(this.defaultData);//将每一层数据都赋上title的slot,以高亮显示搜索字段
          this.setThisExpandedKeys(temp)
          // console.log(temp.id)
        }
      })
    },
    recursionData(node) {
      node.forEach(item => {
        item.scopedSlots = {title: 'label'}
        if (item.children && item.children.length) {
          this.recursionData(item.children)
        }
      })
    },
    setThisExpandedKeys(node) {
      //只展开一级目录
      if (node.children && node.children.length > 0) {
        this.iExpandedKeys.push(node.id)
        //下方代码放开注释则默认展开所有节点

        // for (let a = 0; a < node.children.length; a++) {
        //   this.setThisExpandedKeys(node.children[a])
        // }
      }
    },
    onExpand(expandedKeys) {
      this.iExpandedKeys = expandedKeys
      this.autoExpandParent = false
    },
    searchOnChange() {
      this.showData = [...this.defaultData];
      if (this.searchVal) {
        this.onSearch(this.searchVal);
      } else {
        this.searchValue = "";
        this.iExpandedKeys = [this.showData[0].id];
      }
    },
    onSearch(val) {
      const value = val
      this.searchValue = value
      if (value != '') {
        let treeData = JSON.parse(JSON.stringify(this.showData));
        // 删除四级中未匹配到的数据
        this.deleteTreedata(treeData, val, 4);
        // 删除三级数据中未匹配到的数据
        this.deleteTreedata(treeData, val, 3);
        // 删除二级数据中未匹配到的数据
        this.deleteTreedata(treeData, val, 2);
        this.showData = [...treeData];
        // 展开所有树数据
        this.expandAll(this.showData);
      } else {
        this.iExpandedKeys = [this.showData[0].id];
      }
    },
    deleteTreedata(node, val, level) {
      //这里注意数组一定要从后面对比删除，否则数组从前面删了以后，顺序就乱掉，就只能删第一个了
      for (let len = node.length - 1; len >= 0; len--) {
        if (node[len].children && node[len].children.length) {
          this.deleteTreedata(node[len].children, val, level)
        } else {
          if (node[len].level == level) {
            let str = node[len].label;
            if (str.indexOf(val) < 0) {
              node.splice(len, 1);
            }
          }
        }
      }
    },
    expandAll(node) {
      console.log('nodenode', node);
      node.forEach(item => {
        if (item.children && item.children.length) {
          this.iExpandedKeys.push(item.id)
          this.expandAll(item.children)
        }
      })
    },
  }
}
</script>
<style scoped>
#scrollbar {
  height: 285px;
  overflow-y: auto
}
</style>