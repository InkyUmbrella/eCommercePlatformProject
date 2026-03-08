from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Banner, HotRecommend
from .serializers import BannerSerializer, HotRecommendSerializer

class BannerListView(generics.ListAPIView):
    """轮播图列表接口"""
    serializer_class = BannerSerializer
    pagination_class = None  # 轮播图不分页
    
    def get_queryset(self):
        """只返回启用且排序好的轮播图"""
        return Banner.objects.filter(is_active=True)

class HotRecommendListView(APIView):
    """热门推荐列表接口"""
    
    def get(self, request):
        # 获取请求参数中的类型，默认首页推荐
        recommend_type = request.query_params.get('type', 'home')
        
        # 查询当前有效的推荐
        now = timezone.now()
        recommends = HotRecommend.objects.filter(
            is_active=True,
            recommend_type=recommend_type,
            product__is_active=True  # 只推荐上架的商品
        ).filter(
            # 时间范围判断
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        ).select_related('product').order_by('sort_order')
        
        serializer = HotRecommendSerializer(recommends, many=True, context={'request': request})
        return Response(serializer.data)