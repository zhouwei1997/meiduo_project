# Create your views here.
from django import http
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from contents.utils import get_categories
from goods.models import GoodsCategory
from goods.utils import get_breadcrumb


class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """
        查询并渲染商品列表页
        :param request:
        :param category_id: 分类id
        :param page_num: 分页，默认： 1
        :return:
        """
        # 校验category_id的范围
        try:
            # 三级类别
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('参数category_id不存在')
        # 获取排序规则
        sort = request.GET.get('sort', 'default')
        # 根据sort选择排序字段
        if sort == 'price':
            # 按照价格由低到高排序
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低排序
            sort_field = '-sales'
        else:
            sort = 'default'
            sort_field = 'create_time'
        # 查询商品分类
        categories = get_categories()
        # 查询面包屑导航 一级-> 二级-> 三级
        breadcrumb = get_breadcrumb(category)
        # 分页和排序查询：category_id 查询SKU，一查多
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)
        # 创建分页器
        paginator = Paginator(skus, 5)  # skus分页，每页5条
        # 获取到当前用户查看的记录
        page_skus = paginator.page(page_num)  # 获取到page_num页中的五条记录
        # 获取总页数
        total_page = paginator.num_pages
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb
        }
        return render(
            request, 'list.html', context)
