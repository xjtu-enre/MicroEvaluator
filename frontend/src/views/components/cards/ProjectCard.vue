<template>
  <div class="card">
    <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
          <h6>Your Projects</h6>
          <p class="text-sm mb-0" v-html="des"></p>
        </div>
        <div class="col-6 text-end">
          <material-button color="dark" variant="gradient" @click="addProject">
            <i class="fas fa-plus me-2"></i>
            Add New Project
          </material-button>
          <add-project-card @visible-change="changeVisable" @process-update='updateProcess'
                            :visable="visible"></add-project-card>
        </div>
      </div>
    </div>
    <div class="card-body px-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
          <tr>
            <th
                v-for="(heading, index) of headers"
                :key="index"
                :class="[
                  index === 1 ? 'ps-2' : '',
                  index >= 2 ? 'text-center' : '',
                ]"
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            >
              {{ heading }}
            </th>
          </tr>
          </thead>
          <tbody>
          <tr
              v-for="(
                {
                  id,
                  projectname,
                  description,
                  ismicro,
                  // process
                  // progress: { percentage, color },
                },
                index
              ) of projects"
              :key="index"
          >
            <td>
              <div class="d-flex px-2 py-1">
                <div>
                  <img :src="getImgSrc(ismicro)" class="avatar avatar-sm me-3" alt="Logo"/>
                </div>
                <div class="d-flex flex-column justify-content-center">
                  <h6 class="mb-0 text-sm">{{ projectname }}</h6>
                </div>
              </div>
            </td>
            <td class="align-middle text-sm">
              <span class="text-xs font-weight-bold"> {{ description }} </span>
            </td>
<!--            <td class="align-middle text-center text-sm">-->
<!--                      <span class="badge badge-sm bg-gradient-success"-->
<!--                      >{{ ismicro }}</span-->
<!--                      >-->
<!--            </td>-->
            <td class="align-middle text-center text-sm">
              <div class="progress-wrapper w-75 mx-auto">
                <div class="progress-info">
                  <div class="progress-percentage">
                      <span class="text-xs font-weight-bold"
                      >100%
                        <!--                        {{ this.progress }}%-->
                      </span>
                  </div>
                </div>
                <div class="progress" style="margin:auto;margin-top: 5px">
                  <div
                      class="progress-bar"
                      :class="`w-${100}  bg-gradient-${getColor(100)}`"
                      role="progressbar"
                      :aria-valuenow="this.progress"
                      aria-valuemin="0"
                      aria-valuemax="100"
                  ></div>
                </div>
              </div>
            </td>
            <td class="align-middle text-center text-sm">
              <a class="btn btn-link text-success px-3 mb-0" @click="handleStructure()">
                <i class="mdui-icon material-icons" title="structure">&#xe8f1;</i>
              </a>
              <a class="btn btn-link text-success px-3 mb-0" @click="handleEvaluator(projectname, id)">
                <i class="mdui-icon material-icons" title="evaluator">&#xe6e1;</i>
              </a>
<!--              <a class="btn btn-link text-success px-3 mb-0" @click="handleDetection(projectname, id)">-->
<!--                <i class="mdui-icon material-icons" title="detection">&#xe548;</i>-->
<!--              </a>-->
              <a
                  class="btn btn-link text-danger text-gradient px-3 mb-0"
                  @click="handleDelete(id)"
              >
                <i class="mdui-icon material-icons" title="delete">&#xe872;</i>
              </a>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import MaterialButton from "../material/MaterialButton";
import {deleteProject} from "../../../api/project"
import AddProjectCard from "./AddProjectCard";
import ismicroimg from "../../../assets/img/small-logos/ismocro.svg"
import isnotmicroimg from "../../../assets/img/small-logos/isnotmicro.svg"

export default {
  name: "projectCard",
  components: {
    MaterialButton,
    // MaterialSnackbar
    AddProjectCard
  },
  props: {
    projects: {
      type: Array,
      required: true,
      languange: String,
      projectname: String,
      description: String,
      ismicro: String,
      process: Number
    },
  },
  mounted() {
    this.des = "<i class='fa fa-check text-info' aria-hidden='true'></i> <span class='font-weight-bold ms-1'>" + this.projects.length + "</span> projects in total"
  },
  watch: {
    projects() {
      this.$nextTick(() => {
        this.des = "<i class='fa fa-check text-info' aria-hidden='true'></i> <span class='font-weight-bold ms-1'>" + this.projects.length + "</span> projects in total"
      })
    }
  },
  data() {
    return {
      headers: ['Project Name', 'Description', 'Progress', 'Operator'],
      ismicroimg,
      isnotmicroimg,
      des: '',
      visible: false,
      progress: 0,
    }
  },
  methods: {
    addProject() {
      console.log('visible', this.visible)
      this.visible = !this.visible
    },
    changeVisable() {
      this.visible = false
      this.$emit('projects-refresh')
    },
    updateProcess(process) {
      this.progress = process
    },
    getColor(process) {
      if (process == 100) {
        return 'success'
      } else if (process < 100 && process > 0) {
        return 'info'
      }
      return 'warning'
    },
    getImgSrc(ismicro) {
      if (ismicro) {
        return this.ismicroimg
      }
      return this.isnotmicroimg
    },
    handleEvaluator(projectName, projectid) {
      this.$router.push({
        "name": "Version",
        query: {
          'projectname': projectName,
          'projectid': projectid
        }
      })
    },
    // handleDetection(projectName, projectid) {
    //   this.$router.push({
    //     "name": "HotMap",
    //     query: {
    //       'projectname': projectName,
    //       'projectid': projectid
    //     }
    //   })
    // },
    handleStructure() {
      this.$router.push({
        "name": "Structure",
        // query: {
        //   'projectname': project_name
        // }
      })
    },
    handleIdentifier() {
      this.$router.push({
        "name": "HotMap",
        // query: {
        //   'projectname': project_name
        // }
      })
    },
    handleDelete(project_id) {
      deleteProject(project_id).then((res) => {
        if (res.status == 204) {
          // this.snackbarType += 'success'
          // this.snackbarDscription = 'Delete successfully!!!'
          // this.snackbarColor = 'success'
          this.$emit('projects-refresh')
        } else {
          this.$message.error('删除失败：' + JSON.stringify(res.message))
        }
      })
    },
    closeSnackbar() {
      this.snackbarType += null;
    },
  }
};
</script>
