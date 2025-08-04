from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import home, api_root, test, test_static

urlpatterns = [
    path('', home, name='home'),
    path('test/', test, name='test'),
    path('test-static/', test_static, name='test_static'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api_root'),
    
    # AngularJS 客户端路由 - 所有其他路径都返回主页
    path('products/', TemplateView.as_view(template_name='base.html'), name='products'),
    path('products/<int:id>/', TemplateView.as_view(template_name='base.html'), name='product_detail'),
    path('orders/', TemplateView.as_view(template_name='base.html'), name='orders'),
    path('login/', TemplateView.as_view(template_name='base.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='base.html'), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 