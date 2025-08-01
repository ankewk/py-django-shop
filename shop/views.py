from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    """主页视图"""
    return render(request, 'base.html')


def api_root(request):
    """API根路径"""
    return JsonResponse({
        'message': 'Django商城API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'products': '/api/products/',
            'categories': '/api/categories/',
            'orders': '/api/orders/',
        }
    }) 