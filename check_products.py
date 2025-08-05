#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings_mysql')
django.setup()

from products.models import Product, Category
from django.contrib.auth.models import User

def check_data():
    print("=== 检查数据库数据 ===")
    
    # 检查用户
    user_count = User.objects.count()
    print(f"用户数量: {user_count}")
    
    # 检查分类
    category_count = Category.objects.count()
    print(f"分类数量: {category_count}")
    
    if category_count > 0:
        print("现有分类:")
        for cat in Category.objects.all():
            print(f"  - {cat.name}")
    
    # 检查商品
    product_count = Product.objects.count()
    print(f"商品数量: {product_count}")
    
    if product_count > 0:
        print("现有商品:")
        for product in Product.objects.all():
            print(f"  - {product.name} (¥{product.price}) - 分类: {product.category.name}")
    else:
        print("没有商品数据")
        
        # 创建测试数据
        print("\n=== 创建测试数据 ===")
        
        # 创建分类
        if category_count == 0:
            electronics = Category.objects.create(name='电子产品', description='智能手机、电脑等电子设备')
            clothing = Category.objects.create(name='服装鞋包', description='男装、女装、运动鞋等')
            home = Category.objects.create(name='家居用品', description='家具、装饰品等')
            print("创建了3个分类")
        
        # 创建商品
        if product_count == 0:
            # 获取分类
            electronics = Category.objects.get(name='电子产品')
            clothing = Category.objects.get(name='服装鞋包')
            home = Category.objects.get(name='家居用品')
            
            # 创建商品
            Product.objects.create(
                name='iPhone 15 Pro Max',
                description='苹果最新旗舰手机，搭载A17 Pro芯片',
                price=9999.00,
                category=electronics,
                stock=50,
                is_active=True
            )
            
            Product.objects.create(
                name='MacBook Pro 14英寸',
                description='专业级笔记本电脑，适合开发者和设计师',
                price=14999.00,
                category=electronics,
                stock=30,
                is_active=True
            )
            
            Product.objects.create(
                name='Nike Air Max 运动鞋',
                description='经典运动鞋，舒适透气',
                price=899.00,
                category=clothing,
                stock=100,
                is_active=True
            )
            
            Product.objects.create(
                name='小米13 Ultra 手机',
                description='小米旗舰手机，徕卡光学系统',
                price=5999.00,
                category=electronics,
                stock=80,
                is_active=True
            )
            
            Product.objects.create(
                name='戴森 V15 吸尘器',
                description='无线吸尘器，强劲吸力',
                price=4599.00,
                category=home,
                stock=25,
                is_active=True
            )
            
            print("创建了5个测试商品")
    
    print("\n=== 数据检查完成 ===")

if __name__ == '__main__':
    check_data() 