# -*- coding: utf-8 -*- 
# @Time : 2023/5/11 20:07 
# @Author : 世间无事人
# @File : main.py
# @description celery 程序的入口文件
"""
启动celery任务
linux:celery -A celery_tasks.main worker -l info
windows:celery -A celery_tasks.main worker -l info -P eventlet
"""
import os

from celery import Celery
from celery.utils.log import get_task_logger

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    # 指定配置文件路径
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.settings-dev'

log = get_task_logger('django')
# 创建celery实例
celery_app = Celery('meiduo')
# 加载celery配置文件
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
