<template>
  <div class="checkout-container" v-if="!loading && orderConfirmData">
    <!-- 顶部导航 -->
    <header class="header">
      <button class="back-btn" @click="goBack">返回购物车</button>
      <h1 class="page-title">确认订单</h1>
      <span class="order-id" v-if="createdOrder">订单号：{{ createdOrder.order_no }}</span>
    </header>

    <!-- 收货地址：显示地址列表，允许切换和修改 -->
    <div class="address-card">
      <h3 class="card-title">收货地址</h3>
      <div class="address-list">
        <div
          v-for="addr in orderConfirmData.addresses"
          :key="addr.id"
          class="address-item"
          :class="{ selected: selectedAddressId === addr.id }"
          @click="selectedAddressId = addr.id"
        >
          <div class="address-info">
            <p class="name-phone">{{ addr.name }} {{ addr.phone_number }}</p>
            <p class="address-detail">{{ addr.address }}</p>
            <span v-if="addr.is_default" class="default-tag">默认</span>
          </div>
          <span class="check-icon" v-if="selectedAddressId === addr.id">已选</span>
        </div>
      </div>
      <button class="add-address-btn" @click="goToAddressEdit">+ 新增地址</button>
    </div>

    <!-- 订单商品列表 -->
    <div class="order-items-card">
      <h3 class="card-title">商品清单</h3>
      <div class="item-list">
        <div class="order-item" v-for="item in orderConfirmData.items" :key="item.cart_item_id">
          <img :src="item.image || defaultImage" :alt="item.title" class="item-img" />
          <div class="item-info">
            <p class="item-name">{{ item.title }}</p>
            <p class="item-price">￥{{ item.price }} × {{ item.quantity }}</p>
          </div>
          <p class="item-subtotal">￥{{ item.subtotal }}</p>
        </div>
      </div>
    </div>

    <!-- 支付方式选择 -->
    <div class="payment-card">
      <h3 class="card-title">支付方式</h3>
      <div class="payment-options">
        <label class="payment-option" :class="{ active: paymentMethod === 'wechat' }">
          <input type="radio" v-model="paymentMethod" value="wechat" name="payment" />
          <span class="icon">微信</span>
          <span class="text">微信支付</span>
        </label>
        <label class="payment-option" :class="{ active: paymentMethod === 'alipay' }">
          <input type="radio" v-model="paymentMethod" value="alipay" name="payment" />
          <span class="icon">支付宝</span>
          <span class="text">支付宝支付</span>
        </label>
        <label class="payment-option" :class="{ active: paymentMethod === 'card' }">
          <input type="radio" v-model="paymentMethod" value="card" name="payment" />
          <span class="icon">银行卡</span>
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
          <span class="value">￥{{ orderConfirmData.items_amount }}</span>
        </div>
        <div class="amount-row">
          <span class="label">运费：</span>
          <span class="value">￥{{ orderConfirmData.shipping_fee }}</span>
        </div>
        <div class="amount-row total">
          <span class="label">实付金额：</span>
          <span class="value">￥{{ orderConfirmData.pay_amount }}</span>
        </div>
      </div>
    </div>

    <!-- 底部提交按钮 -->
    <div class="submit-bar">
      <span class="total-amount">实付：￥{{ orderConfirmData.pay_amount }}</span>
      <button class="submit-btn" @click="submitOrder" :disabled="submitting">
        {{ submitting ? '提交中...' : '提交订单' }}
      </button>
    </div>
  </div>
  <div v-else class="loading">加载订单确认信息中...</div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useCartStore } from '@/store/cartStore';
import * as orderApi from '@/api/order';

const router = useRouter();
const route = useRoute();
const cartStore = useCartStore();
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const loading = ref(true);
const submitting = ref(false);
const orderConfirmData = ref(null);
const selectedAddressId = ref(null);
const paymentMethod = ref('wechat');
const createdOrder = ref(null);
const lastSelectedAddressId = ref(null);
const defaultImage = '';

const getFullImageUrl = (path) => {
  if (!path) return defaultImage;
  if (path.startsWith('http')) return path;
  return `${baseURL}${path}`;
};

const normalizeConfirmData = (data) => ({
  ...data,
  addresses: Array.isArray(data?.addresses) ? data.addresses : [],
  items: Array.isArray(data?.items)
    ? data.items.map((item) => ({
        ...item,
        title: item.title || item.product_name || '商品',
        image: getFullImageUrl(item.image || item.cover_image),
      }))
    : [],
});

const resolveSelectedAddressId = (data) => {
  if (lastSelectedAddressId.value && data.addresses.some((addr) => addr.id === lastSelectedAddressId.value)) {
    return lastSelectedAddressId.value;
  }
  if (data.default_address?.id) {
    return data.default_address.id;
  }
  return data.addresses[0]?.id ?? null;
};

const fetchConfirm = async () => {
  loading.value = true;
  try {
    const data = normalizeConfirmData(await orderApi.confirmOrder());
    orderConfirmData.value = data;
    selectedAddressId.value = resolveSelectedAddressId(data);
    lastSelectedAddressId.value = selectedAddressId.value;
  } catch (err) {
    ElMessage.error(err?.message || '获取订单确认信息失败');
    router.push('/cart');
  } finally {
    loading.value = false;
  }
};

watch(
  () => route.query._t,
  (newVal, oldVal) => {
    if (newVal && newVal !== oldVal) {
      lastSelectedAddressId.value = selectedAddressId.value;
      fetchConfirm();
    }
  },
);

onMounted(() => {
  fetchConfirm();
});

const goBack = () => {
  router.push('/cart');
};

const goToAddressEdit = () => {
  router.push({
    path: '/address-edit',
    query: { redirect: '/checkout' },
  });
};

const submitOrder = async () => {
  if (!selectedAddressId.value) {
    ElMessage.warning('请选择收货地址');
    return;
  }

  submitting.value = true;
  try {
    const order = await orderApi.createOrder(selectedAddressId.value);
    createdOrder.value = order;
    await orderApi.payOrder(order.order_id);
    await cartStore.fetchCart();

    ElMessage.success('订单提交成功');
    router.push({
      name: 'OrderSuccess',
      query: {
        orderId: order.order_id,
        orderNo: order.order_no,
        totalAmount: order.pay_amount,
        paymentMethod: paymentMethod.value,
      },
    });
  } catch (err) {
    ElMessage.error(err?.message || '提交订单失败');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>

.checkout-container {
  min-height: 100vh;
  background-color: #fff9f7;
  padding-bottom: 110px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 24px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(255, 192, 203, 0.18);
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-btn {
  border: 1px solid #ffc0cb;
  background-color: #fff0f5;
  color: #8b5a42;
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 13px;
  cursor: pointer;
}

.page-title {
  margin: 0;
  color: #333;
  font-size: 22px;
  font-weight: 700;
}

.order-id {
  color: #8b5a42;
  font-size: 13px;
  white-space: nowrap;
}

.address-card,
.order-items-card,
.payment-card,
.amount-card {
  width: min(920px, calc(100% - 32px));
  margin: 18px auto 0;
  background-color: #fff;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(255, 192, 203, 0.12);
  box-sizing: border-box;
}

.card-title {
  margin: 0 0 16px;
  color: #333;
  font-size: 18px;
  font-weight: 700;
}

.address-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}
.address-item {
  display: flex;

  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ffe6ef;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
}
.address-item.selected {
  border-color: #ff69b4;
  background-color: #fff0f5;
}

.address-info {
  flex: 1;
}
.name-phone {
  font-size: 14px;
  color: #333;
  margin: 0 0 4px 0;
}
.address-detail {
  font-size: 12px;
  color: #666;
  margin: 0;
}
.default-tag {
  display: inline-block;
  background-color: #ff69b4;
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-top: 4px;
}
.check-icon {
  font-size: 18px;
  color: #ff69b4;
}
.add-address-btn {
  width: 100%;
  padding: 10px;
  background-color: #fff;
  border: 1px dashed #ff69b4;
  border-radius: 8px;
  color: #ff69b4;
  font-size: 14px;
  cursor: pointer;
}

.item-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  border-radius: 14px;
  background-color: #fff9fc;
  border: 1px solid #ffe3ee;
}

.item-img {
  width: 84px;
  height: 84px;
  border-radius: 12px;
  object-fit: cover;
  background-color: #f7f7f7;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  margin: 0 0 8px;
  color: #333;
  font-size: 15px;
  font-weight: 600;
}

.item-price {
  margin: 0;
  color: #666;
  font-size: 13px;
}

.item-subtotal {
  margin: 0;
  color: #ff69b4;
  font-size: 18px;
  font-weight: 700;
  white-space: nowrap;
}

.payment-options {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border: 1px solid #ffd6e6;
  border-radius: 14px;
  background-color: #fff9fc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.payment-option input {
  accent-color: #ff69b4;
}

.payment-option.active {
  border-color: #ff69b4;
  background-color: #fff0f7;
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.14);
}

.icon {
  color: #ff69b4;
  font-size: 15px;
  font-weight: 700;
}

.text {
  color: #333;
  font-size: 14px;
}

.amount-detail {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.amount-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #666;
  font-size: 14px;
}

.amount-row.total {
  margin-top: 8px;
  padding-top: 14px;
  border-top: 1px solid #ffe3ee;
  color: #333;
  font-size: 16px;
  font-weight: 700;
}

.label {
  color: inherit;
}

.value {
  color: #ff69b4;
  font-weight: 700;
}

.submit-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 24px;
  background-color: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(10px);
  box-shadow: 0 -4px 18px rgba(255, 192, 203, 0.18);
}

.total-amount {
  color: #333;
  font-size: 18px;
  font-weight: 700;
}

.submit-btn {
  min-width: 180px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #ff87b8 0%, #ff69b4 100%);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  padding: 14px 28px;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(255, 105, 180, 0.24);
}

.submit-btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
  box-shadow: none;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 16px;
  color: #999;
}

@media (max-width: 768px) {
  .header {
    padding: 14px 16px;
    flex-wrap: wrap;
  }

  .page-title {
    font-size: 18px;
  }

  .order-id {
    width: 100%;
  }

  .address-card,
  .order-items-card,
  .payment-card,
  .amount-card {
    width: calc(100% - 24px);
    padding: 16px;
  }

  .order-item {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .item-subtotal {
    width: 100%;
    text-align: right;
  }

  .payment-options {
    grid-template-columns: 1fr;
  }

  .submit-bar {
    padding: 14px 16px;
    flex-direction: column;
    align-items: stretch;
  }

  .submit-btn {
    width: 100%;
  }
}
</style>
