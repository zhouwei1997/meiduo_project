# Create your views here.
import logging

from django import http
from django.views import View

from areas.models import Area
from utils.response_code import RETCODE

logger = logging.getLogger('django')


class AreaView(View):
    """省市区三级联动"""

    def get(self, request):
        # 判断当前是查询省/市区
        area_id = request.GET.get('area_id')
        if not area_id:
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
                return http.JsonResponse(
                    {'code': RETCODE.OK, 'errmsg': 'OK', 'provice_list': province_list})
            except Exception as e:
                logger.error(e)
                return http.JsonResponse(
                    {'code': RETCODE.DBERR, 'errmsg': '查询省份数据错误'})
        else:
            # 查询市区数据
            pass
