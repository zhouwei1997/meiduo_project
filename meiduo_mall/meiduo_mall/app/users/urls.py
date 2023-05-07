# -*- coding: utf-8 -*- 
# @Time : 2023/5/7 13:55 
# @Author : 世间无事人
# @File : urls.py
# users 子应用的路由信息
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view()),
]
