# Create your views here.
from django import http
from django.views import View
from django_redis import get_redis_connection

from verifications import constants
from verifications.libs.captcha.captcha import captcha


class SMSCodeView(View):
    """短信验证码"""
    redis_conn = get_redis_connection('verify_code')
    # redis_conn.setex('sms_%s' % uuid, constants.SMS_CODE_REDIS_EXPIRES, text)


class ImageCodeView(View):
    """图像验证码"""

    def get(self, request, uuid):
        """
        获取图像验证码
        :param request:
        :param uuid: 唯一标识图像验证码属于的用户
        :return: image/jpg/jpeg
        """
        # 生成验证码
        text, image = captcha.generate_captcha()
        # 保存验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 响应image/jepg
        return http.HttpResponse(image, content_type='image/jpg')
