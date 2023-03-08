import request from "../util/request";

export function login() {
  return request({
    url: "/login/",
    method: "get"
  });
}

export function register(params) {
  return request({
    url: "/user/register/",
    method: "post",
    params
  });
}

export function getCurentProjectMetricData() {
  return request({
    url: "/projectdata/",
    method: "get"
  });
}

export function getCurentModuleMetricData() {
  return request({
    url: "/moduledata/",
    method: "get"
  });
}

export function getCurentProject() {
  return request({
    url: "/project/",
    method: "get"
  });
}

export function addProject(params) {
  return request({
    url: "/project/",
    method: "post",
    params
  });
}

export function test(params) {
  return request({
    url: "/test/",
    method: "get",
    params
  });
}

export function checkTaskProcess(task_id, projectname) {
  return request({
    url: "/project/" + task_id + '&' + projectname + '/',
    method: "get",
  })
}

export function deleteProject(id) {
  return request({
    url: "/project/" + id + '/',
    method: "delete",
    // xsrfHeaderName: "X-CSRFToken"
  });
}

export function getVersionData(id) {
  return request({
    url: "/version/" + id + '/',
    method: "get",
  });
}

export function getLineData() {
  return request({
    url: '/linedata/',
    method: "get",
  });
}

export function getHotMapData() {
  return request({
    url: '/hotmapdata/',
    method: "get",
  });
}

export function getMetricData() {
  return request({
    url: '/metricdata/',
    method: "get",
  });
}

export function getTreeData() {
  return request({
    url: '/treedata/',
    method: "get",
  });
}

export function getCatalogueDatasList() {
  return request({
    url: "/catelogues/",
    method: "get"
  });
}


export function getCatalogueTreeMapDatas() {
  return request({
    url: '/cateloguesTreeMap/',
    method: "get"
  });
}

export function getClusterDatasList() {
  return request({
    url: '/cluster/',
    method: "get"
  });
}

// export function getAllScore() {
//   return request({
//     url: '/score/',
//     method: "get",
//     params: {'id': id}
//   })
// }

export const downloadInspect = params => {
  request({
    url: "/getReport/",
    method: "post",
    params
  });
};

export function Upexcele(value) {
  const url = window.URL.createObjectURL(value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report.docx'
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

export function competeMetricData(params) {
  return request({
    url: "/competeMetricData/",
    method: "get",
    params
  });
}

export function getProjectData(params) {
  return request({
    url: "/getProjectData/",
    method: "get",
    params
  });
}


export function getFunctionality(params) {
  return request({
    url: "/get_all_Data_functionality/",
    method: "get",
    params
  });
}

export function getInteractionComplexity(params) {
  return request({
    url: "/get_all_Data_InteractionComplexity/",
    method: "get",
    params
  });
}

export function getEvolvability(params) {
  return request({
    url: "/get_all_Data_evolvability/",
    method: "get",
    params
  });
}

export function getModularity(params) {
  return request({
    url: "/get_all_Data_modularity/",
    method: "get",
    params
  });
}

export function getPlanTree(params) {
  return request({
    url: "/drawTree/",
    method: "get",
    params
  });
}

export function getHistoryData(params) {
  return request({
    url: "/getHistoryData/",
    method: "get",
    params
  });
}

export function getHotmapData(params) {
  return request({
    url: "/hotmap/",
    method: "get",
    params
  });
}

export function getCauseEntitiesData(params) {
  return request({
    url: "/cause/",
    method: "get",
    params
  });
}


export function batchImportProject(params) {
  return request({
    url: "/batchImportProject/",
    method: "get",
    params
  });
}

export function deleteBatchFile(params) {
  return request({
    url: "/deleteBatchFile/",
    method: "get",
    params
  });
}

export function getSectionNodesList(params) {
  return request({
    url: '/sectionNodes/',
    method: "get",
    params
  });
}

export function getSectionEdgesList(params) {
  return request({
    url: '/sectionEdges/',
    method: "get",
    params
  });
}


export function addData(params) {
  return request({
    url: '/addData/',
    method: "get",
    params
  })
}


export function uploadSection(params) {
  return request({
    url: '/uploadSection/',
    method: "get",
    params
  })
}
