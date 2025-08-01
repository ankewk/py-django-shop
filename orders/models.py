from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='订单号')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    shipping_address = models.TextField(verbose_name='收货地址')
    shipping_phone = models.CharField(max_length=20, verbose_name='收货电话')
    shipping_name = models.CharField(max_length=100, verbose_name='收货人姓名')
    notes = models.TextField(blank=True, verbose_name='订单备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # 生成订单号：年月日时分秒+用户ID后4位
            from datetime import datetime
            now = datetime.now()
            self.order_number = f"{now.strftime('%Y%m%d%H%M%S')}{str(self.user.id).zfill(4)}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.quantity * self.price
        super().save(*args, **kwargs) 