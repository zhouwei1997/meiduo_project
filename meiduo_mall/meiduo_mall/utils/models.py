# -*- coding: utf-8 -*- 
# @Time : 2023/5/18 21:32 
# @Author : 世间无事人
# @File : models.py
# @description :
from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 表示是抽象模型类，用于继承使用，数据库迁移时不会创建表
