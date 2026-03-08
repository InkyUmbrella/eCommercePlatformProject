from rest_framework import serializers
from .models import Banner, HotRecommend
from products.serializers import ProductListSerializer

class BannerSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image_url', 'link', 'sort_order']
    
    def get_image_url(self, obj):
        """获取图片完整URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class HotRecommendSerializer(serializers.ModelSerializer):
    """热门推荐序列化器"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = HotRecommend
        fields = ['id', 'product', 'product_id', 'recommend_type', 'sort_order']