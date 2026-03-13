<template>
  <div class="product-list-container">
    <!-- 顶部导航栏（与首页完全一致） -->
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <div class="search-bar">
          <span class="search-label">❤️ 美妆分类</span>
          <select class="search-select" v-model="selectedCategory">
            <option value="name">美妆名称</option>
            <option value="brand">品牌</option>
            <option value="price">价格</option>
          </select>
          <input
            type="text"
            placeholder="搜索您心仪的美妆商品"
            class="search-input"
            v-model="searchKeyword"
            @keyup.enter="handleSearch"
          />
          <button class="search-btn" @click="handleSearch">🔍</button>
          <span class="filter-label">⭐ 美妆品牌</span>
          <select class="filter-select" v-model="selectedBrand">
            <option value="">全部品牌</option>
            <option value="SK-II">SK-II</option>
            <option value="Lancôme">兰蔻 (Lancôme)</option>
            <option value="YSL">圣罗兰 (YSL)</option>
            <option value="L'Oréal">巴黎欧莱雅 (L'Oréal Paris)</option>
            <option value="CHANDO">自然堂 (CHANDO)</option>
            <option value="CHANEL">香奈儿 (CHANEL)</option>
          </select>
        </div>
      </div>
      <div class="header-right">
        <button class="nav-btn" @click="goToHome">🏠 首页</button>
        <button class="nav-btn" @click="goToCart">🛒 购物车</button>
        <button class="nav-btn" @click="goToOrders">📋 订单</button>
        <button class="nav-btn" @click="goToProfile">👤 我的</button>
        
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar" />

      </div>
    </header>

    <!-- 面包屑导航 -->
    <div class="breadcrumb">
      <span class="breadcrumb-item" @click="goToHome">首页</span>
      <span class="separator">></span>
      <span class="breadcrumb-item">搜索结果</span>
    </div>

    <!-- 分类筛选信息（动态显示） -->
    <div class="filter-info">
      <p>
        美妆分类：
        <span class="highlight">{{ categoryText }}</span>
        共找到 <span class="highlight">{{ productList.length }}</span> 件美妆
      </p>
    </div>

    <!-- 商品列表 -->
    <div class="product-grid">
      <div class="product-card" v-for="product in productList" :key="product.id"
      @click="goToDetail(product.id)" 
        style="cursor: pointer;" 
      >
        <div class="product-image">
          <img :src="product.image" :alt="product.name" />
        </div>
        <div class="product-info">
          <h4 class="product-name">{{ product.name }}</h4>
          <p class="product-desc">{{ product.description }}</p>
          <div class="product-footer">
            <span class="product-price">¥{{ product.price }}</span>
            <button class="favorite-btn" @click.stop="toggleFavorite(product.id)">
              {{ product.isFavorite ? '❤️' : '🤍' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElPagination } from 'element-plus'; // 假设使用 element-plus
import * as productApi from '@/api/product';

const route = useRoute();
const router = useRouter();

// 搜索筛选
const searchKeyword = ref('');
const selectedCategory = ref('name'); // 此字段实际是搜索类型，但后端可能不支持，需要确认
const selectedBrand = ref('');

// 分页
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);

// 数据
const productList = ref([]);
const loading = ref(false);
const error = ref(null);

// 初始化从路由参数
const initFromRoute = () => {
  searchKeyword.value = route.query.keyword || '';
  selectedCategory.value = route.query.category || 'name';
  selectedBrand.value = route.query.brand || '';
  currentPage.value = parseInt(route.query.page) || 1;
  // pageSize 可能来自路由，但一般不变
};

// 获取商品列表
const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 构建请求参数
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
    };
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value; // 假设后端用 keyword 搜索
    }
    if (selectedBrand.value) {
      params.brand = selectedBrand.value;
    }
    // 如果 selectedCategory 不是 'name'，可能需要传递不同的搜索类型，但先忽略或询问后端
    const res = await productApi.getProducts(params);
    // 假设后端返回格式为 { count: 100, results: [...] }
    productList.value = res.results.map(item => ({
      id: item.id,
      name: item.name,
      description: item.short_description || item.description || '',
      price: item.price,
      image: item.cover_image ? (item.cover_image.startsWith('http') ? item.cover_image : (import.meta.env.VITE_API_BASE_URL + item.cover_image)) : '',
      isFavorite: false, // 暂不实现
    }));
    total.value = res.count;
  } catch (err) {
    error.value = err.message;
    ElMessage.error('加载商品列表失败：' + err.message);
  } finally {
    loading.value = false;
  }
};

// 监听路由变化
watch(() => route.query, () => {
  initFromRoute();
  fetchProducts();
}, { immediate: true });

// 搜索
const handleSearch = () => {
  const query = { ...route.query }; // 保留其他参数
  if (searchKeyword.value.trim()) {
    query.keyword = searchKeyword.value.trim();
  } else {
    delete query.keyword;
  }
  // 品牌
  if (selectedBrand.value) {
    query.brand = selectedBrand.value;
  } else {
    delete query.brand;
  }
  // 分类类型？先忽略
  if (selectedCategory.value !== 'name') {
    query.category_type = selectedCategory.value; // 需要后端支持
  } else {
    delete query.category_type;
  }
  // 重置页码
  query.page = 1;
  router.push({ path: '/products', query });
};

// 分页变化
const handlePageChange = (page) => {
  router.push({ ...route, query: { ...route.query, page } });
};

// 导航
const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToProfile = () => router.push('/profile');
const goToDetail = (id) => router.push({ name: 'ProductDetail', params: { productId: id } });

// 收藏
const toggleFavorite = (id) => {
  const product = productList.value.find(p => p.id === id);
  if (product) product.isFavorite = !product.isFavorite;
};

// 分类文本（保持不变）
const categoryText = computed(() => {
  const map = { name: '美妆名称', brand: '品牌', price: '价格' };
  return map[selectedCategory.value] || '全部';
});



</script>

<style scoped>
/* 全局容器 */
.product-list-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航栏（与首页完全一致） */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 30px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.2);
  box-sizing: border-box;
  width: 100%;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.logo {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
}
.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #8b5a42; /* 统一为深棕色 */
  line-height: 1;
  letter-spacing: 1px;
}
.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 0 20px;
}
.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: nowrap;
}
.search-label, .filter-label {
  color: #ff69b4;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}
.search-select, .filter-select {
  padding: 6px 10px;
  border: 1px solid #ffc0cb;
  border-radius: 6px;
  background-color: #fff;
  font-size: 14px;
  white-space: nowrap;
  width: 100px;
}
.search-input {
  padding: 8px 15px;
  border: 1px solid #ffc0cb;
  border-radius: 6px 0 0 6px;
  width: 320px;
  font-size: 14px;
  outline: none;
}
.search-input:focus {
  border-color: #ff69b4;
}
.search-btn {
  padding: 8px 18px;
  background-color: #ffb6c1;
  border: none;
  border-radius: 0 6px 6px 0;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}
.search-btn:hover {
  background-color: #ff69b4;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-shrink: 0;
}
.nav-btn {
  padding: 6px 10px;
  background: none;
  border: none;
  color: #8b5a42;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 4px;
  transition: all 0.3s;
}
.nav-btn:hover {
  color: #ff69b4;
  background-color: #fff0f5;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ffc0cb;
}

/* 面包屑导航 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px 30px;
  font-size: 14px;
  color: #666;
}
.breadcrumb-item {
  cursor: pointer;
}
.breadcrumb-item:hover {
  color: #ff69b4;
}
.separator {
  color: #ccc;
}

/* 分类筛选信息 */
.filter-info {
  padding: 0 30px 20px;
  font-size: 16px;
  color: #666;
}
.highlight {
  color: #ff69b4;
  font-weight: 600;
}

/* 商品列表网格 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 0 30px 30px;
}


/* 商品卡片 */
.product-card {
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.15);
  transition: box-shadow 0.3s ease;
}
.product-card:hover {
  box-shadow: 0 4px 12px rgba(255, 192, 203, 0.25);
}
.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}
.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px 12px 0 0;
}
.product-info {
  padding: 15px;
}
.product-name {
  font-size: 15px;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.product-desc {
  font-size: 12px;
  color: #999;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.product-price {
  font-size: 18px;
  color: #ff69b4;
  font-weight: bold;
}
.favorite-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #ff69b4;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-center {
    display: none; /* 小屏隐藏搜索栏 */
  }
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    padding: 0 15px 20px;
  }
}
</style>