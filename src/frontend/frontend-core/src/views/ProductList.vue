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

const route = useRoute();
const router = useRouter();

const goToDetail = (productId) => {
  router.push({
    name: 'ProductDetail', 
    params: { productId: productId } 
  });
};

const goToLogin = () => {
  router.push('/login');
};

// 搜索相关变量
const searchKeyword = ref('');
const selectedCategory = ref('name');
const selectedBrand = ref('');

// 从路由参数初始化
const initFromRoute = () => {
  searchKeyword.value = route.query.keyword || '';
  selectedCategory.value = route.query.category || 'name';
  selectedBrand.value = route.query.brand || '';
};
initFromRoute(); // 初始化
watch(() => route.query, initFromRoute, { immediate: true });

// 处理搜索
const handleSearch = () => {
  const query = {};
  if (searchKeyword.value.trim()) {
    query.keyword = searchKeyword.value.trim();
  }
  if (selectedCategory.value !== 'name') {
    query.category = selectedCategory.value;
  }
  if (selectedBrand.value) {
    query.brand = selectedBrand.value;
  }
  router.push({ path: '/products', query });
};

// 导航
const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToProfile = () => router.push('/profile');

// 分类文本显示（用于筛选信息）
const categoryText = computed(() => {
  const map = {
    name: '美妆名称',
    brand: '品牌',
    price: '价格'
  };
  return map[selectedCategory.value] || '全部';
});

// 商品列表数据（示例）
const productList = ref([
  {
    id: 1,
    name: '古驰红礼盒金绒雾217唇膏',
    description: '古驰 (GUCCI) 元旦新年礼物口红红礼盒金绒...',
    price: '202',
    image: new URL('@/assets/product/gucci.jpg', import.meta.url).href,
    isFavorite: false
  },
  {
    id: 2,
    name: 'YSL圣罗兰方管口红',
    description: 'YSL圣罗兰方管口红 唇霜N*M裸缪斯化妆...',
    price: '410',
    image: new URL('@/assets/product/ysl.jpg', import.meta.url).href,
    isFavorite: false
  },
  {
    id: 3,
    name: '迪奥DIOR烈艳蓝金唇膏高订口红',
    description: '迪奥DIOR【享随身色】烈艳蓝金唇膏高订...',
    price: '790',
    image: new URL('@/assets/product/dior.jpg', import.meta.url).href,
    isFavorite: false
  },
  {
    id: 4,
    name: '兰蔻箐纯柔雾水唇釉',
    description: '兰蔻箐纯柔雾水唇釉   196/296丝...',
    price: '380',
    image: new URL('@/assets/product/lan.png', import.meta.url).href,
    isFavorite: false
  }
]);

// 收藏功能
const toggleFavorite = (id) => {
  const product = productList.value.find(p => p.id === id);
  if (product) {
    product.isFavorite = !product.isFavorite;
  }
};
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