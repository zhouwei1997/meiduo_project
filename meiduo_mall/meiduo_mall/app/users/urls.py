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
    # 判断手机号是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 添加邮箱
    url(r'^emails/$', views.EmailView.as_view(), name='email'),
    # 验证邮箱
    url(r'^emails/verifications/$', views.VerifyEmailView.as_view()),
    # 用户地址
    url(r'^addresses/$', views.AddressView.as_view(), name='address'),
    # 新增地址
    url(r'^addresses/create/$', views.AddressCreateView.as_view()),
    # 修改和删除地址
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 修改地址标题
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    # 修改密码
    url(r'^passwoeds/$', views.ChangePasswordView.as_view(), name='pass'),
]
