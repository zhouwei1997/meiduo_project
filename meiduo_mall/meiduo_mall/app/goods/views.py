# Create your views here.
import datetime
import logging

from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from contents.utils import get_categories
from goods.models import GoodsCategory, SKU, GoodsVisitCount
from goods.utils import get_breadcrumb
from meiduo_mall.utils.response_code import RETCODE

logger = logging.getLogger('django')


class DetailVisitView(View):
    """统计商品分类访问量"""

    def post(self, request, category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id 不存在')
        # 获取当天的日期
        t = timezone.localtime()
        # 获取当天的时间字符串
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        # 将当天的时间字符串转成时间对象datetime，为了跟date字段的类型匹配 2019:05:23  2019-05-23
        # 时间字符串转时间对象；datetime.strftime() # 时间对象转时间字符串
        today_date = datetime.strptime(today_str, '%Y-%m-%d')
        # 判断当天指定的分类商品对应的记录是否存在
        try:
            counts_date = GoodsVisitCount.objects.get(
                data=today_date, category=category)
        except GoodsCategory.DoesNotExist:
            counts_date = GoodsVisitCount()
        try:
            counts_date.category = category
            counts_date.count += 1
            counts_date.date = today_date
            counts_date.save()
        except Exception as e:
            return http.HttpResponseServerError('统计失败')
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK'
        })


class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist as e:
            logger.error(e)
            return render(request, '404.html')
        # 查询商品分类
        categories = get_categories()
        breadcrumb = get_breadcrumb(sku.category)
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格商品
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不在继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制道歉sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找复合道歉规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs
        }
        return render(request, 'detail.html', context)


class HotGoodsView(View):
    """商品热销排行"""

    def get(self, request, category_id):
        # 查询指定分类的SKU信息，而且必须是上架的状态，然后按照销量由高到低排序，最后切片取出前两位
        skus = SKU.objects.filter(
            category_id=category_id, is_launched=True).order_by('-sales')[:2]
        # 模型列表转字典
        hot_skus = []
        for sku in skus:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            }
            hot_skus.append(sku_dict)
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'hot_skus': hot_skus
        })


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
        try:
            # 获取到当前用户查看的记录
            page_skus = paginator.page(page_num)  # 获取到page_num页中的五条记录
        except EmptyPage:
            return http.HttpResponseNotFound('EmptyPage 页码不存在')
        # 获取总页数
        total_page = paginator.num_pages
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'page_skus': page_skus,
            'total_page': total_page,
            'page_num': page_num,
            'sort': sort,
            'category_id': category_id
        }
        return render(
            request, 'list.html', context)
