# Create your views here.

import logging
import random

from django import http
from django.views import View
from django_redis import get_redis_connection

from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.utils.response_code import RETCODE
from verifications import constants
from verifications.libs.captcha.captcha import captcha

# 创建日志输出器
logger = logging.getLogger('django')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        :param request: 请求参数
        :param mobile: 手机号
        :return: JSON
        """
        image_code_client = request.GET.get("image_code")
        uuid = request.GET.get('uuid')
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必要参数')
        redis_conn = get_redis_connection('verify_code')
        # 判断用户时候频繁发送短信验证码
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse(
                {'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信访问过于频繁'})
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse(
                {'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已失效'})
        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # 将bytes转字符串再比较
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse(
                {'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码输入错误'})
        # 生成短信验证码
        sms_code = '%04d' % random.randint(0, 9999)
        logger.info(sms_code)
        # 创建redis的管道
        pl = redis_conn.pipeline()
        # 保存验证码
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行
        pl.execute()
        # 发送短信验证码
        # send_sms_code.delay(mobile, sms_code)
        send_sms_code.delay(mobile, sms_code)
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '短信发送成功'
        })


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
        redis_conn.setex(
            'img_%s' %
            uuid,
            constants.IMAGE_CODE_REDIS_EXPIRES,
            text)
        # 响应image/jepg
        return http.HttpResponse(image, content_type='image/jpg')
