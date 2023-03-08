// vue.config.js;
module.exports = {
  runtimeCompiler: true,
  devServer: {
    proxy: {
      "^/api": {
        target: "http://127.0.0.1:8081", // 你要请求的后端接口ip+port
        changeOrigin: true, // 允许跨域，在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样服务端和服务端进行数据的交互就不会有跨域问题
        ws: true, // 开启webSocket
        pathRewrite: {
          "^/api": "" // 替换成target中的地址
        }
      }
    }
  }
}
;
// app.use((req, res, next) => {
//   //只对api开头的请求做拦截处理
//   if (/^\/api/.test(req.path)) {
//     if (req.path == '/api/login' || req.headers.token) {
//       next();
//     } else {
//       //设置错误状态码为401
//       res.sendStatus('401')
//       next();
//     }
//   } else {
//     next();
//   }
// })
