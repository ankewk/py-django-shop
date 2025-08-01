from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消订单"""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'message': '订单已取消'})
        return Response({'error': '只能取消待付款的订单'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """支付订单"""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'paid'
            order.save()
            return Response({'message': '订单已支付'})
        return Response({'error': '只能支付待付款的订单'}, status=status.HTTP_400_BAD_REQUEST) 