import axios from "axios";

const baseUrl = "/api";

const service = axios.create({
  baseURL: baseUrl,
  timeout: 60000
});

service.interceptors.request.use(
  config => {
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

service.interceptors.response.use(
  response => {
    // const res = response.data;

    // if (res.msg !== "success") {
    //   Message({
    //     message: res.msg || "Error",
    //     type: "error",
    //     duration: 5 * 1000
    //   });
    //   return Promise.reject(new Error(res.msg || "Error"));
    // } else {
    //   return res;
    // }
    return response;
  },
  // error => {
  //   Message({
  //     message: error.message,
  //     type: "error",
  //     duration: 5 * 1000
  //   });
  //   return Promise.reject(error);
  // }
);

export default service;
