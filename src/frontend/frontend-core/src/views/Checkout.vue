<template>
  <div class="checkout-container">
    <h2>确认订单</h2>

    <div v-if="loading">加载中...</div>
    <div v-else>
      <section class="card">
        <h3>收货地址</h3>
        <div v-if="!orderConfirmData.addresses?.length">暂无地址，请先新增地址</div>
        <label v-for="addr in orderConfirmData.addresses" :key="addr.id" class="address-item">
          <input type="radio" :value="addr.id" v-model="selectedAddressId" />
          <span>{{ addr.name }} {{ addr.phone_number }} {{ addr.address }}</span>
        </label>
      </section>

      <section class="card">
        <h3>商品清单</h3>
        <div v-for="item in orderConfirmData.items" :key="item.cart_item_id" class="item-row">
          <span>{{ item.title }}</span>
          <span>x{{ item.quantity }}</span>
          <span>￥{{ item.subtotal }}</span>
        </div>
      </section>

      <section class="card">
        <div>商品金额：￥{{ orderConfirmData.items_amount }}</div>
        <div>运费：￥{{ orderConfirmData.shipping_fee }}</div>
        <strong>实付：￥{{ orderConfirmData.pay_amount }}</strong>
      </section>

      <div class="actions">
        <button @click="goBack">返回购物车</button>
        <button :disabled="submitting" @click="submitOrder">{{ submitting ? '提交中...' : '提交并支付' }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useCartStore } from '@/store/cartStore';
import * as orderApi from '@/api/order';

const router = useRouter();
const cartStore = useCartStore();

const loading = ref(false);
const submitting = ref(false);
const orderConfirmData = ref({
  addresses: [],
  items: [],
  items_amount: '0.00',
  shipping_fee: '0.00',
  pay_amount: '0.00',
});
const selectedAddressId = ref(null);

const fetchConfirm = async () => {
  loading.value = true;
  try {
    const data = await orderApi.confirmOrder();
    orderConfirmData.value = data;
    selectedAddressId.value = data.default_address?.id || data.addresses?.[0]?.id || null;
  } catch (err) {
    ElMessage.error(`获取确认信息失败: ${err.message}`);
    router.push('/cart');
  } finally {
    loading.value = false;
  }
};

const submitOrder = async () => {
  if (!selectedAddressId.value) {
    ElMessage.warning('请选择收货地址');
    return;
  }
  submitting.value = true;
  try {
    const order = await orderApi.createOrder(selectedAddressId.value);
    await orderApi.payOrder(order.order_id);
    await cartStore.fetchCart();
    ElMessage.success('下单并支付成功');
    router.push({
      name: 'OrderSuccess',
      query: {
        orderId: order.order_id,
        orderNo: order.order_no,
        totalAmount: order.pay_amount,
      },
    });
  } catch (err) {
    ElMessage.error(`提交订单失败: ${err.message}`);
  } finally {
    submitting.value = false;
  }
};

const goBack = () => router.push('/cart');

onMounted(fetchConfirm);
</script>

<style scoped>
.checkout-container { padding: 16px; max-width: 860px; margin: 0 auto; }
.card { border: 1px solid #eee; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
.address-item { display: block; margin: 8px 0; }
.item-row { display: grid; grid-template-columns: 1fr auto auto; gap: 12px; margin: 8px 0; }
.actions { display: flex; justify-content: flex-end; gap: 8px; }
</style>
