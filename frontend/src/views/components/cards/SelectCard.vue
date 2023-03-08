<template>
  <div>
<!--    <div class="card-header pb-0 p-3">-->
      <div class="row">
        <div class="col-12 d-flex align-items-center">
<!--          <h6 class="mb-0">Please select {{ this.optnames[0] }} and {{ this.optnames[1] }} </h6>-->
          <span style="margin-left: 30px">{{ this.optnames[0] }}:  </span>
          <select name="opt1" v-model="opt1" @change="selectOpt1($event)"
                 class="selectOpt">
            <option value="isOpt1">please select {{ this.optnames[0] }}</option>
            <option v-for="(item, index) in opts" :key="index" :value="item.opt1">
              {{ item.opt1 }}
            </option>
          </select>
          &nbsp;&nbsp;<span style="margin-left: 30px">{{ this.optnames[1] }}:  </span>
          <select name="opt2" v-model="opt2" @change="selectOpt2($event)" class="selectOpt">
            <option value="isOpt2">please select {{ this.optnames[1] }}</option>
            <option v-for="(item, index) in selectOpt2Data" :key="index" :value="item">
              {{ item }}
            </option>
          </select>
        </div>

<!--      </div>-->
    </div>
<!--    <div class="card-body p-3">-->
<!--      <div class="row">-->
<!--        <div class="col-md-12 mb-md-0 mb-4">-->

<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
  </div>
</template>

<script>

export default {
  name: "select-card",
  props: {
    'optnames': Array,
    'opts': Array
  },
  created() {
    var temp = {}
    var index = 0
    for (var i = 0; i < this.opts.length; i++) {
      var opt2 = this.opts[i].opt2
      for (var j = 0; j < opt2.length; j++) {
        temp[opt2[j]] = index++
      }
    }
    this.opt2Index = temp
  },
  data() {
    return {
      opt1: "isOpt1",//维度
      opt2: "isOpt2",//指标
      selectOpt2Data: {},//选择维度对应的指标
    };
  },
  methods: {
    //第一个选择框选择
    selectOpt1(event) {
      this.opt2 = "isOpt2"
      this.selectOpt2Data = this.opts[event.target.selectedIndex - 1].opt2
      this.opt1 = event.target.value
    },
    //第二个选择框选择
    selectOpt2(event) {
      this.opt2 = event.target.value
      debugger
      this.$emit('change-opt2', this.opt2, this.opt2Index[this.opt2] * 2 + 4)
    }
  }
};
</script>

<style>
.selectOpt {
  margin-left: 20px;
  width: 200px;
  display: block;
  padding: 0.5rem 0;
  padding-left: 0.5rem;
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1rem;
  color: #495057;
  background-color: transparent;
  background-clip: padding-box;
  border: 1px solid #d2d6da;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0.375rem;
  transition: 0.2s ease;
}
</style>
