# -*- coding: utf-8 -*-
# @Time : 2023/5/7 9:49
# @Author : 世间无事人
# @File : jinja2_env.py

"""
补充jinja2环境
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({'static': staticfiles_storage.url, 'url': reverse, })
    return env
