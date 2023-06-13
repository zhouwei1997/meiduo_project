# -*- coding: utf-8 -*- 
# @Time : 2023/6/13 20:07 
# @Author : 世间无事人
# @File : utils.py 
# @description :
from collections import OrderedDict

from goods.models import GoodsChannel


def get_categories():
    """获取商品分类"""
    # 查询并展示商品分类
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}
        cat1 = channel.category  # 当前频道的类别
        # 追加当前频道
        categories[group_id]['channels'].append(
            {'id': cat1.id, 'name': cat1.name, 'url': channel.url})
        # 构造当前类别的子类别
        for cat2 in cat1.subs.all():  # 从一级类别找二级类别
            cat2.sub_cats = []  # 二级类别添加一个保存三级类别的列表
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)
    return categories
