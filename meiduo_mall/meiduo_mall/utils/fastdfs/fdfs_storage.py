# -*- coding: utf-8 -*- 
# @Time : 2023/6/11 12:10 
# @Author : 世间无事人
# @File : fdfs_storage.py 
# @description :
from django.conf import settings
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """自定义文件存储类"""

    def __init__(self, fdfs_base_url=None):
        """文件存储类初始化"""
        # if not fdfs_base_url:
        #     self.fdfs_base_url = settings.FDFS_BASE_URL
        # self.fdfs_base_url = fdfs_base_url
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

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
        return settings.FDFS_BASE_URL + name
