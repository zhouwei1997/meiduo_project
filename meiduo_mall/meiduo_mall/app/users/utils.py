# -*- coding: utf-8 -*-
# @Time : 2023/5/14 14:43
# @Author : 世间无事人
# @File : utils.py
# 自定义用户认证后端，实现多账号登录
import re

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from users import constants
from users.models import User


def generate_verify_email_url(user):
    """
    商城邮箱激活链接
    :param user:当前登录的用户
    :return:token
    """
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = s.dumps(data)
    return settings.EMAIL_VERIFY_URL + '?token=' + token.decode()


def get_user_by_account(account):
    """
    通过账号获取用户
    :param account: 手机号/用户名
    :return:
    """
    try:
        # 校验username参数是用户名还是手机号
        if re.match(r'^1[3-9]\d{9}$', account):
            # username == 用户名
            user = User.objects.get(mobile=account)
        else:
            # username == 手机号
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写用户认证的方法
        1、使用账号查询用户
        2、如果可以查询到用户，需要校验密码时候正确
        :param request:
        :param username: 用户名/手机号
        :param password: 密码明文
        :param kwargs:
        :return: user
        """
        # 查询用户
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        else:
            return None
