"""VueDjangoFrameWorkShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from extra_apps import xadmin
from django.views.static import serve

from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewset, HotSearchsViewset, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset
from trade.views import AlipayView
from VueDjangoFrameWorkShop.settings import MEDIA_ROOT

# STATIC_ROOT

router = DefaultRouter()

# 配置goods的url,这个basename是干啥的
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置Category的url
router.register(r'categorys', CategoryViewset, base_name="categorys")

# 热搜词
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

# 配置codes的url
router.register(r'codes', SmsCodeViewset, base_name="codes")

# 配置users的url
router.register(r'users', UserViewset, base_name="users")

# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")

# 收货地址
router.register(r'address', AddressViewset, base_name="address")

# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 订单相关url
router.register(r'orders', OrderViewset, base_name="orders")

# 首页banner轮播图url
router.register(r'banners', BannerViewset, base_name="banners")

# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    # rest 登录的
    path('api-auth/', include('rest_framework.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    re_path('^', include(router.urls)),

    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),

    path('docs/', include_docs_urls(title='慕学生鲜文档')),

    # drf 自带的token认证模式
    path('api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    path('login/', obtain_jwt_token),

    # 支付宝支付相关接口
    path('alipay/return/', AlipayView.as_view(), name='alipay'),

]
