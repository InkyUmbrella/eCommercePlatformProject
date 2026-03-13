<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <div class="search-bar">
          <span class="search-label">❤️ 美妆分类</span>
          <select class="search-select">
            <option>美妆名称</option>
            <option>品牌</option>
            <option>价格</option>
          </select>
          <input 
          type="text" 
          placeholder="搜索您心仪的美妆商品" 
          class="search-input" 
            v-model="searchKeyword"
            @keyup.enter="handleSearch"   
          />
          <button class="search-btn"@click="handleSearch">🔍</button>
          <span class="filter-label">⭐ 美妆品牌</span>
          <select class="filter-select"v-model="selectedBrand">
            <option value>全部品牌</option>
            <option value>SK-II</option>
            <option value>兰蔻 (Lancôme)</option>
            <option value>圣罗兰 (YSL)</option>
            <option value>巴黎欧莱雅 (L'Oréal Paris)</option>
            <option value>自然堂 (CHANDO)</option>
            <option value>香奈儿 (CHANEL)</option>
          </select>
        </div>
      </div>
      <div class="header-right">
        <button class="nav-btn" @click="goToHome">🏠 首页</button>
        <button class="nav-btn" @click="goToCart">🛒 购物车</button>
        <button class="nav-btn" @click="goToOrders">📋 订单</button>

        <button class="nav-btn" @click="goToProfile">👤 我的</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
         
      </div>
    </header>
        <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- 主页内容 -->
    <template v-else>
      <!-- 轮播图 -->
      <div class="carousel">
        <div
          class="carousel-item"
          v-for="(item, index) in banners"
          :key="index"
          :class="{ active: index === currentIndex }"
        >
          <img :src="item.image" :alt="item.title" class="carousel-img" />
          <div class="carousel-text">
            <h3>{{ item.title }}</h3>
            <p>{{ item.subtitle }}</p>
            <button class="carousel-btn" @click="handleCarouselClick(item.link)">
              {{ item.btnText }}
            </button>
          </div>
        </div>
        <div class="carousel-dots">
          <span
            class="dot"
            v-for="(_, index) in banners"
            :key="index"
            :class="{ active: index === currentIndex }"
            @click="goToSlide(index)"
          ></span>
        </div>
      </div>

      <!-- 新品上架模块 -->
      <section class="new-products">
        <div class="section-title">
          <h2>新品上架</h2>
          <div class="carousel-controls">
            <button class="control-btn" @click="prevProduct">←</button>
            <button class="control-btn" @click="nextProduct">→</button>
          </div>
        </div>
        <div class="product-list">
          <div
            class="product-card"
            v-for="(product, index) in newProducts"
            :key="index"
          >
            <div class="product-badge" v-if="product.is_new">新品</div>
            <img :src="product.image" :alt="product.name" class="product-img" />
            <p class="product-name">{{ product.name }}</p>
            <p class="product-price">¥{{ product.price }}</p>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import * as homeApi from '@/api/home';
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
banners.value = bannersRes.map(item => ({
  ...item,
  image: item.image.startsWith('http') ? item.image : baseURL + item.image
}));
const router = useRouter();

// 数据
const banners = ref([]);
const newProducts = ref([]);
const loading = ref(true);
const error = ref(null);

// 轮播图索引
const currentIndex = ref(0);
let autoPlayTimer = null;

// 搜索（保持不变）
const searchKeyword = ref('');
const selectedCategory = ref('name');
const selectedBrand = ref('');

// 获取主页数据
const fetchHomeData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const [bannersRes, newProductsRes] = await Promise.all([
      homeApi.getBanners(),
      homeApi.getNewProducts()
    ]);

    // 映射轮播图字段（根据实际返回调整）
    banners.value = bannersRes.map(item => ({
      image: item.image,           // 假设返回的是完整URL或需要拼接
      title: item.title,
      subtitle: item.subtitle,
      btnText: item.btn_text,      // 后端字段可能是 btn_text
      link: item.link
    }));

    // 映射新品商品字段
    newProducts.value = newProductsRes.map(item => ({
      id: item.id,
      name: item.name,              // 如果后端是 title，改为 item.title
      price: item.price,            // 价格可能是字符串或数字
      image: item.cover_image,      // 如果后端是 cover，改为 item.cover
      is_new: item.is_new || false  // 如果后端没有 is_new，可以去掉badge
    }));
  } catch (err) {
    error.value = err.message;
    ElMessage.error('加载主页数据失败：' + err.message);
  } finally {
    loading.value = false;
  }
};

// 如果图片是相对路径，需要拼接完整地址
const getFullImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  // 拼接后端地址（从环境变量或固定配置读取）
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
  return baseURL + path;
};

onMounted(() => {
  fetchHomeData();
  startAutoPlay();

  const carouselDom = document.querySelector('.carousel');
  carouselDom?.addEventListener('mouseenter', stopAutoPlay);
  carouselDom?.addEventListener('mouseleave', startAutoPlay);
});

onUnmounted(() => {
  stopAutoPlay();
  const carouselDom = document.querySelector('.carousel');
  carouselDom?.removeEventListener('mouseenter', stopAutoPlay);
  carouselDom?.removeEventListener('mouseleave', startAutoPlay);
});

// 轮播自动播放
const startAutoPlay = () => {
  if (autoPlayTimer) clearInterval(autoPlayTimer);
  if (banners.value.length === 0) return;
  autoPlayTimer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % banners.value.length;
  }, 3000);
};
const stopAutoPlay = () => {
  clearInterval(autoPlayTimer);
};
const goToSlide = (index) => {
  currentIndex.value = index;
  stopAutoPlay();
  startAutoPlay();
};

// 轮播按钮点击
const handleCarouselClick = (link) => {
  if (link && link !== '#') router.push(link);
};

// 搜索
const handleSearch = () => {
  const query = {};
  if (searchKeyword.value.trim()) query.keyword = searchKeyword.value.trim();
  if (selectedCategory.value !== 'name') query.category = selectedCategory.value;
  if (selectedBrand.value) query.brand = selectedBrand.value;
  router.push({ path: '/products', query });
};

// 导航
const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToProfile = () => router.push('/profile');
</script>

<style scoped>
/* 全局容器 */
.home-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
/* 顶部导航栏 - 核心调整间距和排版 */
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
.loading {
  text-align: center;
  padding: 50px;
  color: #ff69b4;
}
.error {
  text-align: center;
  padding: 50px;
  color: red;
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

/* 轮播图（图二效果） */
.carousel {
  position: relative;
  width: 95%; /* 略窄于容器，更美观 */
  height: 300px;
  overflow: hidden;
  margin: 20px auto; /* 水平居中 */
  border-radius: 12px; /* 加圆角，和整体风格统一 */
}
.carousel-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.carousel-item.active {
  opacity: 1;
}
.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.carousel-text {
  position: absolute;
  bottom: 40px;
  left: 40px;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4); /* 加深阴影，文字更清晰 */
}
.carousel-text h3 {
  font-size: 26px;
  margin-bottom: 8px;
  font-weight: 700;
}
.carousel-text p {
  font-size: 15px;
  margin-bottom: 15px;
}
.carousel-btn {
  padding: 10px 22px;
  background-color: #FF69B4;
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
}
.carousel-btn:hover {
  background-color: #FF87B8;
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.5);
  transform: translateY(-2px); /* 轻微上浮，更有交互感 */
}
.carousel-dots {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s;
}
.dot.active {
  background-color: #ff69b4;
  width: 22px;
  border-radius: 5px; /* 激活态变椭圆，更醒目 */
}
/* 新品上架模块 */
.new-products {
  padding: 0 30px 20px;
}
.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ffe6ef; /* 加底部分割线，排版更清晰 */
}
.heart {
  color: #ff69b4;
  font-size: 20px;
  margin-right: 8px;
}
.section-title h2 {
  font-size: 20px;
  color: #333;
  font-weight: 600;
  margin: 0;
}
.carousel-controls {
  display: flex;
  gap: 10px;
}
.control-btn {
  padding: 6px 12px;
  background-color: #fff;
  border: 1px solid #ffc0cb;
  border-radius: 6px;
  cursor: pointer;
  color: #ff69b4;
  transition: all 0.3s;
}
.control-btn:hover {
  background-color: #fff0f5;
  border-color: #ff69b4;
}
.product-list {
  display: flex;
  gap: 22px; /* 加大商品卡片间距 */
  overflow-x: auto;
  scroll-behavior: smooth;
  padding-bottom: 15px;
  scrollbar-width: thin; /* 美化滚动条 */
  scrollbar-color: #ffc0cb #fff0f5;
}
/* 美化webkit滚动条 */
.product-list::-webkit-scrollbar {
  height: 6px;
}
.product-list::-webkit-scrollbar-thumb {
  background-color: #ffc0cb;
  border-radius: 3px;
}
.product-list::-webkit-scrollbar-track {
  background-color: #fff0f5;
}
.product-card {
  min-width: 200px;
  background-color: #fff;
  border-radius: 10px; /* 加大圆角，更精致 */
  box-shadow: 0 3px 10px rgba(255, 192, 203, 0.15);
  padding: 12px;
  position: relative;
  transition: box-shadow 0.3s;
}
.product-card:hover {
  box-shadow: 0 5px 15px rgba(255, 192, 203, 0.25); /* 卡片悬浮阴影，提升质感 */
}
.product-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background-color: #ff69b4;
  color: #fff;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}
.product-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 12px;
}
.product-name {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* 文字超出省略 */
}
.product-price {
  font-size: 16px;
  color: #ff69b4;
  font-weight: bold;
  margin: 0;
}
/* 响应式适配 - 小屏幕不拥挤 */
@media (max-width: 1200px) {
  .search-input {
    width: 250px;
  }
  .header {
    padding: 12px 20px;
  }
}
@media (max-width: 992px) {
  .search-select, .filter-select {
    width: 80px;
  }
  .search-input {
    width: 200px;
  }
  .header-right {
    gap: 12px;
  }
}
</style>