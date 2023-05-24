# Create your views here.
import json
import logging
import re

from django import http
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from meiduo_mall.utils.response_code import RETCODE
from users.models import User

logger = logging.getLogger('django')


class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')
        # 赋值给email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """用户中心页面"""
        # 如果LoginRequireMixin判断出用户已登录，那么request.user就是登录用户对象
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_activem}
        return render(request, 'user_center_info.html', context)


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """
        退出登录
        :param request:
        :return: 首页
        """
        logout(request)
        # 删除cookie中的用户名
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """
        提供用户登录页面
        :param request:
        :return: 登录页面
        """
        return render(request, 'login.html')

    def post(self, request):
        """用户登录逻辑"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少为8位，最长为20位')
        # 认证登陆用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})
        # 状态保持
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户；浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户，状态保持周期为2周  默认 2周
            request.session.set_expiry(None)
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            # 首页展示用户名信息
            response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        return response


class MobileCountView(View):
    """判断手机号时候重复注册"""

    def get(self, request, mobile):
        """
        获取手机号
        :param request:请求对象
        :param mobile:手机号
        :return:JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '该手机号已经被注册',
            'count': count
        })


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '该用户名已经被注册',
            'count': count
        })


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供用户注册页面
        :param request:
        :return: 注册页面
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        用户注册业务逻辑
        :param request:
        :return:
        """
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')
        # 校验参数
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断短信验证码是否正确
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(
                request, 'register.html', {
                    'sms_code_errmsg': '短信验证码已失效'})
        if sms_code_client != sms_code_server.decode():
            return render(
                request, 'register.html', {
                    'sms_code_errmsg': '输入短信验证码有误'})
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据
        try:
            user = User.objects.create_user(
                username=username, password=password, mobile=mobile)
        except DatabaseError as e:
            logger.error(e)
            return render(
                request, 'register.html', {
                    'register_errmsg': '注册失败'})
        # 状态保持
        login(request, user)
        # 响应结果；重定向到首页
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        return response
