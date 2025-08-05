from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    """主页视图"""
    return render(request, 'base.html')

def api_root(request):
    """API根路径"""
    return JsonResponse({
        'message': 'Django商城API',
        'version': '1.0.0'
    })

def test(request):
    """测试页面"""
    return render(request, 'test.html')

def test_static(request):
    """静态文件测试页面"""
    return render(request, 'simple_test.html')

def admin_test(request):
    return render(request, 'admin/test.html')

def admin_simple_test(request):
    return render(request, 'admin/simple_test.html')

def admin_vue_test(request):
    return render(request, 'admin/vue_test.html') 