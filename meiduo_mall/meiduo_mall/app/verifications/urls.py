# -*- coding: utf-8 -*- 
# @Time : 2023/5/10 19:40 
# @Author : 世间无事人
# @File : urls.py

from django.conf.urls import url

from verifications import views

urlpatterns = [
    # 图像验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
]
