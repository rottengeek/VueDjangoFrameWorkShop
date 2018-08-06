from django.views.generic.base import View
from .models import Goods

class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        """
        # json_list = []
        goods = Goods.objects.all()[:10]

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        from django.http import HttpResponse, JsonResponse
        return JsonResponse(json_data, safe=False)
