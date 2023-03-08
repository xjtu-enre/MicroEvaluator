import redis
from celery.app.control import Control
from django.http import JsonResponse, HttpResponse
# from .tasks import *
from celery import result
from backend.celery import backend
# from project.utils.data_view import update_project_process, query_project_by_name
#
#
# # Create your views here.
# def task_add_view(request):
#     project_name = request.GET.get('project_name')
#     project = query_project_by_name(project_name)
#
#     task_id = gen_dep_by_java_jar.delay(project.url, project_name, project.version)
#     return HttpResponse(task_id)
#
#
# def get_result_by_task_id(request):
#     redis_cli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')
#     task_id = request.GET.get('task_id')
#     project_name = request.GET.get('project_name')
#     # 异步执行
#     ar = result.AsyncResult(task_id)
#
#     if ar.ready():
#         # 删除redis中的key
#         all_key = redis_cli.keys('celery-*')
#         if all_key:
#             for key in all_key:
#                 redis_cli.delete(key)
#         # 删除celery正在执行的任务
#         celery_control = Control(app=backend)
#         celery_control.revoke(task_id, terminate=True)
#         update_project_process(project_name, 30)
#         return JsonResponse({'status': ar.state, 'result': ar.get()})
#     # 读取目前进度，返回给前台（redis中process字段用来记录）
#     return JsonResponse({'status': ar.state, 'result': 0})
