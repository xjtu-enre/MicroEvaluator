# MicroEvaluator

## architecture

![系统架构图](./image/系统架构.png)

### 使用流程

1. 启动后台8081端口

2. 启动redis

   ```
   redis-server.exe redis.windows.conf
   ```

3. 启动celery

   ```
   celery  -A backend worker  -l debug -P eventlet
   ```

4. 启动前台

   ```
   npm run dev
   ```

   

