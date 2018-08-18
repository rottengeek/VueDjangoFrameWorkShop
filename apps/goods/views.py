from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

from goods.serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, \
    IndexCategorySerializer
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页
    """
    # queryset是一个属性
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 设置列表页的单独auth认证
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 设置排序
    ordering_fields = ('sold_num', 'shop_price')
    filter_class = GoodsFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取已经被我们设置顶部导航的数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
