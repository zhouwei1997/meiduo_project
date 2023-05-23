# -*- coding: utf-8 -*- 
# @Time : 2023/5/20 11:08 
# @Author : 世间无事人
# @File : utils.py 
# @description : 工具方法
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serialzier, BadData

from oauth import constants


def check_access_token(access_token_openid):
    """
    反序列化openid
    :param access_token_openid:openid密文
    :return: openid
    """
    s = Serialzier(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    try:
        data = s.loads(access_token_openid)
    except BadData:
        # 密文过期
        return None
    else:
        return data.get('openid')


def generate_access_token(openid):
    """
    签名、序列化openid
    :param openid:  openid明文
    :return: token - openid密文
    """
    # 创建序列化对象
    s = Serialzier(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    token = s.dumps(data)
    return token
