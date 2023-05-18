# -*- coding: utf-8 -*- 
# @Time : 2023/5/18 21:34 
# @Author : 世间无事人
# @File : urls.py 
# @description :
from django.conf.urls import url

from oauth import views

urlpatterns = [
    # 获取扫码页面
    url(r'^qq/login/$', views.QQAuthURLView.as_view()),
    # 处理QQ登录回调
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
]
