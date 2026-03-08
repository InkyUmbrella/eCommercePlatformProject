from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductSpecification

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children', 'sort_order']
    
    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data

class ProductImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'sort_order', 'is_main']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProductSpecificationSerializer(serializers.ModelSerializer):
    """商品规格序列化器"""
    class Meta:
        model = ProductSpecification
        fields = ['id', 'name', 'value', 'price_adjust', 'stock', 'image', 'sort_order']

class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器（精简版）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'price', 'market_price', 
            'cover_image_url', 'stock', 'is_active', 
            'category', 'category_name', 'short_description',
            'sales_count', 'rating', 'is_new', 'is_hot'
        ]
    
    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器（完整版）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecificationSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'brand', 'model',
            'price', 'market_price', 'cost_price',
            'stock', 'stock_warning', 'sales_count', 'view_count',
            'rating', 'review_count',
            'cover_image_url', 'video_url',
            'images', 'specs',
            'description', 'short_description', 'specifications',
            'is_active', 'is_new', 'is_hot', 'is_recommend',
            'category', 'category_name',
            'created_at', 'updated_at', 'published_at'
        ]
    
    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def to_representation(self, instance):
        """增加浏览次数"""
        # 每次访问详情时增加浏览次数
        from django.db.models import F
        Product.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        return super().to_representation(instance)