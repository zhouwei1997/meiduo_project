# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/5/24
# @file  views.py
# @description
"""
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from meiduo_mall.utils.response_code import RETCODE


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """
    自定义判断用户是否登录的扩展类
    :return JSON
    """

    def handle_no_permission(self):
        """
        重写 handle_no_permission 方法
        :return: JSON
        """
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
