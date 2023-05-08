# -*- coding: utf-8 -*- 
# @Time : 2023/5/8 22:29 
# @Author : 世间无事人
# @File : urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # 首页广告：'/'
    url(r'^$', views.IndexView.as_view(), name='index')
]
