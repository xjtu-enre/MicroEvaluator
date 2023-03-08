<template>
  <div class="card my-4">
    <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
      <div
          class="bg-gradient-dark shadow-success border-radius-lg pt-4 pb-3"
      >
        <h6 class="text-white text-capitalize ps-3">Project Versions Info</h6>
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
          <tr v-for="(
                      {
                      version,
                      loc,
                      score,
                      // timestap
                  },
                  index
                  ) of versiondata"
              :key="index">
            <td>
              <div class="d-flex px-2 py-1">
                <div>
                  <img
                      :src="ismicroimg"
                      class="avatar avatar-sm me-3 border-radius-lg"
                      alt="user1"
                  />
                </div>
                <div class="d-flex flex-column justify-content-center">
                  <h6 class="mb-0 text-sm">{{ version }}</h6>
                </div>
              </div>
            </td>
            <td>
              <p class="text-xs text-secondary mb-0">{{ loc }}</p>
            </td>
            <td class="align-middle text-center text-sm">
                      <span :class="getScoreColor(score)"
                      >{{ score }}</span
                      >
            </td>
<!--              <p class="text-xs text-secondary mb-0">-->
<!--                Good:score≥0.8-->
<!--              </p>-->
<!--              &lt;!&ndash;              <hr class="vertical dark"/>&ndash;&gt;-->
<!--              <p class="text-xs text-secondary mb-0">-->
<!--                Average:0.4≤score&lt;0.8-->
<!--              </p>-->
<!--              &lt;!&ndash;              <hr class="vertical dark"/>&ndash;&gt;-->
<!--              <p class="text-xs text-secondary mb-0">-->
<!--                Poor:score&lt;0.4-->
<!--              </p>-->
<!--            </td>-->
<!--            <td class="align-middle text-center text-sm">-->
<!--              <p class="mb-0 text-xs text-secondary">-->
<!--                <i class="fa fa-clock me-1"></i>-->
<!--                {{ getTime(timestap) }}-->
<!--              </p>-->
<!--            </td>-->
            <td class="align-middle text-center text-sm">
              <a class="btn btn-link text-success px-3 mb-0" @click="goMetric(version, loc)">
                <i class="mdui-icon material-icons" title="metric">&#xe6df;</i>
              </a>
            </td>
          </tr>
          <tr>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import ismicroimg from "../../../assets/img/small-logos/ismocro.svg"

export default {
  name: "VersionProjectCard",
  props: {
    versiondata: Array,
    projectname: String
  },
  created() {
    console.log(this.versiondata)
    console.log('this.projectname', this.projectname)
  },
  data() {
    return {
      // headers: ['Version', 'Loc', 'Score', 'CreateTime', 'Operator'],
      headers: ['Version', 'Loc', 'Score', 'Operator'],
      ismicroimg
    }
  },
  methods: {
    goMetric(version, loc) {
      this.$router.push({
        name: "MetricData",
        query: {
          'projectname': this.projectname,
          'version': version,
          'loc': loc
        }
      });
    },
    getScoreColor(score) {
      if (score < 0.4) {
        return 'badge badge-sm bg-gradient-danger'
      } else if (score >= 0.4 && score < 0.7) {
        return 'badge badge-sm bg-gradient-warning'
      }
      return 'badge badge-sm bg-gradient-success'
    },
    getTime(timestap) {
      console.log(timestap)
      var date = new Date(timestap)
      console.log(date)
    }
  }
}
</script>

<style scoped>

</style>