from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='商品名称')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='分类')
    stock = models.PositiveIntegerField(default=0, verbose_name='库存')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='商品')
    image_url = models.URLField(blank=True, verbose_name='图片URL')
    is_primary = models.BooleanField(default=False, verbose_name='是否主图')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - {self.image.name}" 