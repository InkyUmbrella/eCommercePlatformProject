<template>
  <div class="cart-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <h1 class="page-title">我的购物车</h1>
        <p class="tip-text">温馨提示：美妆是否购买成功，以最终下单为准，请尽快结算</p>
      </div>
      <div class="header-right">
        <button class="nav-btn" @click="goToHome">🏠 首页</button>
        <button class="nav-btn" @click="goToCart">🛒 购物车</button>
        <button class="nav-btn" @click="goToOrders">📋 订单</button>

        <button class="nav-btn" @click="goToProfile">👤 我的</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
         
      </div>
    </header>

    <!-- 成功提示条（可选，模拟加入购物车成功） -->
    <div class="success-tip" v-if="showSuccessTip">
      ✅ 成功加入购物车！
    </div>

    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 购物车主体 -->
    <div v-else class="cart-main">
      <!-- 购物车头部操作栏 -->
      <div class="cart-header">
        <div class="cart-title">
          <span class="heart">❤️</span>
          <span>美妆商城</span>
        </div>
        <button class="clear-btn" @click="handleClearCart">清空</button>
      </div>

      <!-- 购物车列表 -->
      <div class="cart-list">
        <!-- 表头（增加全选复选框） -->
        <div class="cart-table-header">
          <span class="col-select">
            <input type="checkbox" :checked="allSelected" @change="toggleAllSelect" />
          </span>
          <span class="col-info">美妆信息</span>
          <span class="col-spec">规格</span>
          <span class="col-price">单价</span>
          <span class="col-quantity">数量</span>
          <span class="col-discount">会员优惠</span>
          <span class="col-subtotal">小计</span>
          <span class="col-action">操作</span>
        </div>

        <div class="cart-item" v-for="item in cartItems" :key="item.id">
          <div class="col-select">
            <input type="checkbox" v-model="item.selected" class="checkbox" @change="handleToggleCheck(item.id)" />
          </div>
          <div class="col-info">
            <img :src="item.image || defaultImage" :alt="item.name" class="product-img" />
            <span class="product-name">{{ item.name }}</span>
          </div>
          <div class="col-spec">-</div>
          <div class="col-price">¥{{ item.price.toFixed(2) }}</div>
          <div class="col-quantity">
            <button class="quantity-btn" @click="handleDecrease(item)" :disabled="item.quantity <= 1">-</button>
            <input type="number" v-model.number="item.quantity" class="quantity-input" readonly />
            <button class="quantity-btn" @click="handleIncrease(item)">+</button>
          </div>
          <div class="col-discount">-</div>
          <div class="col-subtotal">¥{{ (item.price * item.quantity).toFixed(2) }}</div>
          <div class="col-action">
            <button class="delete-btn" @click="handleRemove(item.id)">×</button>
          </div>
        </div>
      </div>

      <!-- 底部操作栏 -->
      <div class="cart-footer">
        <div class="footer-left">
          <button class="continue-shopping" @click="goBack">← 继续选购</button>
          <span class="cart-summary">共 {{ cartItems.length }} 件美妆，已选 {{ checkedCount }} 件</span>
        </div>
        <div class="footer-right">
          <span class="total-label">合计：</span>
          <span class="total-price">¥{{ totalAmount }}</span>
          <button class="checkout-btn" :disabled="Number(totalAmount) <= 0" @click="goToCheckout">去结算 →</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useCartStore } from '@/store/cartStore';
import { ElMessage } from 'element-plus'; // 如果你使用了 Element Plus

const router = useRouter();
const cartStore = useCartStore();
const { cartItems, checkedCount, totalAmount, loading, error } = storeToRefs(cartStore);

// 默认图片（当商品图片缺失时显示）
const defaultImage = '@/assets/default-product.png';

// 全选状态计算属性
const allSelected = computed(() => {
  return cartItems.value.length > 0 && cartItems.value.every(item => item.selected);
});

// 页面加载时获取购物车
onMounted(() => {
  cartStore.fetchCart();
});

// 处理勾选切换
const handleToggleCheck = (id) => {
  cartStore.toggleCheck(id);
};

// 增加数量
const handleIncrease = (item) => {
  cartStore.updateQuantity(item.id, 'increase');
};

// 减少数量
const handleDecrease = (item) => {
  cartStore.updateQuantity(item.id, 'decrease');
};

// 删除商品
const handleRemove = (id) => {
  ElMessage.confirm('确定要删除该商品吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    cartStore.removeItem(id);
  }).catch(() => {});
};

// 清空购物车
const handleClearCart = () => {
  ElMessage.confirm('确定要清空购物车吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    cartStore.clearCart();
  }).catch(() => {});
};

// 全选/全不选
const toggleAllSelect = (e) => {
  cartStore.toggleSelectAll(e.target.checked);
};

// 继续选购
const goBack = () => {
  router.push('/products');
};

// 去结算
const goToCheckout = () => {
  const selectedItems = cartItems.value.filter(item => item.selected);
  if (selectedItems.length === 0) {
    ElMessage.warning('请先选择要结算的商品！');
    return;
  }
  // 组装订单数据，存入 sessionStorage
  const orderData = {
    orderId: Date.now(),
    createTime: new Date().toLocaleString(),
    totalAmount: totalAmount.value,
    items: selectedItems.map(item => ({
      id: item.id,
      name: item.name,
      price: item.price,
      quantity: item.quantity,
      image: item.image,
      subtotal: (item.price * item.quantity).toFixed(2)
    })),
    address: { /* 模拟地址，后续可从地址管理获取 */ }
  };

  sessionStorage.setItem('checkoutOrder', JSON.stringify(orderData));



  router.push({ name: 'Checkout' });


};

// 导航方法
const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToProfile = () => router.push('/profile');
</script>

<style scoped>
/* 全局容器 */
.cart-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7; /* 浅米色背景，和商城一致 */
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航栏 */
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
  flex-direction: column;
  align-items: center;
}
.page-title {
  font-size: 22px;
  color: #333;
  font-weight: 600;
  margin: 0 0 5px 0;
}
.tip-text {
  font-size: 12px;
  color: #999;
  margin: 0;
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
  border-radius: 8px;
  transition: all 0.3s;
}
.nav-btn.active {
  color: #ff69b4;
  background-color: #fff0f5;
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
}

/* 购物车主体 */
.cart-main {
  width: 90%;
  max-width: 800px;
  margin: 20px auto;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.15);
  overflow: hidden;
}

/* 购物车头部 */
.cart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #ffe6ef;
}
.cart-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  color: #ff69b4;
  font-weight: 600;
}
.heart {
  font-size: 20px;
}
.clear-btn {
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
  color: #ff69b4;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}
.clear-btn:hover {
  background-color: #ff69b4;
  color: #fff;
}

/* 购物车列表 */
.cart-list {
  padding: 0 20px;
}
/* 表头 */
.cart-table-header {
  display: grid;
  grid-template-columns: 30px 2fr 1fr 1fr 1fr 1fr 1fr 50px;
  gap: 10px;
  padding: 10px 0;
  font-size: 12px;
  color: #999;
  border-bottom: 1px solid #ffe6ef;
}
/* 商品项 */
.cart-item {
  display: grid;
  grid-template-columns: 30px 2fr 1fr 1fr 1fr 1fr 1fr 50px;
  gap: 10px;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #ffe6ef;
}
.col-select {
  display: flex;
  align-items: center;
  justify-content: center;
}
.checkbox {
  width: 16px;
  height: 16px;
  accent-color: #ff69b4;
}
.col-info {
  display: flex;
  align-items: center;
  gap: 10px;
}
.product-img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 8px;
}
.product-name {
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}
.col-spec, .col-discount {
  font-size: 12px;
  color: #999;
}
.col-price {
  font-size: 14px;
  color: #333;
}
.col-quantity {
  display: flex;
  align-items: center;
  gap: 5px;
}
.quantity-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
  color: #ff69b4;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.quantity-input {
  width: 30px;
  text-align: center;
  border: 1px solid #ffc0cb;
  border-radius: 4px;
  padding: 2px;
  font-size: 12px;
}
.col-subtotal {
  font-size: 14px;
  color: #ff69b4;
  font-weight: 600;
}
.col-action {
  display: flex;
  align-items: center;
  justify-content: center;
}
.delete-btn {
  background: none;
  border: none;
  color: #ff69b4;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
}

/* 底部操作栏 */
.cart-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-top: 1px solid #ffe6ef;
}
.footer-left {
  display: flex;
  align-items: center;
  gap: 20px;
}
.continue-shopping {
  background: none;
  border: none;
  color: #ff69b4;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}
.cart-summary {
  font-size: 12px;
  color: #999;
}
.footer-right {
  display: flex;
  align-items: center;
  gap: 15px;
}
.total-label {
  font-size: 14px;
  color: #666;
}
.total-price {
  font-size: 20px;
  color: #ff69b4;
  font-weight: bold;
}
.checkout-btn {
  padding: 10px 25px;
  background-color: #ff69b4;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}
.checkout-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.checkout-btn:hover:not(:disabled) {
  background-color: #ff87b8;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-center {
    display: none;
  }
  .cart-main {
    width: 95%;
  }
  .cart-table-header, .cart-item {
    grid-template-columns: 25px 2fr 0.5fr 0.5fr 0.8fr 0.5fr 0.8fr 30px;
    gap: 5px;
  }
  .col-spec, .col-discount {
    display: none; /* 移动端隐藏次要列 */
  }
  .product-name {
    font-size: 12px;
  }
  .quantity-input {
    width: 25px;
  }
  .cart-footer {
    flex-direction: column;
    gap: 10px;
    align-items: flex-end;
  }
}
</style>