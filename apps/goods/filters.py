import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    自定义过滤类
    """
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte',help_text='最高价格')
    # 行为: 名称中包含某字符，且字符不区分大小写
    # name = django_filters.CharFilter(name="name", lookup_expr="icontains")
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级目录二级目录还是三级目录。
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'is_hot','is_new']
