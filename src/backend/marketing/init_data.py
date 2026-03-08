import os
import django
from django.core.files import File
from django.utils import timezone

def init_marketing_data():
    """初始化营销数据（轮播图、热门推荐）"""
    from products.models import Product
    from marketing.models import Banner, HotRecommend
    
    print("开始初始化营销数据...")
    
    # 获取所有商品（假设已经有商品数据）
    products = Product.objects.all()
    if not products.exists():
        print("警告：没有商品数据，请先创建商品！")
        return
    
    # 创建轮播图（如果没有）
    if not Banner.objects.exists():
        banners_data = [
            {
                'title': '夏季新品上市',
                'link': '/products/?category=1',
                'sort_order': 1,
            },
            {
                'title': '限时特惠',
                'link': '/products/?price__lte=1000',
                'sort_order': 2,
            },
            {
                'title': '热门推荐',
                'link': '/recommends/',
                'sort_order': 3,
            }
        ]
        
        for banner_data in banners_data:
            # 注意：实际图片需要手动上传，这里只创建记录
            banner = Banner.objects.create(
                title=banner_data['title'],
                link=banner_data['link'],
                sort_order=banner_data['sort_order'],
                is_active=True
            )
            print(f"创建轮播图: {banner.title}")
    
    # 创建热门推荐
    if not HotRecommend.objects.exists():
        recommend_types = ['home', 'category', 'detail']
        
        for idx, product in enumerate(products[:6]):  # 取前6个商品
            recommend_type = recommend_types[idx % 3]  # 轮流分配不同类型
            HotRecommend.objects.get_or_create(
                product=product,
                recommend_type=recommend_type,
                defaults={
                    'sort_order': idx,
                    'is_active': True
                }
            )
            print(f"创建热门推荐: {recommend_type} - {product.name}")
    
    print(f"营销数据初始化完成！")
    print(f"轮播图数量: {Banner.objects.count()}")
    print(f"热门推荐数量: {HotRecommend.objects.count()}")

if __name__ == '__main__':
    # 设置Django环境
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendCore.settings')
    django.setup()
    init_marketing_data()