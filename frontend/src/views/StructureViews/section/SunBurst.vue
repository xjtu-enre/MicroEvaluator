<template>
  <div>
    <div class="row">
      <div class="col-lg-8 col-md-6 mt-4">
        <div class="card card-body">
          <div id="chart"></div>
        </div>
      </div>
      <!--          <a-collapse v-model:activeKey="packageActiveKey" :expand-icon-position="expandIconPosition">-->
      <!--            <template #expandIcon="{ isActive }">-->
      <!--              <a-icon type="caret-right" :rotate="isActive ? 90 : 0"/>-->
      <!--            </template>-->
      <!--            <a-collapse-panel key="1" header="图例">-->
      <!--              <div id="legend"></div>-->
      <!--            </a-collapse-panel>-->
      <!--            <template v-if="currentKey === 'package'">-->
      <!--              <a-collapse-panel key="2" header="面包屑">-->
      <!--                <div id="breadCrumb"></div>-->
      <!--              </a-collapse-panel>-->
      <!--              <a-collapse-panel key="4" header="参数设置">-->
      <!--                <Row-->
      <!--                >-->
      <!--                  <Col :span="15"><h4>结点展示是否受层次影响</h4></Col-->
      <!--                  >-->
      <!--                  <Col :span="9"-->
      <!--                  >-->
      <!--                    <Switch-->
      <!--                        v-model:checked="nodeCheckedValue"-->
      <!--                        checked-children="是"-->
      <!--                        un-checked-children="否"-->
      <!--                        @change="handleNodeCheckedChange"/>-->
      <!--                  </Col-->
      <!--                  >-->
      <!--                </Row>-->
      <!--                <Row><h4>结点层次筛选</h4></Row>-->
      <!--                <Row>-->
      <!--                  <Col :span="4">-->
      <!--                    <h5>source</h5>-->
      <!--                  </Col>-->
      <!--                  <Col :span="6">-->
      <!--                    <Select-->
      <!--                        v-model:value="source"-->
      <!--                        style="width: 100px; margin-left: 20px"-->
      <!--                        :options="sourceData"-->
      <!--                        @change="handleSourceChange"-->
      <!--                    />-->
      <!--                  </Col>-->
      <!--                </Row>-->
      <!--                <Row>-->
      <!--                  <Col :span="4">-->
      <!--                    <h5>target</h5>-->
      <!--                  </Col>-->
      <!--                  <Col :span="6">-->
      <!--                    <Select-->
      <!--                        v-model:value="target"-->
      <!--                        style="width: 100px; margin-left: 20px"-->
      <!--                        :options="targetData"-->
      <!--                        @change="handleTargetChange"-->
      <!--                    />-->
      <!--                  </Col>-->
      <!--                </Row>-->
      <!--                <Row><h4>边出入度展示</h4></Row>-->
      <!--                <Row>-->
      <!--                  <a-checkbox-group-->
      <!--                      v-model:value="checkboxValue"-->
      <!--                      :options="checkboxOptions"-->
      <!--                      @change="handleCheckboxChange"-->
      <!--                  />-->
      <!--                </Row>-->
      <!--                <Row-->
      <!--                >-->
      <!--                  <Col :span="15">-->
      <!--                    <Row><h4>边边框显示</h4></Row>-->
      <!--                  </Col-->
      <!--                  >-->
      <!--                  <Col :span="9"-->
      <!--                  >-->
      <!--                    <Switch-->
      <!--                        v-model:checked="edgeStrokeValue"-->
      <!--                        checked-children="是"-->
      <!--                        un-checked-children="否"-->
      <!--                        @change="handleEdgeStrokeChange"/>-->
      <!--                  </Col-->
      <!--                  >-->
      <!--                </Row>-->
      <!--                <Row><h4>区域zoom</h4></Row>-->
      <!--                <Row>-->
      <!--                  <Col :span="10"-->
      <!--                  >-->
      <!--                    <a-button :danger="buttonDanger" @click="handleClick">{{-->
      <!--                        buttonContent-->
      <!--                      }}-->
      <!--                    </a-button>-->
      <!--                  </Col-->
      <!--                  >-->
      <!--                  <Col :span="10"-->
      <!--                  >-->
      <!--                    <a-button :disabled="disabled" @click="zoomReset" type="primary"-->
      <!--                    >reset-->
      <!--                    </a-button-->
      <!--                    >-->
      <!--                  </Col-->
      <!--                  >-->
      <!--                </Row>-->
      <!--              </a-collapse-panel>-->
      <!--            </template>-->
      <!--            <template v-if="currentKey === 'file'">-->
      <!--              <a-collapse-panel key="2" header="文件选择">-->
      <!--                <Select-->
      <!--                    v-model:value="fileType"-->
      <!--                    placeholder="文件类型"-->
      <!--                    style="width: 100px"-->
      <!--                    :label-in-value="true"-->
      <!--                    :options="fileTypes"-->
      <!--                    @change="handleFileTypeChange"-->
      <!--                />-->
      <!--                <Select-->
      <!--                    v-model:value="fileName"-->
      <!--                    placeholder="文件名称"-->
      <!--                    style="width: 200px"-->
      <!--                    :options="fileNames"-->
      <!--                    @change="handleFileNameChange"-->
      <!--                />-->
      <!--              </a-collapse-panel>-->
      <!--              <a-collapse-panel key="4" header="参数设置">-->
      <!--                <Row><h4>边出入度筛选</h4></Row>-->
      <!--                <Row>-->
      <!--                  <a-checkbox-group-->
      <!--                      v-model:value="fileEdgeValue"-->
      <!--                      :options="fileEdgeOptions"-->
      <!--                      @change="handleFileEdgeChange"-->
      <!--                  />-->
      <!--                </Row>-->
      <!--                <Row><h4>文件关系筛选</h4></Row>-->
      <!--                <Row>-->
      <!--                  <a-checkbox-group-->
      <!--                      v-model:value="fileRelationValue"-->
      <!--                      :options="fileRelationOptions"-->
      <!--                      @change="handleFileRelationChange"-->
      <!--                  />-->
      <!--                </Row>-->
      <!--              </a-collapse-panel-->
      <!--              >-->
      <!--            </template>-->
      <!--            <a-collapse-panel key="3" header="统计图" :force-render="true">-->
      <!--              <div id="count" style="width: 310px; height: 260px"></div>-->
      <!--            </a-collapse-panel>-->
      <!--          </a-collapse>-->
      <div class="col-lg-3 col-md-6 mt-4">
        <div class="card card-body">
          <!--          <div class="panels">-->
          <a-collapse v-model:activeKey="packageActiveKey" :expand-icon-position="expandIconPosition">
            <template #expandIcon="{ isActive }">
              <a-icon type="caret-right" :rotate="isActive ? 90 : 0"/>
            </template>
            <a-collapse-panel key="1" header="图例">
              <div id="legend"></div>
            </a-collapse-panel>
            <template v-if="currentKey === 'package'">
              <a-collapse-panel key="2" header="面包屑">
                <div id="breadCrumb"></div>
              </a-collapse-panel>
              <a-collapse-panel key="4" header="参数设置">
                <Row
                >
                  <Col :span="15"><h4>结点展示是否受层次影响</h4></Col
                  >
                  <Col :span="9"
                  >
                    <Switch
                        v-model:checked="nodeCheckedValue"
                        checked-children="是"
                        un-checked-children="否"
                        @change="handleNodeCheckedChange"/>
                  </Col
                  >
                </Row>
                <Row><h4>结点层次筛选</h4></Row>
                <Row>
                  <Col :span="4">
                    <h5>source</h5>
                  </Col>
                  <Col :span="6">
                    <Select
                        v-model:value="source"
                        style="width: 100px; margin-left: 20px"
                        :options="sourceData"
                        @change="handleSourceChange"
                    />
                  </Col>
                </Row>
                <Row>
                  <Col :span="4">
                    <h5>target</h5>
                  </Col>
                  <Col :span="6">
                    <Select
                        v-model:value="target"
                        style="width: 100px; margin-left: 20px"
                        :options="targetData"
                        @change="handleTargetChange"
                    />
                  </Col>
                </Row>
                <Row><h4>边出入度展示</h4></Row>
                <Row>
                  <a-checkbox-group
                      v-model:value="checkboxValue"
                      :options="checkboxOptions"
                      @change="handleCheckboxChange"
                  />
                </Row>
                <Row
                >
                  <Col :span="15">
                    <Row><h4>边边框显示</h4></Row>
                  </Col
                  >
                  <Col :span="9"
                  >
                    <Switch
                        v-model:checked="edgeStrokeValue"
                        checked-children="是"
                        un-checked-children="否"
                        @change="handleEdgeStrokeChange"/>
                  </Col
                  >
                </Row>
                <Row><h4>区域zoom</h4></Row>
                <Row>
                  <Col :span="10"
                  >
                    <a-button :danger="buttonDanger" @click="handleClick">{{
                        buttonContent
                      }}
                    </a-button>
                  </Col
                  >
                  <Col :span="10"
                  >
                    <a-button :disabled="disabled" @click="zoomReset" type="primary"
                    >reset
                    </a-button
                    >
                  </Col
                  >
                </Row>
              </a-collapse-panel>
            </template>
            <template v-if="currentKey === 'file'">
              <a-collapse-panel key="2" header="文件选择">
                <Select
                    v-model:value="fileType"
                    placeholder="文件类型"
                    style="width: 100px"
                    :label-in-value="true"
                    :options="fileTypes"
                    @change="handleFileTypeChange"
                />
                <Select
                    v-model:value="fileName"
                    placeholder="文件名称"
                    style="width: 200px"
                    :options="fileNames"
                    @change="handleFileNameChange"
                />
              </a-collapse-panel>
              <a-collapse-panel key="4" header="参数设置">
                <Row><h4>边出入度筛选</h4></Row>
                <Row>
                  <a-checkbox-group
                      v-model:value="fileEdgeValue"
                      :options="fileEdgeOptions"
                      @change="handleFileEdgeChange"
                  />
                </Row>
                <Row><h4>文件关系筛选</h4></Row>
                <Row>
                  <a-checkbox-group
                      v-model:value="fileRelationValue"
                      :options="fileRelationOptions"
                      @change="handleFileRelationChange"
                  />
                </Row>
              </a-collapse-panel
              >
            </template>
            <a-collapse-panel key="3" header="统计图" :force-render="true">
              <div id="count" style="width: 310px; height: 260px"></div>
            </a-collapse-panel>
          </a-collapse>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {computed} from 'vue';
// import PCollapse from "../../components/panel/PCollapse";
import {drawChart} from '../../../assets/js/section/sunburst';
import {getSectionEdgesList, getSectionNodesList} from "../../../api/project";

export default ({
  name: 'SectionSunburst',
  props: {
    nodes: {
      type: Object,
    },
    edges: {
      type: Object,
    },
  },
  // components: {PCollapse},
  data() {
    return {
      componentKey: 'd3',
      checkboxGroupProps: {
        checkboxValue: ['in', 'out'],
        checkboxOptions: [
          {label: '入度', value: 'in'},
          {label: '出度', value: 'out'},
        ],
        fileEdgeValue: ['in', 'out'],
        fileEdgeOptions: [
          {label: '入度', value: 'in'},
          {label: '出度', value: 'out'},
        ],
        fileRelationValue: ['in_package', 'out_package', 'out_organization'],
        fileRelationOptions: [
          {label: '包内', value: 'in_package'},
          {label: '包外', value: 'out_package'},
          {label: '跨组织', value: 'out_organization'},
        ],
      },
      collapseProps: {
        allowClear: true,
        expandIconPosition: 'right',
        fileActiveKey: ['1'],
        forceRender: true,
        packageActiveKey: ['1', '2'],
      },
      echartsProps: {
        echartsNodes: [],
        echartsEdges: []
      },
      selectProps: {
        fileName: '',
        fileNamesObject: {},
        fileType: {value: 'in_package'},
        fileTypes: []
      },
      sourceProps: {
        isChanged: true,
        source: '0',
        sourceData: [],
        sourceObject: [],
        target: '0',
      },
      switchProps: {
        edgeStrokeValue: false,
        nodeCheckedValue: false,
      },
      zoomProps: {
        disabled: false,
      },
      currentKey: 'package',
      buttonContent: computed(() => (this.zoomProps.disabled ? '开启zoom' : '禁止zoom')),
      buttonDanger: computed(() => !this.zoomProps.disabled),
      handleClick: computed(() =>
          this.zoomProps.disabled ? this.zoomProps.zoomAbled : this.zoomProps.zoomDisabled,
      ),
      fileNames: computed(() => this.selectProps.fileNamesObject[this.selectProps.fileType.value]),
      targetData: computed(() => this.sourceProps.sourceObject[this.sourceProps.source]),
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
          drawChart(
              this.componentKey,
              this.currentKey,
              this.nodeDatas,
              this.edgeDatas,
              this.checkboxGroupProps,
              this.echartsProps,
              this.selectProps,
              this.sourceProps,
              this.switchProps,
              this.zoomProps,
          );
        }
      })
    }
  },
});
</script>

<style>
.tooltip {
  position: absolute;
  pointer-events: none;
  height: 40px;
  padding: 4px;
  border-radius: 8px;
  background-color: white;
  font-size: 0.8em;
}
</style>
