from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import home, api_root, test, test_static, admin_test, admin_simple_test, admin_vue_test
from .admin_views import admin_dashboard, admin_products, admin_orders, admin_users

urlpatterns = [
    path('', home, name='home'),
    path('test/', test, name='test'),
    path('test-static/', test_static, name='test_static'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api_root'),
    path('api/v1/', include('shop.api_urls')),  # API v1

    # 自定义后台管理路由
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-products/', admin_products, name='admin_products'),
    path('admin-orders/', admin_orders, name='admin_orders'),
    path('admin-users/', admin_users, name='admin_users'),
    path('admin-test/', admin_test, name='admin_test'),
    path('admin-simple-test/', admin_simple_test, name='admin_simple_test'),
    path('admin-vue-test/', admin_vue_test, name='admin_vue_test'),

    # AngularJS 客户端路由 - 所有其他路径都返回主页
    path('products/', TemplateView.as_view(template_name='base.html'), name='products'),
    path('products/<int:id>/', TemplateView.as_view(template_name='base.html'), name='product_detail'),
    path('cart/', TemplateView.as_view(template_name='base.html'), name='cart'),
    path('checkout/', TemplateView.as_view(template_name='base.html'), name='checkout'),
    path('orders/', TemplateView.as_view(template_name='base.html'), name='orders'),
    path('login/', TemplateView.as_view(template_name='base.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='base.html'), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 