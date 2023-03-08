from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from backend import settings

# 设置系统环境变量，安装django，必须设置，否则在启动celery时会报错
# backend 是当前项目名
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
backend = Celery('backend', broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2')
backend.config_from_object('backend.celery_config')
backend.autodiscover_tasks(lambda: settings.INSTALLED_APPS)