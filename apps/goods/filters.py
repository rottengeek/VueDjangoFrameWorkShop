import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    自定义过滤类
    """
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    # 行为: 名称中包含某字符，且字符不区分大小写
    name = django_filters.CharFilter(name="name", lookup_expr="icontains")
    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']
