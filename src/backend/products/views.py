from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from .models import Category, Product
from .serializers import (
    CategorySerializer, 
    ProductListSerializer, 
    ProductDetailSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    """自定义分页类"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryListView(generics.ListAPIView):
    """分类列表接口"""
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    pagination_class = None

class ProductListView(generics.ListAPIView):
    """商品列表接口 - 支持搜索、筛选、排序、分页"""
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 过滤字段
    filterset_fields = {
        'category_id': ['exact'],
        'is_active': ['exact'],
        'is_new': ['exact'],
        'is_hot': ['exact'],
        'price': ['gte', 'lte'],
        'brand': ['exact'],
    }
    
    # 搜索字段
    search_fields = ['name', 'sku', 'description', 'brand']
    
    # 排序字段
    ordering_fields = ['price', 'created_at', 'sales_count', 'rating']
    ordering = ['-created_at']  # 默认排序
    
    def get_queryset(self):
        """获取查询集，只返回上架商品"""
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # 关键词搜索增强
        keyword = self.request.query_params.get('search', None)
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(sku__icontains=keyword) |
                Q(brand__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    """商品详情接口"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    
    def get_queryset(self):
        """优化查询，预加载关联数据"""
        return Product.objects.filter(is_active=True).select_related(
            'category'
        ).prefetch_related(
            'images',
            'specs'
        )
    
    def retrieve(self, request, *args, **kwargs):
        """重写retrieve方法，可以添加自定义逻辑"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 可以在这里添加相关推荐商品
        related_products = Product.objects.filter(
            category=instance.category,
            is_active=True
        ).exclude(id=instance.id)[:4]
        
        related_serializer = ProductListSerializer(
            related_products, 
            many=True, 
            context={'request': request}
        )
        
        data = serializer.data
        data['related_products'] = related_serializer.data
        
        return Response(data)

# 新增：新品推荐接口
class NewProductListView(generics.ListAPIView):
    """新品列表接口"""
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True, 
            is_new=True
        ).select_related('category')[:20]

# 新增：热卖商品接口
class HotProductListView(generics.ListAPIView):
    """热卖商品列表接口"""
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True, 
            is_hot=True
        ).select_related('category')[:20]

# 新增：商品搜索建议接口
class ProductSearchSuggestView(generics.ListAPIView):
    """商品搜索建议接口"""
    serializer_class = ProductListSerializer
    pagination_class = None
    
    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        if len(keyword) < 2:
            return Product.objects.none()
        
        return Product.objects.filter(
            Q(is_active=True) &
            (Q(name__icontains=keyword) | Q(brand__icontains=keyword))
        )[:10]