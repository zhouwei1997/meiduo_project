# -*- coding: utf-8 -*- 
# @Time : 2023/6/11 12:10 
# @Author : 世间无事人
# @File : fdfs_storage.py 
# @description :
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """自定义文件存储类"""

    # def __init__(self, option=None):
    #     """文件存储类初始化"""
    #     if not option:
    #         option = settings.CUSTOM_STORAGE_OPTIONS
    #     pass

    def _open(self, name, mode='rb'):
        """
        打开文件
        :param name: 文件路径
        :param mode: 文件打开方式
        :return: None
        """
        pass

    def _save(self, name, content):
        """
        保存文件时调用
        :param name: 文件路径
        :param content: 文件二进制内容
        :return:
        """
        pass

    def url(self, name):
        """
        返回文件的全路径
        :param name: 文件相对路径
        :return: 文件全路径
        """
        return 'http://192.168.183.10:88/' + name
