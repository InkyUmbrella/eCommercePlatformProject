<template>
  <div class="product-detail-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <div class="breadcrumb">
          <span class="breadcrumb-item" @click="goHome">❤️ 美妆商城</span>
          <span class="separator">></span>
          <span class="breadcrumb-item current">YSL圣罗兰方管口红</span>
        </div>
      </div>
      <div class="header-right">
        <button class="nav-btn" @click="goHome">🏠 首页</button>
        <button class="nav-btn" @click="goToCart">🛒 购物车</button>
        <button class="nav-btn" @click="goToOrders">📋 订单</button>

        <button class="nav-btn" @click="goToSupport">💬 客服</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
      </div>
    </header>
    <!-- ✅ 新增：成功加入购物车提示条（3秒自动消失） -->
    <div class="success-tip" v-if="showSuccessTip">
      ✅ 成功加入购物车！
    </div>

    <!-- 商品详情主体 -->
    <div class="product-detail-main">
      <!-- 左侧：商品图片 -->
      <div class="product-image-section">
        <div class="product-image">
          <img :src="productData.image" :alt="productData.name" />
        </div>
      </div>

      <!-- 右侧：商品信息 -->
      <div class="product-info-section">
        <h1 class="product-title">{{ productData.name }}</h1>
        <p class="product-subtitle">{{ productData.description }}</p>

        <!-- 价格与库存 -->
        <div class="price-stock">
          <span class="price">¥{{ productData.price }}</span>
          <span class="stock">库存 {{ productData.stock }} 件</span>
        </div>

        <!-- 收货地址 -->
        <div class="address-section">
          <div class="section-title">
            <span class="icon">📍</span>
            <span>收货地址</span>
          </div>
          <div class="address-info">
            <span class="address-text">{{ addressDisplayText }}</span>
            <button class="modify-btn"@click="goToAddressEdit">修改</button>
          </div>
        </div>

        <!-- 购买数量 -->
        <div class="quantity-section">
          <div class="section-title">
            <span class="icon">🛍️</span>
            <span>购买数量</span>
          </div>
          <div class="quantity-control">
            <button class="quantity-btn" @click="decreaseQuantity">-</button>
            <input type="number" v-model="quantity" class="quantity-input" readonly />
            <button class="quantity-btn" @click="increaseQuantity">+</button>
          </div>
        </div>

        <!-- 合计与操作按钮 -->
        <div class="action-section">
          <div class="total-price">
            合计：<span class="total">¥{{ totalPrice }}</span>
          </div>
          <div class="action-buttons">
            <button class="add-to-cart-btn" @click="addToCart">🛒 加入购物车</button>
            <button class="buy-now-btn" @click="buyNow">立即购买</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 服务保障模块 -->
    <div class="service-section">
      <div class="service-item" v-for="service in serviceList" :key="service.id">
        <span class="service-icon">{{ service.icon }}</span>
        <div class="service-text">
          <h4>{{ service.title }}</h4>
          <p>{{ service.desc }}</p>
        </div>
      </div>
    </div>

    <!-- 新增：右下角悬浮留言板按钮 -->
    <div class="cloud-service-btn" @click="goToSupport">
      <span class="btn-icon">📝</span>
      <span class="btn-text">商城客服</span>
    </div>

    <!-- 底部导航 -->
    <footer class="footer">
      <div class="footer-content">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="footer-logo" />
        <span class="footer-text">Beauty</span>
      </div>
      <p class="copyright">© 2026 Beauty All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useCartStore } from '@/store/cartStore';
import * as productApi from '@/api/product';
import * as addressApi from '@/api/address'; // 需要创建

const router = useRouter();
const route = useRoute();
const cartStore = useCartStore();

const productId = computed(() => parseInt(route.params.productId));
const productData = ref({
  id: null,
  name: '',
  description: '',
  price: 0,
  stock: 0,
  image: '',
});
const loading = ref(true);
const error = ref(null);
const quantity = ref(1);
const showSuccessTip = ref(false);
const totalPrice = computed(() => {
  const price = Number(productData.value?.price || 0);
  return (price * quantity.value).toFixed(2);
});
const defaultAddress = ref(null); // 默认地址
const addressDisplayText = computed(() => {
  if (!defaultAddress.value) {
    return '请先添加收货地址';
  }
  const { name, phone_number, address } = defaultAddress.value;
  return [name, phone_number, address].filter(Boolean).join(' ');
});

// 获取商品详情
const fetchProduct = async () => {
  loading.value = true;
  try {
    const data = await productApi.getProductDetail(productId.value);
    productData.value = {
      id: data.id,
      name: data.name,
      description: data.short_description || data.description,
      price: data.price,
      stock: data.stock,
      image: data.cover_image ? (data.cover_image.startsWith('http') ? data.cover_image : import.meta.env.VITE_API_BASE_URL + data.cover_image) : '',
    };
  } catch (err) {
    error.value = err.message;
    ElMessage.error('加载商品详情失败：' + err.message);
    // 跳回列表页
    setTimeout(() => router.push('/products'), 1500);
  } finally {
    loading.value = false;
  }
};

// 获取默认地址（用于显示）
const fetchDefaultAddress = async () => {
  try {
    const addresses = await addressApi.getAddresses();
    const defaultAddr = addresses.find(addr => addr.is_default);
    if (defaultAddr) {
      defaultAddress.value = defaultAddr;
    } else if (addresses.length > 0) {
      defaultAddress.value = addresses[0];
    }
  } catch (err) {
    console.error('获取地址失败', err);
  }
};

onMounted(() => {
  fetchProduct();
  fetchDefaultAddress();
});

watch(
  () => route.query._t,
  (newVal, oldVal) => {
    if (newVal && newVal !== oldVal) {
      fetchDefaultAddress();
    }
  },
);

// 数量增减
const decreaseQuantity = () => {
  if (quantity.value > 1) quantity.value--;
};
const increaseQuantity = () => {
  if (productData.value && quantity.value < productData.value.stock) quantity.value++;
};

// 加入购物车
const addToCart = async () => {
  if (!productData.value) return;
  try {
    await cartStore.addToCart({
      id: productData.value.id,
      name: productData.value.name,
      price: parseFloat(productData.value.price),
      image: productData.value.image,
    }, quantity.value);
    showSuccessTip.value = true;
    setTimeout(() => { showSuccessTip.value = false; }, 3000);
    ElMessage.success('已加入购物车');
  } catch (err) {
    ElMessage.error('加入购物车失败：' + err.message);
  }
};

// 立即购买
const buyNow = () => {
  // 简单跳转，但需要传递商品信息到 checkout 页
  // 可以先将商品加入购物车，然后跳转
  addToCart().then(() => {
    router.push('/checkout');
  });
};

// 地址编辑
const goToAddressEdit = () => {
  router.push({
    name: 'AddressEdit',
    query: {
      addressId: defaultAddress.value?.id,
      redirect: `/product-detail/${productId.value}`,
    },
  });
};

// 其他导航
const goHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToSupport = () => router.push({ name: 'Support', query: { productId: productId.value } });


// 服务保障数据
const serviceList = ref([
  { id: 1, icon: '❤️', title: '品质保障', desc: '精选优质美妆' },
  { id: 2, icon: '🎁', title: '精美包装', desc: '送礼原有心意' },
  { id: 3, icon: '🔄', title: '无忧退换', desc: '7天无理由退换' },
  { id: 4, icon: '🚚', title: '快速配送', desc: '全国顺丰包邮' }
]);
</script>

<style scoped>
/* 全局容器 */
.product-detail-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航栏（与列表页统一） */
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
  font-size: 18px;
  font-weight: 700;
  color: #8b5a42;
  line-height: 1.2;
}
.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}
.breadcrumb-item {
  cursor: pointer;
}
.breadcrumb-item:hover {
  color: #ff69b4;
}
.breadcrumb-item.current {
  color: #ff69b4;
  font-weight: 600;
}
.separator {
  color: #ccc;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
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
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

/* 商品详情主体 */
.product-detail-main {
  display: flex;
  gap: 40px;
  padding: 30px;
  background-color: #fff;
  margin: 20px auto;
  width: 90%;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.15);
}

/* 左侧图片区 */
.product-image-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.product-image {
  width: 300px;
  height: 300px;
  overflow: hidden;
  border-radius: 12px;
}
.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 右侧信息区 */
.product-info-section {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.product-title {
  font-size: 22px;
  color: #333;
  margin: 0;
}
.product-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

/* 价格与库存 */
.price-stock {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #ffe6ef;
}
.price {
  font-size: 24px;
  color: #ff69b4;
  font-weight: bold;
}
.stock {
  font-size: 14px;
  color: #666;
}

/* 地址/数量模块 */
.address-section, .quantity-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #ffe6ef;
}
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}
.icon {
  color: #ff69b4;
}
.address-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.address-text {
  font-size: 14px;
  color: #333;
}
.modify-btn {
  padding: 4px 8px;
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
  border-radius: 4px;
  color: #ff69b4;
  font-size: 12px;
  cursor: pointer;
}

/* 数量控制 */
.quantity-control {
  display: flex;
  align-items: center;
  gap: 10px;
}
.quantity-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
  color: #ff69b4;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.quantity-input {
  width: 40px;
  text-align: center;
  border: 1px solid #ffc0cb;
  border-radius: 4px;
  padding: 4px;
}

/* 操作按钮区 */
.action-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
}
.total-price {
  font-size: 16px;
  color: #666;
}
.total {
  font-size: 20px;
  color: #ff69b4;
  font-weight: bold;
}
.action-buttons {
  display: flex;
  gap: 15px;
}
.add-to-cart-btn {
  padding: 10px 20px;
  background-color: #fff;
  border: 1px solid #ff69b4;
  border-radius: 8px;
  color: #ff69b4;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}
.add-to-cart-btn:hover {
  background-color: #ff69b4;
  color: #fff;
}
.buy-now-btn {
  padding: 10px 25px;
  background-color: #ff69b4;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}
.buy-now-btn:hover {
  background-color: #ff87b8;
}

/* 服务保障模块 */
.service-section {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 20px;
  background-color: #fff9f7;
}
.service-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(255, 192, 203, 0.1);
}
.service-icon {
  font-size: 20px;
  color: #ff69b4;
}
.service-text h4 {
  font-size: 14px;
  color: #333;
  margin: 0 0 4px 0;
}
.service-text p {
  font-size: 12px;
  color: #999;
  margin: 0;
}

/* 底部导航 */
.footer {
  text-align: center;
  padding: 20px;
  background-color: #fff;
  margin-top: 20px;
}
.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}
.footer-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
.footer-text {
  font-size: 16px;
  color: #8b5a42;
  font-weight: 600;
}
.copyright {
  font-size: 12px;
  color: #999;
}
/* 云朵形状悬浮按钮（上移至底部80px） */
.cloud-service-btn {
  position: fixed;
  right: 20px;
  bottom: 80px; /* 保持上移位置，可按需调整 */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px; /* 图标和文字的间距 */
  /* 云朵形状核心：不规则圆角+宽高比 */
  width: 120px; 
  height: 60px;
  border-radius: 30px 30px 20px 30px; /* 左上/右上/右下/左下，模拟云朵弧度 */
  /* 粉色渐变底色，比纯色更有层次感 */
  background: linear-gradient(135deg, #ff87b8 0%, #ff69b4 100%);
  box-shadow: 0 6px 16px rgba(255, 105, 180, 0.4);
  color: #fff;
  cursor: pointer;
  z-index: 999;
  transition: all 0.3s ease;
  /* 云朵小细节：加一个"小凸起"模拟云朵轮廓 */
  position: relative;
}
/* 云朵右侧小凸起 */
.cloud-service-btn::after {
  content: '';
  position: absolute;
  right: 15px;
  top: -10px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff87b8 0%, #ff69b4 100%);
  box-shadow: 0 2px 8px rgba(255, 105, 180, 0.2);
}
/* 悬浮动效：轻微放大+阴影加深+小凸起同步变化 */
.cloud-service-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(255, 105, 180, 0.5);
}
.cloud-service-btn:hover::after {
  transform: scale(1.1);
  right: 12px;
  top: -12px;
}

.btn-icon {
  font-size: 24px;
  margin-bottom: 2px;
}
.btn-text {
  font-size: 12px;
  line-height: 1;
}
/* 成功加入购物车提示条 */
.success-tip {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 8px 15px;
  text-align: center;
  font-size: 14px;
  border-radius: 6px;
  margin: 10px auto;
  width: 90%;
  max-width: 800px;
  box-shadow: 0 2px 6px rgba(46, 125, 50, 0.2);
  z-index: 99;
  position: relative;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .message-board-btn {
    width: 50px;
    height: 50px;
  }
  .btn-icon {
    font-size: 20px;
  }
  .btn-text {
    font-size: 10px;
  }
}
/* 响应式适配 */
@media (max-width: 992px) {
  .product-detail-main {
    flex-direction: column;
    align-items: center;
  }
  .product-image {
    width: 250px;
    height: 250px;
  }
}
</style>
