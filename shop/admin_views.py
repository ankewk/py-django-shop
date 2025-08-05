from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.models import User
import datetime

# 安全导入，避免导入错误
try:
    from orders.models import Order
except ImportError:
    Order = None

try:
    from products.models import Product
except ImportError:
    Product = None

@staff_member_required
def admin_dashboard(request):
    """美化的后台管理仪表板"""
    
    # 获取统计数据
    context = {
        'product_count': Product.objects.count() if Product else 0,
        'order_count': Order.objects.count() if Order else 0,
        'user_count': User.objects.count(),
        'server_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # 计算总收入
    if Order:
        total_revenue = Order.objects.filter(
            status__in=['已付款', '已发货', '已完成']
        ).aggregate(total=Sum('total'))['total'] or 0
        context['revenue'] = f"¥{total_revenue:.2f}"
    else:
        context['revenue'] = "¥0.00"
    
    return render(request, 'admin/index.html', context)

@staff_member_required
def admin_products(request):
    """商品管理页面"""
    if not Product:
        context = {
            'products': [],
            'product_count': 0,
            'active_products_count': 0,
            'low_stock_count': 0,
            'total_value': '¥0.00',
            'error': '商品模型未找到'
        }
        return render(request, 'admin/products.html', context)
    
    products = Product.objects.all().order_by('-created_at')
    
    # 计算详细统计
    active_products = products.filter(is_active=True)
    low_stock_products = products.filter(stock__lte=10)
    total_value = sum(product.price * product.stock for product in products)
    
    context = {
        'products': products,
        'product_count': products.count(),
        'active_products_count': active_products.count(),
        'low_stock_count': low_stock_products.count(),
        'total_value': f"¥{total_value:.2f}",
    }
    return render(request, 'admin/products.html', context)

@staff_member_required
def admin_orders(request):
    """订单管理页面"""
    if not Order:
        context = {
            'orders': [],
            'order_count': 0,
            'error': '订单模型未找到'
        }
        return render(request, 'admin/orders.html', context)
    
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
        'order_count': orders.count(),
    }
    return render(request, 'admin/orders.html', context)

@staff_member_required
def admin_users(request):
    """用户管理页面"""
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'user_count': users.count(),
    }
    return render(request, 'admin/users.html', context) 