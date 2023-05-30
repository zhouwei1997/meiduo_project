# Create your views here.
import logging

from django import http
from django.core.cache import cache
from django.views import View

from areas import constants
from areas.models import Area
from utils.response_code import RETCODE

logger = logging.getLogger('django')


class AreaView(View):
    """省市区三级联动"""

    def get(self, request):
        # 判断当前是查询省/市区
        area_id = request.GET.get('area_id')
        if not area_id:
            # 获取并判断是否有缓存
            province_list = cache.get('province_list')
            if not province_list:
                # 查询省级数据
                try:
                    province_model_list = Area.objects.filter(
                        parent_id__isnull=True)
                    province_list = []
                    for provice_model in province_model_list:
                        provice_dict = {
                            "id": provice_model.id,
                            "name": provice_model.name
                        }
                        province_list.append(provice_dict)
                        # 缓存省份字典列表数据
                        cache.set('province_list', province_list, constants.CACHE_EXPIRES)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse(
                        {'code': RETCODE.DBERR, 'errmsg': '查询省份数据错误'})
            return http.JsonResponse(
                {'code': RETCODE.OK, 'errmsg': 'OK', 'provice_list': province_list})
        else:
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    # 查询市区数据
                    parent_model = Area.objects.get(id=area_id)
                    sub_model_list = parent_model.subs.all()
                    # 将子集模型列表转成列表
                    subs = []
                    for sub_model in sub_model_list:
                        sub_dict = {
                            'id': sub_model.id,
                            'name': sub_model.name
                        }
                        subs.append(sub_dict)
                    # 构造子集json数据
                    sub_data = {
                        'id': parent_model.id,
                        'name': parent_model.name,
                        'subs': subs
                    }
                    # 缓存城市/区县数据
                    cache.set('sub_area_' + area_id, sub_data, constants.CACHE_EXPIRES)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({
                        'code': RETCODE.DBERR,
                        'errmsg': '查询城市/区县数据错误'
                    })
            return http.JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'sub_data': sub_data
            })
