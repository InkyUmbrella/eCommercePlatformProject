<template>
  <div class="checkout-container" v-if="!loading && orderConfirmData">
    <!-- 顶部导航 -->
    <header class="header">
      <button class="back-btn" @click="goBack">← 返回购物车</button>
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
          <span class="check-icon" v-if="selectedAddressId === addr.id">✅</span>
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
            <p class="item-price">¥{{ item.price }} × {{ item.quantity }}</p>
          </div>
          <p class="item-subtotal">¥{{ item.subtotal }}</p>
        </div>
      </div>
    </div>

    <!-- 支付方式选择（保持前端模拟） -->
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
          <span class="value">¥{{ orderConfirmData.items_amount }}</span>
        </div>
        <div class="amount-row">
          <span class="label">运费：</span>
          <span class="value">¥{{ orderConfirmData.shipping_fee }}</span>
        </div>
        <div class="amount-row total">
          <span class="label">实付金额：</span>
          <span class="value">¥{{ orderConfirmData.pay_amount }}</span>
        </div>
      </div>
    </div>

    <!-- 底部提交按钮 -->
    <div class="submit-bar">
      <span class="total-amount">实付：¥{{ orderConfirmData.pay_amount }}</span>
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
import * as cartApi from '@/api/cart';

const router = useRouter();
const route = useRoute();
const cartStore = useCartStore();

const loading = ref(true);
const submitting = ref(false);
const orderConfirmData = ref(null);        // 确认接口返回的数据
const selectedAddressId = ref(null);       // 当前选中的地址ID
const paymentMethod = ref('wechat');        // 支付方式
const createdOrder = ref(null);             // 创建订单后返回的订单信息
const lastSelectedAddressId = ref(null);    // 用于刷新后恢复选中

const defaultImage = '@/assets/default-product.png';

// 获取订单确认信息
const fetchConfirm = async () => {
  loading.value = true;
  try {
    const data = await orderApi.confirmOrder();
    orderConfirmData.value = data;

    // 决定选中的地址：优先使用 lastSelectedAddressId，若不存在或不在列表中，则用默认地址或第一个
    let newSelectedId = null;
    if (lastSelectedAddressId.value) {
      const exists = data.addresses.some(addr => addr.id === lastSelectedAddressId.value);
      if (exists) {
        newSelectedId = lastSelectedAddressId.value;
      }
    }
    if (!newSelectedId) {
      if (data.default_address) {
        newSelectedId = data.default_address.id;
      } else if (data.addresses.length > 0) {
        newSelectedId = data.addresses[0].id;
      }
    }
    selectedAddressId.value = newSelectedId;
    // 更新 lastSelected 为当前选中，供下次刷新使用
    lastSelectedAddressId.value = newSelectedId;
  } catch (err) {
    ElMessage.error('获取订单确认信息失败：' + err.message);
    router.push('/cart');
  } finally {
    loading.value = false;
  }
};

// 监听路由中的 _t 参数，变化时重新获取数据（用于从地址编辑页返回）
watch(() => route.query._t, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) {
    // 保存当前选中，以便恢复
    lastSelectedAddressId.value = selectedAddressId.value;
    fetchConfirm();
  }
});

onMounted(() => {
  fetchConfirm();
});

// 返回购物车
const goBack = () => {
  router.push('/cart');
};

// 跳转到地址编辑页（新增/编辑）
const goToAddressEdit = () => {
  router.push({
    path: '/address-edit',
    query: { redirect: '/checkout' } // 保存后返回本页
  });
};

// 提交订单
const submitOrder = async () => {
  if (!selectedAddressId.value) {
    ElMessage.warning('请选择收货地址');
    return;
  }

  submitting.value = true;
  try {
    // 1. 创建订单
    const order = await orderApi.createOrder(selectedAddressId.value);
    createdOrder.value = order;

    // 2. 支付（模拟）
    await orderApi.payOrder(order.order_id);

    // 3. 支付成功后，从购物车中移除已购商品
    const cartItemIds = orderConfirmData.value.items.map(item => item.cart_item_id);
    for (const id of cartItemIds) {
      await cartApi.deleteCartItem(id);
    }
    // 同时更新本地 store
    cartStore.fetchCart();

    // 4. 跳转到成功页
    ElMessage.success('订单支付成功！');
    router.push({
      name: 'OrderSuccess',
      query: {
        orderId: order.order_id,
        orderNo: order.order_no,
        totalAmount: order.pay_amount
      }
    });
  } catch (err) {
    ElMessage.error('提交订单失败：' + err.message);
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
/* 原有的样式保持不变，只需追加地址列表相关样式 */
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

.loading {
  text-align: center;
  padding: 50px;
  font-size: 16px;
  color: #999;
}
/* 原有其他样式保持不变 */
</style>