# # Broker配置，使用Redis作为消息中间件
# BROKER_URL = 'redis://127.0.0.1:6379/1'
# # BACKEND配置，这里使用redis
# RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 时区配置
CELERY_TIMEZONE = 'Asia/Shanghai'