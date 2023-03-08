<template>
  <div>
    <div class="row">
      <div class="col-lg-9 col-md-6 mt-4">
        <div class="card card-body">
          <div id="tooltip"></div>
          <div id="chart"></div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mt-4">
        <div class="card card-body">
          <p-collapse title="图例" headColor="#151515" bgColor="#fff" isCollapse="true" style="color:black;">
            <div id="legend"></div>
          </p-collapse>
<!--          <a-collapse v-model:activeKey="activeKey" :expand-icon-position="expandIconPosition">-->
<!--            <template #expandIcon="{ isActive }">-->
<!--              <a-icon type="caret-right" :rotate="isActive ? 90 : 0"/>-->
<!--            </template>-->
<!--            <a-collapse-panel key="1" header="图例">-->
<!--              <div id="legend"></div>-->
<!--            </a-collapse-panel>-->
<!--            <a-collapse-panel key="2" header="参数设置">-->
<!--              <Row-->
<!--              ><h4>{{ h4Value }}</h4></Row-->
<!--              >-->
<!--              <Row>-->
<!--                <Col :span="15">-->
<!--                  <Slider-->
<!--                      v-model:value="sliderValue"-->
<!--                      :max="max"-->
<!--                      :min="min"-->
<!--                      :tooltip-visible="false"-->
<!--                      @change="handleSliderChange"-->
<!--                  />-->
<!--                </Col>-->
<!--                <Col :span="2">-->
<!--                  <InputNumber-->
<!--                      v-model:value="sliderValue"-->
<!--                      :max="max"-->
<!--                      :min="min"-->
<!--                      @change="handleSliderChange"-->
<!--                      style="margin-left: 16px; width: 5px"-->
<!--                  />-->
<!--                </Col>-->
<!--              </Row>-->
<!--              <Row><h4>原生伴生筛选</h4></Row>-->
<!--              <Row-->
<!--              >-->
<!--                <a-radio-group v-model:value="radioValue" @change="handleRadioChange"-->
<!--                >-->
<!--                  <a-radio :value="1">伴生</a-radio>-->
<!--                  <a-radio :value="0">原生</a-radio>-->
<!--                </a-radio-group-->
<!--                >-->
<!--              </Row-->
<!--              >-->
<!--              <Row><h4>区域zoom</h4></Row>-->
<!--              <Row>-->
<!--                <Col :span="10"-->
<!--                >-->
<!--                  <a-button :danger="buttonDanger" @click="handleClick">{{-->
<!--                      buttonContent-->
<!--                    }}-->
<!--                  </a-button>-->
<!--                </Col-->
<!--                >-->
<!--                <Col :span="10"-->
<!--                >-->
<!--                  <a-button :disabled="disabled" @click="zoomReset" type="primary">reset</a-button>-->
<!--                </Col-->
<!--                >-->
<!--              </Row>-->
<!--            </a-collapse-panel>-->
<!--          </a-collapse>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {computed} from 'vue';
import PCollapse from "../../components/panel/PCollapse";
import {changeLinksByRadio, changeLinksBySlider, drawChart, drawLegend} from '../../../assets/js/section/chord';
import {getSectionEdgesList, getSectionNodesList} from "../../../api/project";

export default ({
  name: 'SectionChord',
  components: {
    PCollapse
  },
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
      collapseProps: {
        allowClear: true,
        activeKey: ['1'],
        expandIconPosition: 'right',
        forceRender: true,
      },
      sliderProps: {
        max: 100,
        min: 10,
        sliderValue: 20,
        handleSliderChange: (value) => {
          changeLinksBySlider(this.radioProps.radioValue, value);
        }
      },
      radioProps: {
        radioValue: 1,
        handleRadioChange: (event) => {
          changeLinksByRadio(event.target.value, this.sliderProps);
        }
      },
      zoomProps: {
        disabled: false,
      },
      buttonContent: computed(() => (this.zoomProps.disabled ? '开启zoom' : '禁止zoom')),
      buttonDanger: computed(() => !this.zoomProps.disabled),
      handleClick: computed(() =>
          this.zoomProps.disabled ? this.zoomProps.zoomAbled : this.zoomProps.zoomDisabled,
      ),
      h4Value_array: ['原生到伴生边数', '伴生到原生边数'],
      h4Value: computed(() => this.h4Value_array[this.radioProps.radioValue]),
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
          drawLegend();
          drawChart(this.nodeDatas, this.edgeDatas, this.radioProps, this.sliderProps, this.zoomProps);
        }
      })
    }
  }
});
</script>

<style>
.panels {
  position: fixed !important;
  bottom: 0;
  /*right: -20;*/
  width: 350px;
  /*max-height: calc(100vh - 2 * var(--stage-padding));*/
  overflow-y: auto;
  /*padding: var(--stage-padding);*/
  scrollbar-width: thin;
}

.tool-tip {
  position: absolute;
  z-index: 2;
  visibility: hidden;
  background-color: #fff;
  border: 1px solid #333;
  padding: 12px 6px;
  pointer-events: none;
}
</style>
