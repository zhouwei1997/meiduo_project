# -*- coding: utf-8 -*- 
# @Time : 2023/5/29 20:42 
# @Author : 世间无事人
# @File : urls.py 
# @description :
from django.conf.urls import url

from areas import views

urlpatterns = [
    # 省市区三级联动
    url(r'^areas/$', views.AreasView.as_view())
]
