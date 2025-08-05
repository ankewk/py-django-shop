#!/usr/bin/env python
"""
Swagger配置测试脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings_mysql')
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

def test_swagger_urls():
    """测试Swagger URL是否可访问"""
    from django.urls import reverse
    
    try:
        # 测试Swagger UI URL
        swagger_url = reverse('schema-swagger-ui')
        print(f"✅ Swagger UI URL: {swagger_url}")
        
        # 测试ReDoc URL
        redoc_url = reverse('schema-redoc')
        print(f"✅ ReDoc URL: {redoc_url}")
        
        # 测试API根URL
        api_root_url = reverse('api_root')
        print(f"✅ API Root URL: {api_root_url}")
        
        print("✅ Swagger配置测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Swagger配置测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    try:
        from products.api_views import ProductViewSet, CategoryViewSet
        from orders.api_views import OrderViewSet, OrderItemViewSet
        
        print("✅ API视图导入成功")
        
        # 测试序列化器
        from products.serializers import ProductSerializer, CategorySerializer
        from orders.serializers import OrderSerializer, OrderItemSerializer
        
        print("✅ 序列化器导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ API端点测试失败: {e}")
        return False

if __name__ == '__main__':
    print("开始Swagger配置测试...")
    
    # 测试Swagger URL
    swagger_ok = test_swagger_urls()
    
    # 测试API端点
    api_ok = test_api_endpoints()
    
    if swagger_ok and api_ok:
        print("\n🎉 所有测试通过！Swagger配置成功！")
        print("\n访问地址:")
        print("- Swagger UI: http://127.0.0.1:8000/api/v1/swagger/")
        print("- ReDoc: http://127.0.0.1:8000/api/v1/redoc/")
        print("- API根: http://127.0.0.1:8000/api/v1/")
    else:
        print("\n❌ 测试失败，请检查配置") 