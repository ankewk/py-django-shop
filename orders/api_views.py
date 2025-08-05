from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderListSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """订单API视图集"""
    queryset = Order.objects.prefetch_related('items').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method']
    search_fields = ['order_number', 'customer_name', 'customer_email']
    ordering_fields = ['created_at', 'total', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer

    @swagger_auto_schema(
        operation_description="获取订单列表",
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="按状态筛选",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'payment_method',
                openapi.IN_QUERY,
                description="按支付方式筛选",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="搜索订单号、客户姓名或邮箱",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: OrderListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取订单详情",
        responses={200: OrderSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="创建新订单",
        request_body=OrderSerializer,
        responses={201: OrderSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="更新订单信息",
        request_body=OrderSerializer,
        responses={200: OrderSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="部分更新订单信息",
        request_body=OrderSerializer,
        responses={200: OrderSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="删除订单",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取待处理订单",
        responses={200: OrderListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """获取待处理订单"""
        pending_orders = self.queryset.filter(status='待付款')
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="获取已完成订单",
        responses={200: OrderListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """获取已完成订单"""
        completed_orders = self.queryset.filter(status='已完成')
        serializer = self.get_serializer(completed_orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="更新订单状态",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="新状态",
                    enum=['待付款', '已付款', '已发货', '已完成', '已取消']
                )
            },
            required=['status']
        ),
        responses={200: OrderSerializer}
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """更新订单状态"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status is None:
            return Response(
                {'error': '状态是必需的'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_statuses = ['待付款', '已付款', '已发货', '已完成', '已取消']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'无效的状态，必须是以下之一: {", ".join(valid_statuses)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """订单项API视图集"""
    queryset = OrderItem.objects.select_related('product').all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @swagger_auto_schema(
        operation_description="获取订单项列表",
        responses={200: OrderItemSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取订单项详情",
        responses={200: OrderItemSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs) 