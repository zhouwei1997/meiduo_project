# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2022/7/24
# @file  urls.py
# @description
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # 用户注册
    url(r'^register/$', views.RegisterView.as_view(), name='register')
]
