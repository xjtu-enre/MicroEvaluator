<template>
  <div class="dialog-wrap" v-if="visable">
    <div class="dialog-body">
      <div class="card card-plain">
        <div class="pb-0 card-header bg-transparent mb-4">
          <h4 class="font-weight-bolder" style="float: left">Add New Project</h4>
        </div>
        <div class="card-body">
          <form role="form">
            <div class="mb-3">
              <span style="float: left">Project Name:</span>
              <material-input
                  id="projectname"
                  type="text"
                  label="please input project Name"
                  name="projectname"
                  size="lg"
                  @input="project.projectname=$event.target.value"
              />
            </div>
            <div class="mb-3">
              <span style="float: left">Url:</span>
              <material-input
                  id="url"
                  type="text"
                  label="please input url"
                  name="url"
                  size="lg"
                  @input="project.url=$event.target.value"
              />
            </div>
            <div class="mb-3">
              <span style="float: left">Description:</span>
              <material-input
                  id="description"
                  type="text"
                  label="please input description"
                  name="description"
                  size="lg"
                  @input="project.description=$event.target.value"
              />
            </div>
            <div class="mb-3">
              <span style="float: left">Language:</span>
              <material-input
                  id="language"
                  type="text"
                  label="please input language"
                  name="language"
                  size="lg"
                  @input="project.language=$event.target.value"
              />
            </div>
            <div class="mb-3">
              <span style="float: left">Version:</span>
              <material-input
                  id="ver"
                  type="text"
                  label="please input version"
                  name="ver"
                  size="lg"
                  @input="project.ver=$event.target.value"
              />
            </div>
            <material-checkbox
                id="ismicro"
                class="font-weight-light"
                @checked="setIsMicro"
            >
              This is a microservice project.
            </material-checkbox>
            <div>
              <div style="width: 40%;float: left;margin-right: 20px;margin-left: 50px;align-content: center">
                <material-button
                    class="mt-4"
                    variant="gradient"
                    color="success"
                    fullWidth
                    size="lg"
                    @click="submit"
                >Submit
                </material-button>
              </div>
              <div style="width: 40%;float: left">
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
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  addProject,
  checkTaskProcess,
} from "../../../api/project"
import MaterialInput from "../material/MaterialInput.vue";
import MaterialCheckbox from "../material/MaterialCheckbox.vue";
import MaterialButton from "../material/MaterialButton.vue";

export default {
  name: "AddProject",
  props: {
    visable: {  // 数据显示隐藏
      type: Boolean,
      default: false,
    }
  },
  components: {
    MaterialInput,
    MaterialCheckbox,
    MaterialButton,
  }
  ,
  data() {
    return {
      process: 0,
      project: {
        projectname: '',
        url: '',
        description: '',
        language: '',
        ver: '',
        ismicro: '',
      }
    };
  }
  ,
  watch: {
    process: {
      handler(newValue, oldValue) {
        console.log(newValue)
        console.log(oldValue)
        this.$emit('process-update')
      }
    }
  }
  ,
  methods: {
    setIsMicro(checked) {
      this.project.ismicro = checked
    },
    cancel(e) {
      console.log(e)
      this.$emit('visible-change')
    }
    ,
    submit() {
      this.$emit('visible-change')
      addProject(this.project).then((res) => {
        debugger
        if (res.data.message == 'success') {
          // this.$message.success('新增成功')
          this.confirmLoading = false
          this.cancel()
          var taskId = res.data.result
          // this.checkTask(taskId, this.project.projectname)
          this.timer = setInterval(this.checkTask, 10000, taskId, this.project.projectname);
        } else {
          // this.$message.warning('该项目已经存在')
          this.confirmLoading = false
          this.cancel()
        }
      }).finally((res) => {
        console.log(res);
        this.confirmLoading = false
      })
    },
    checkTask(task_id, projectname) {
      // 每5秒访问后台接口一次，查看当前解析进度
      checkTaskProcess(task_id, projectname).then((res) => {
        debugger
        this.process = res.data.result
        if (res.data.result == 100) {
          clearInterval(this.timer);
          this.timer = null
        }
      })
    }
  }
  ,
}
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
  top: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
  width: 30%
}
</style>
