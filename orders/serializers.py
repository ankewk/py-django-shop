from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_phone', 'shipping_name', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # 计算总金额
        total_amount = 0
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            product = Product.objects.get(id=product_id)
            total_amount += product.price * quantity
        
        # 创建订单
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        
        # 创建订单项
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            product = Product.objects.get(id=product_id)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
                total_price=product.price * quantity
            )
        
        return order 