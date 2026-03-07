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

        <button class="nav-btn" @click="goToProfile">👤 我的</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
      </div>
    </header>

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
            <span class="address-text">北京市 市辖区 东城区 (某小区)</span>
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
import { ref, computed, onMounted } from 'vue';  
import { useRouter,useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute(); 
// 跳转到地址修改页（可传递地址ID）
const goToAddressEdit = () => {
  router.push({
    name: 'AddressEdit',
    query: { addressId: '1001' } // 传递要修改的地址ID
  });
};
// ✅ 1. 接收路由参数 - 同时兼容props和route.params（双重保障）
const props = defineProps({
  productId: {
    type: [String, Number], // 兼容字符串/数字ID，彻底解决类型不匹配
    required: true
  }
});
// 模拟商品总数据（实际项目中从后端接口获取）
const allProducts = ref([
  {
    id: 1,
    name: '古驰红礼盒金绒雾217唇膏',
    description: '古驰 (GUCCI) 元旦新年礼物口红红礼盒金绒...',
    price: '202',
    stock: '300',
    image: new URL('@/assets/product/gucci.jpg', import.meta.url).href
  },
  {
    id: 2,
    name: 'YSL圣罗兰方管口红',
    description: 'YSL圣罗兰方管口红 唇霜NM裸缪斯化妆品生日礼盒女生',
    price: '410',
    stock: '450',
    image: new URL('@/assets/product/ysl.jpg', import.meta.url).href
  },
  {
    id: 3,
    name: '迪奥DIOR烈艳蓝金唇膏高订口红',
    description: '迪奥DIOR【享随身色】烈艳蓝金唇膏高订...',
    price: '790',
    stock: '200',
    image: new URL('@/assets/product/dior.jpg', import.meta.url).href
  },
  {
    id: 4,
    name: '兰蔻菁纯唇膏90周年限定口红',
    description: '兰蔻菁纯唇膏90周年限定口红 196/296丝...',
    price: '380',
    stock: '150',
    image: new URL('@/assets/product/lan.png', import.meta.url).href
  }
]);
// ✅ 3. 商品数据+兜底初始化（避免空白）
const productData = ref({
  name: '加载中...',
  description: '请稍等',
  price: '0.00',
  stock: '0',
  image: new URL('@/assets/bg-makeup', import.meta.url).href // 可选：加个加载图
});

// 核心：根据ID加载商品 - 做类型转换+错误兜底
onMounted(() => {
  // 把接收的参数转成数字，彻底解决类型不匹配问题！！
  const targetId = Number(props.productId || route.params.productId);
  // 根据ID查找商品
  const targetProduct = allProducts.value.find(item => item.id === targetId);
  
  if (targetProduct) {
    // 找到商品，赋值渲染
    productData.value = targetProduct;
  } else {
    // 没找到商品，兜底提示+跳回列表页
    productData.value.name = '商品不存在';
    productData.value.description = '您访问的商品已下架或不存在';
    alert('该商品不存在！');
    setTimeout(() => {
      router.push('/product-list');
    }, 1500);
  }
});

// 购买数量
const quantity = ref(1);

// 计算总价
const totalPrice = computed(() => {
  return (productData.value.price * quantity.value).toFixed(2);
});

// 数量增减
const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};
const increaseQuantity = () => {
  if (quantity.value < productData.value.stock) {
    quantity.value++;
  }
};

// 操作按钮
const addToCart = () => {
  alert(`已将 ${productData.value.name} ×${quantity.value} 加入购物车`);
};
const buyNow = () => {
  router.push('/checkout'); // 跳转到结算页
};
const goHome = () => {
  router.push('/home');
};

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