from django.urls import path
from . import views

urlpatterns = [
    # 分类接口
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # 商品接口
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/new/', views.NewProductListView.as_view(), name='product-new'),
    path('products/hot/', views.HotProductListView.as_view(), name='product-hot'),
    path('products/search/suggest/', views.ProductSearchSuggestView.as_view(), name='product-suggest'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]