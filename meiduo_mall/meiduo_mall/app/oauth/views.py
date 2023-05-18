# Create your views here.
from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django.views import View

from meiduo_mall.utils.response_code import RETCODE


class QQAuthUserView(View):
    """处理QQ登录回调地址"""

    def get(self, request):
        """处理QQ登录回调"""
        code = request.GET.get("code")
        if not code:
            return http.HttpResponseForbidden('获取code失败')


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
