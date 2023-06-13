# Create your views here.
from collections import OrderedDict

from django.shortcuts import render
from django.views import View

from contents.models import ContentCategory
from contents.utils import get_categories


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告"""
        # 查询并展示商品分类
        # categories = OrderedDict()
        # channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        # for channel in channels:
        #     group_id = channel.group_id  # 当前组
        #     if group_id not in categories:
        #         categories[group_id] = {'channels': [], 'sub_cats': []}
        #     cat1 = channel.category  # 当前频道的类别
        #     # 追加当前频道
        #     categories[group_id]['channels'].append(
        #         {'id': cat1.id, 'name': cat1.name, 'url': channel.url})
        #     # 构造当前类别的子类别
        #     for cat2 in cat1.subs.all():  # 从一级类别找二级类别
        #         cat2.sub_cats = []  # 二级类别添加一个保存三级类别的列表
        #         for cat3 in cat2.subs.all():
        #             cat2.sub_cats.append(cat3)
        #         categories[group_id]['sub_cats'].append(cat2)
        categories = get_categories()
        # 查询首页广告
        # 查询所有的广告类别
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            # 查询未下架的广告排序
            contents[content_category.key] = content_category.content_set.filter(
                status=True).order_by('sequence')
        # 使用广告类别查询出该类别对应的所有广告内容
        return render(
            request, 'index.html', {
                'categories': categories, 'contents': contents})
