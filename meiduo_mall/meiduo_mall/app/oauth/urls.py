# -*- coding: utf-8 -*- 
# @Time : 2023/5/18 21:34 
# @Author : 世间无事人
# @File : urls.py 
# @description :
from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^qq/login/', views.QQAuthURLView.as_view()),
]
