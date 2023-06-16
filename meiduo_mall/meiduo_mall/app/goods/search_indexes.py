# -*- coding: utf-8 -*- 
# @Time : 2023/6/16 19:52 
# @Author : 世间无事人
# @File : search_indexes.py 
# @description : SKU信息全文检索,存放索引类
from haystack import indexes

from goods.models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)
