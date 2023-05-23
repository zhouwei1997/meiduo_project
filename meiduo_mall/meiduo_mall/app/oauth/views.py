# Create your views here.
import logging
import re

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from meiduo_mall.utils.response_code import RETCODE
from oauth.models import OAuthQQUser
from oauth.utils import generate_access_token, check_access_token

logger = logging.getLogger('django')


class QQAuthUserView(View):
    """处理QQ登录回调地址"""

    def get(self, request):
        """处理QQ登录回调"""
        code = request.GET.get("code")
        if not code:
            return http.HttpResponseForbidden('获取code失败')

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 获取access_token
            access_token = oauth.get_access_token(code)
            # 获取openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logging.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')
        # 判断openid是否绑定用户
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist as e:
            # openid未绑定用户
            access_token_openid = generate_access_token(openid)
            return render(
                request, 'oauth_callback.html', {
                    'access_token_openid': access_token_openid})
        else:
            # openid绑定用户
            login(request, oauth_user.user)
            return redirect(reverse('contents:index')).set_cookie(
                'username',
                oauth_user.user.username,
                max_age=3600 * 24 * 15)

    def post(self, request):
        """绑定用户"""
        mobile = request.GET.get('mobile')
        password = request.GET.get('password')
        sms_code_client = request.GET.get('sms_code_client')
        access_token_openid = request.GET.get('access_token_openid')
        if not all([mobile, password, sms_code_client]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        if not re.match(r'^[0-9A-Za-z]{8,20}', password):
            http.HttpResponseForbidden('请输入8-20位的密码')
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is not None:
            return render(
                request, 'oauth_callback.html', {
                    'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(
                request, 'oauth_callback.html', {
                    'sms_code_errmsg': '输入短信验证码有误'})
        # 判断openid是否有效
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(
                request, 'oauth_callback.html', {
                    'openid_errmsg': 'openid已失效'})
        """
        1、使用手机号查询对应的用户是否存在
        2、如果手机号不存在，新建用户
        3、如果手机号用户存在，需要校验用户
        4、将用户绑定到openid
        5、状态保持
        6、cookies中写入用户名
        7、响应结果
        """
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=mobile, password=password, mobile=mobile)
        else:
            if not user.check_password(password):
                return render(
                    request, 'oauth_callback.html', {
                        'account_errmsg': '账号或密码错误'})
        # oauth_qq_user = OAuthQQUser(user=user, openid=openid)
        # oauth_qq_user.save()
        try:
            oauth_qq_user = OAuthQQUser.objects.create(
                user=user, openid=openid)
        except Exception as e:
            logger.error(e)
            return render(
                request, 'oauth_callback.html', {
                    'qq_login_errmsg': '账号或密码错误'})
        login(request, oauth_qq_user.user)
        return redirect(request.GET.get('state')).set_cookie(
            'username', oauth_qq_user.user.username, max_age=3600 * 24 * 15)


class QQAuthURLView(View):
    """
    提供QQ登录页面
    """

    def get(self, request):
        next = request.GET.get("next")
        # 获取QQ登录页面
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next)
        login_url = oauth.get_qq_url()
        return http.JsonResponse(
            {'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': login_url})
