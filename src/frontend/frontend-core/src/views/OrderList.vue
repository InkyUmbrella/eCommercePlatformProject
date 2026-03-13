<template>
  <div class="order-container">
    <header class="header">
      <h2>我的订单</h2>
      <div class="header-actions">
        <button @click="goToHome">首页</button>
        <button @click="goToCart">购物车</button>
      </div>
    </header>

    <div class="toolbar">
      <input v-model="searchKeyword" placeholder="搜索商品或订单ID" />
      <button @click="handleSearch">搜索</button>
    </div>

    <div class="tabs">
      <button :class="{ active: activeTab === 'all' }" @click="switchTab('all')">全部</button>
      <button :class="{ active: activeTab === 'pending_payment' }" @click="switchTab('pending_payment')">待支付</button>
      <button :class="{ active: activeTab === 'pending_shipment' }" @click="switchTab('pending_shipment')">待发货</button>
      <button :class="{ active: activeTab === 'pending_receipt' }" @click="switchTab('pending_receipt')">待收货</button>
      <button :class="{ active: activeTab === 'completed' }" @click="switchTab('completed')">已完成</button>
      <button :class="{ active: activeTab === 'refund_processing' }" @click="switchTab('refund_processing')">售后中</button>
      <button :class="{ active: activeTab === 'cancelled' }" @click="switchTab('cancelled')">已取消</button>
    </div>

    <div v-if="loading" class="info">加载中...</div>
    <div v-else-if="error" class="info error">{{ error }}</div>

    <div v-else class="list">
      <div class="card" v-for="order in orderList" :key="order.id">
        <div class="row">
          <strong>订单号：{{ order.orderNo }}</strong>
          <span>{{ order.statusText }}</span>
        </div>
        <div class="row muted">创建时间：{{ order.createTime }}</div>
        <div class="row">
          <span>{{ order.name }}</span>
          <span>x{{ order.quantity }}</span>
          <span>￥{{ order.price }}</span>
        </div>
        <div class="row muted" v-if="order.address.name">
          收货地址：{{ order.address.name }} {{ order.address.phone_number }} {{ order.address.address }}
        </div>
        <div class="actions">
          <button v-if="['pending_payment','pending_shipment','refund_processing'].includes(order.status)" @click="cancelOrder(order.id)">取消订单</button>
          <button v-if="order.status === 'pending_receipt'" @click="confirmReceive(order.id)">确认收货</button>
          <button v-if="['pending_receipt','completed'].includes(order.status)" @click="applyRefund(order.id)">申请售后</button>
          <button v-if="order.status === 'refund_processing'" @click="completeRefund(order.id)">售后完成</button>
          <button v-if="['pending_shipment','pending_receipt'].includes(order.status)" @click="viewLogistics(order.id)">查看物流</button>
        </div>
      </div>

      <div class="pagination" v-if="pagination.total > pagination.pageSize">
        <button :disabled="pagination.page <= 1" @click="handlePageChange(pagination.page - 1)">上一页</button>
        <span>{{ pagination.page }} / {{ totalPages }}</span>
        <button :disabled="pagination.page >= totalPages" @click="handlePageChange(pagination.page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as orderApi from '@/api/order';

const router = useRouter();
const orderList = ref([]);
const loading = ref(false);
const error = ref(null);
const activeTab = ref('all');
const searchKeyword = ref('');
const pagination = ref({ page: 1, pageSize: 10, total: 0 });

const totalPages = computed(() => Math.max(1, Math.ceil(pagination.value.total / pagination.value.pageSize)));

const getStatusText = (status) => {
  const map = {
    pending_payment: '待支付',
    pending_shipment: '待发货',
    pending_receipt: '待收货',
    completed: '已完成',
    cancelled: '已取消',
    refund_processing: '售后中',
  };
  return map[status] || status;
};

const fetchOrders = async () => {
  loading.value = true;
  error.value = null;
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
      search: searchKeyword.value || undefined,
      status: activeTab.value === 'all' ? undefined : activeTab.value,
    };
    const res = await orderApi.getOrders(params);
    orderList.value = (res.results || []).map((item) => ({
      id: item.id,
      orderNo: item.order_no || `ORD${String(item.id).padStart(8, '0')}`,
      createTime: item.created_at,
      status: item.status,
      statusText: getStatusText(item.status),
      name: item.items?.[0]?.title || '商品',
      quantity: (item.items || []).reduce((sum, i) => sum + (i.quantity || 0), 0),
      price: item.pay_amount,
      address: item.address || { name: '', phone_number: '', address: '' },
    }));
    pagination.value.total = res.count || 0;
  } catch (err) {
    error.value = err.message;
    ElMessage.error(`加载订单失败: ${err.message}`);
  } finally {
    loading.value = false;
  }
};

const switchTab = (tab) => {
  activeTab.value = tab;
  pagination.value.page = 1;
  fetchOrders();
};

const handleSearch = () => {
  pagination.value.page = 1;
  fetchOrders();
};

const handlePageChange = (page) => {
  pagination.value.page = page;
  fetchOrders();
};

const cancelOrder = async (orderId) => {
  try {
    await orderApi.cancelOrder(orderId);
    ElMessage.success('订单已取消');
    fetchOrders();
  } catch (err) {
    ElMessage.error(`取消失败: ${err.message}`);
  }
};

const confirmReceive = async (orderId) => {
  try {
    await orderApi.receiveOrder(orderId);
    ElMessage.success('已确认收货');
    fetchOrders();
  } catch (err) {
    ElMessage.error(`确认收货失败: ${err.message}`);
  }
};

const applyRefund = async (orderId) => {
  try {
    await orderApi.refundOrder(orderId);
    ElMessage.success('已进入售后中');
    fetchOrders();
  } catch (err) {
    ElMessage.error(`申请售后失败: ${err.message}`);
  }
};

const completeRefund = async (orderId) => {
  try {
    await orderApi.completeRefund(orderId);
    ElMessage.success('售后已完成');
    fetchOrders();
  } catch (err) {
    ElMessage.error(`售后完成失败: ${err.message}`);
  }
};

const viewLogistics = async (orderId) => {
  try {
    const data = await orderApi.getLogistics(orderId);
    const lines = (data.timeline || []).map((i) => `${i.time} ${i.text}`).join('\n');
    ElMessageBox.alert(`${data.company} ${data.tracking_no}\n\n${lines}`, '物流信息');
  } catch (err) {
    ElMessage.error(`获取物流失败: ${err.message}`);
  }
};

const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');

watch(searchKeyword, () => {
  // keep manual search behavior; no auto-fetch for every key stroke
});

onMounted(fetchOrders);
</script>

<style scoped>
.order-container { padding: 16px; }
.header { display: flex; justify-content: space-between; align-items: center; }
.header-actions button { margin-left: 8px; }
.toolbar { margin: 12px 0; display: flex; gap: 8px; }
.tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }
.tabs button.active { background: #ff69b4; color: #fff; border-color: #ff69b4; }
.card { border: 1px solid #eee; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.row { display: flex; gap: 12px; justify-content: space-between; margin: 6px 0; }
.row.muted { color: #666; font-size: 12px; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.info { padding: 16px; }
.info.error { color: #c00; }
.pagination { display: flex; gap: 12px; justify-content: center; align-items: center; margin-top: 12px; }
</style>
