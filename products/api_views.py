from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, Category
from .serializers import ProductSerializer, ProductListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """分类API视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="获取所有商品分类",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="创建新的商品分类",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    """商品API视图集"""
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'stock']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @swagger_auto_schema(
        operation_description="获取商品列表",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="按分类筛选",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="按状态筛选",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="搜索商品名称或描述",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="排序字段",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ProductListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取商品详情",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="创建新商品",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="更新商品信息",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="部分更新商品信息",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="删除商品",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取热门商品",
        responses={200: ProductListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取热门商品"""
        featured_products = self.queryset.filter(is_active=True).order_by('-created_at')[:8]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="获取库存不足的商品",
        responses={200: ProductListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """获取库存不足的商品"""
        low_stock_products = self.queryset.filter(stock__lte=10, is_active=True)
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="更新商品库存",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER, description="新库存数量")
            },
            required=['stock']
        ),
        responses={200: ProductSerializer}
    )
    @action(detail=True, methods=['patch'])
    def update_stock(self, request, pk=None):
        """更新商品库存"""
        product = self.get_object()
        new_stock = request.data.get('stock')
        
        if new_stock is None:
            return Response(
                {'error': '库存数量是必需的'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_stock < 0:
            return Response(
                {'error': '库存数量不能为负数'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock = new_stock
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data) 