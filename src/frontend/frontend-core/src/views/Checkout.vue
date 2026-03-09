<template>
  <div class="checkout-container"v-if="orderData.address && orderData.items">
    <!-- 顶部导航 -->
    <header class="header">
      <button class="back-btn" @click="goBack">← 返回购物车</button>
      <h1 class="page-title">确认订单</h1>
      <span class="order-id">订单号：{{ orderData.orderId }}</span>
    </header>

    <!-- 收货地址 -->
    <div class="address-card">
      <h3 class="card-title">收货地址</h3>
      <div class="address-info" @click="goToAddressEdit">
        <p class="name-phone">{{ orderData.address.name }} {{ orderData.address.phone }}</p>
        <p class="address-detail">{{ orderData.address.region }} {{ orderData.address.detail }}</p>
        <span class="edit-icon">✏️</span>
      </div>
    </div>

    <!-- 订单商品列表 -->
    <div class="order-items-card">
      <h3 class="card-title">商品清单</h3>
      <div class="item-list">
        <div class="order-item" v-for="item in orderData.items" :key="item.id">
          <img :src="item.image" :alt="item.name" class="item-img" />
          <div class="item-info">
            <p class="item-name">{{ item.name }}</p>
            <p class="item-price">¥{{ item.price }} × {{ item.quantity }}</p>
          </div>
          <p class="item-subtotal">¥{{ item.subtotal }}</p>
        </div>
      </div>
    </div>

    <!-- 支付方式选择 -->
    <div class="payment-card">
      <h3 class="card-title">支付方式</h3>
      <div class="payment-options">
        <label class="payment-option" :class="{ active: paymentMethod === 'wechat' }">
          <input type="radio" v-model="paymentMethod" value="wechat" name="payment" />
          <span class="icon">💚</span>
          <span class="text">微信支付</span>
        </label>
        <label class="payment-option" :class="{ active: paymentMethod === 'alipay' }">
          <input type="radio" v-model="paymentMethod" value="alipay" name="payment" />
          <span class="icon">💙</span>
          <span class="text">支付宝支付</span>
        </label>
        <label class="payment-option" :class="{ active: paymentMethod === 'card' }">
          <input type="radio" v-model="paymentMethod" value="card" name="payment" />
          <span class="icon">💳</span>
          <span class="text">银行卡支付</span>
        </label>
      </div>
    </div>

    <!-- 订单金额 -->
    <div class="amount-card">
      <h3 class="card-title">订单金额</h3>
      <div class="amount-detail">
        <div class="amount-row">
          <span class="label">商品总价：</span>
          <span class="value">¥{{ orderData.totalAmount }}</span>
        </div>
        <div class="amount-row">
          <span class="label">运费：</span>
          <span class="value">¥0.00（包邮）</span>
        </div>
        <div class="amount-row total">
          <span class="label">实付金额：</span>
          <span class="value">¥{{ orderData.totalAmount }}</span>
        </div>
      </div>
    </div>

    <!-- 底部提交按钮 -->
    <div class="submit-bar">
      <span class="total-amount">实付：¥{{ orderData.totalAmount }}</span>
      <button class="submit-btn" @click="submitOrder">提交订单</button>
    </div>
  </div>
   <div v-else class="loading">加载订单数据中...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCartStore } from '@/store/cartStore';

const router = useRouter();
const route = useRoute();
const cartStore = useCartStore();

// 接收购物车传递的订单数据
const orderData = ref({});
// 支付方式（默认微信）
const paymentMethod = ref('wechat');

// 初始化：解析订单数据
onMounted(() => {
  try {
    // 从 sessionStorage 读取订单数据
    const stored = sessionStorage.getItem('checkoutOrder');
    if (stored) {
      const parsed = JSON.parse(stored);
      // 如果地址缺失，补充默认地址（保险）
      if (!parsed.address) {
        parsed.address = {
          name: '张三',
          phone: '13800138000',
          region: '北京市东城区',
          detail: '某某小区1号楼2单元301'
        };
      }
      orderData.value = parsed;
      // 可选：读取后立即清除，防止刷新页面重复提交（但保留一次即可）
      // sessionStorage.removeItem('checkoutOrder');
    } else {
      alert('订单数据不存在，请重新结算！');
      router.push('/cart');
    }
  } catch (e) {
    console.error('订单数据解析失败', e);
    alert('订单数据解析失败，请重新结算！');
    router.push('/cart');
  }
});

// 返回购物车
const goBack = () => {
  router.push('/cart');
};

// 跳转到地址修改页
const goToAddressEdit = () => {
  router.push({
    path: '/address-edit',
    query: { redirect: '/checkout' }
  });
};

// 提交订单（核心结算功能）
const submitOrder = () => {
  
  const settledIds = orderData.value.items.map(item => item.id);
  
  // 1. 模拟支付验证（实际项目对接支付接口）
  alert(`
    订单提交成功！
    订单号：${orderData.value.orderId}
    支付方式：${
      paymentMethod.value === 'wechat' ? '微信支付' : 
      paymentMethod.value === 'alipay' ? '支付宝支付' : '银行卡支付'
    }
    实付金额：¥${orderData.value.totalAmount}
  `);
  
  // 2. 提交成功后：清空购物车中已结算的商品
  cartStore.removeItems(settledIds);
  cartStore.cartItems = cartStore.cartItems.filter(item => !settledIds.includes(item.id));
  
  // 3. 跳转到订单成功页（可创建OrderSuccess.vue）
  router.push({
    name: 'OrderSuccess',
    query: {
      orderId: orderData.value.orderId,
      totalAmount: orderData.value.totalAmount
    }
  });
};
</script>

<style scoped>
/* 全局容器 */
.checkout-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  padding-bottom: 80px; /* 给底部提交按钮留空间 */
}

/* 顶部导航 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}
.back-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #333;
  cursor: pointer;
}
.page-title {
  font-size: 18px;
  color: #333;
  font-weight: 600;
  margin: 0;
}
.order-id {
  font-size: 12px;
  color: #999;
}

/* 通用卡片样式 */
.address-card, .order-items-card, .payment-card, .amount-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
  margin: 10px 20px;
  padding: 15px;
}
.card-title {
  font-size: 16px;
  color: #333;
  font-weight: 600;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #ffe6ef;
}

/* 收货地址 */
.address-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.name-phone {
  font-size: 14px;
  color: #333;
  margin: 0 0 5px 0;
}
.address-detail {
  font-size: 12px;
  color: #666;
  margin: 0;
}
.edit-icon {
  color: #ff69b4;
  font-size: 16px;
}

/* 商品清单 */
.item-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.order-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 0;
  border-bottom: 1px solid #f5f5f5;
}
.item-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}
.item-info {
  flex: 1;
}
.item-name {
  font-size: 14px;
  color: #333;
  margin: 0 0 5px 0;
  line-height: 1.2;
}
.item-price {
  font-size: 12px;
  color: #999;
  margin: 0;
}
.item-subtotal {
  font-size: 14px;
  color: #ff69b4;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 16px;
  color: #999;
}
/* 支付方式 */
.payment-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.payment-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
}
.payment-option.active {
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
}
.payment-option input {
  width: 16px;
  height: 16px;
  accent-color: #ff69b4;
}
.icon {
  font-size: 20px;
}
.text {
  font-size: 14px;
  color: #333;
}

/* 订单金额 */
.amount-detail {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.amount-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}
.amount-row.total {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ffe6ef;
}
.amount-row.total .label {
  font-weight: 600;
  color: #333;
}
.amount-row.total .value {
  font-weight: 600;
  color: #ff69b4;
  font-size: 16px;
}
.label {
  color: #666;
}
.value {
  color: #333;
}

/* 底部提交栏 */
.submit-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background-color: #fff;
  box-shadow: 0 -2px 8px rgba(255, 192, 203, 0.1);
}
.total-amount {
  font-size: 16px;
  color: #ff69b4;
  font-weight: 600;
}
.submit-btn {
  padding: 10px 30px;
  background-color: #ff69b4;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}
.submit-btn:hover {
  background-color: #ff87b8;
}

/* 响应式适配 */
@media (min-width: 768px) {
  .checkout-container {
    max-width: 600px;
    margin: 0 auto;
  }
}
</style>