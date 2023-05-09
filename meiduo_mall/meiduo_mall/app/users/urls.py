# -*- coding: utf-8 -*- 
# @Time : 2023/5/7 13:55 
# @Author : 世间无事人
# @File : urls.py
# users 子应用的路由信息
from django.conf.urls import url

from users import views

urlpatterns = [
    # 用户注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', views.UsernameCountView.as_view()),
]
