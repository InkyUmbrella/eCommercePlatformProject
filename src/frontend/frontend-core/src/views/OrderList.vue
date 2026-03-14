<template>
  <div class="order-container">
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <h1 class="page-title">我的订单</h1>
        <p class="tip-text">查看您的美妆订单，跟踪物流状态</p>
      </div>
       <div class="header-right">
        <button class="nav-btn" @click="goToHome">首页</button>
        <button class="nav-btn" @click="goToCart">购物车</button>
        <button class="nav-btn" @click="goToOrders">订单</button>

        <button class="nav-btn" @click="goToSupport">客服</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
       </div>
    </header>

    <div class="search-bar">
      <select class="search-select">
        <option>商品名称</option>
        <option>订单号</option>
      </select>
      <input type="text" class="search-input" placeholder="搜索订单" v-model="searchKeyword" />
      <button class="search-btn" @click="handleSearch">搜索</button>
    </div>

    <div class="order-tabs">
      <button
        class="tab-item"
        :class="{ active: activeTab === 'all' }"
        @click="switchTab('all')"
      >
        全部订单
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'pending_payment' }"
        @click="switchTab('pending_payment')"
      >
        待支付
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'pending_shipment' }"
        @click="switchTab('pending_shipment')"
      >
        待发货<span class="badge" v-if="pendingShipCount > 0">{{ pendingShipCount }}</span>
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'pending_receipt' }"
        @click="switchTab('pending_receipt')"
      >
        待收货
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'completed' }"
        @click="switchTab('completed')"
      >
        已完成
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'refund_processing' }"
        @click="switchTab('refund_processing')"
      >
        售后中
      </button>
      <button
        class="tab-item"
        :class="{ active: activeTab === 'cancelled' }"
        @click="switchTab('cancelled')"
      >
        已取消
      </button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="order-list">
      <div class="order-item" v-for="order in orderList" :key="order.id">
        <div class="order-header">
          <span class="order-id">订单号：{{ order.orderNo }}</span>
          <span class="order-time">{{ order.createTime }}</span>
          <span class="order-status" :class="order.status">{{ order.statusText }}</span>
        </div>

        <div class="order-content">
          <img :src="order.image" :alt="order.name" class="product-img" />
          <div class="product-info">
            <h4 class="product-name">{{ order.name }}</h4>
            <p class="product-desc">分类：{{ order.category }} | 数量：{{ order.quantity }} 件</p>
          </div>
          <div class="order-amount">
            <p class="amount-label">实付款</p>
            <p class="amount-price">￥{{ order.price }}</p>
            <p class="payment-method">{{ order.paymentMethod }}</p>
          </div>
        </div>

        <div class="order-address" v-if="order.address.name || order.address.detail">
          <span class="address-icon">地址</span>
          <span class="address-text">{{ order.address.name }} {{ order.address.phone }}</span>
          <span class="address-detail">{{ order.address.region }} {{ order.address.detail }}</span>
        </div>

        <div class="order-actions">
          <button
            class="action-btn logistics"
            v-if="['pending_shipment', 'pending_receipt'].includes(order.status)"
            @click="viewLogistics(order.id)"
          >
            查看物流
          </button>

          <button
            class="action-btn cancel"
            v-if="order.status === 'pending_payment'"
            @click="cancelOrder(order.id)"
          >
            取消订单
          </button>

          <button
            class="action-btn refund"
            v-if="!['pending_payment', 'cancelled'].includes(order.status) && !order.aftersaleUsed"
            @click="applyRefund(order.id)"
          >
            申请退款
          </button>

          <button
            class="action-btn confirm"
            v-if="order.status === 'pending_receipt'"
            @click="confirmReceive(order.id)"
          >
            确认收货
          </button>

          <button
            class="action-btn buy-again"
            v-if="['completed', 'cancelled'].includes(order.status)"
            @click="buyAgain(order.productId)"
          >
            再次购买
          </button>
        </div>
      </div>

      <div class="pagination" v-if="pagination.total > pagination.pageSize">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="pagination.total"
          :page-size="pagination.pageSize"
          :current-page="pagination.page"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <div class="logistics-dialog-mask" v-if="showLogisticsDialog" @click="closeLogisticsDialog"></div>
    <div class="logistics-dialog" v-if="showLogisticsDialog">
      <div class="dialog-header">
        <h3>物流信息</h3>
        <button class="close-btn" @click="closeLogisticsDialog">×</button>
      </div>
      <div class="dialog-content">
        <div class="logistics-info">
          <p class="logistics-company">快递公司：{{ logisticsCompany }}</p>
          <p class="logistics-no">运单号码：{{ logisticsNo }}</p>
        </div>
        <div class="logistics-timeline">
          <div class="timeline-item" v-for="item in logisticsList" :key="item.id">
            <div class="timeline-dot" :class="{ active: item.status === 'current' }"></div>
            <div class="timeline-content">
              <p class="timeline-text">{{ item.text }}</p>
              <p class="timeline-time">{{ item.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as orderApi from '@/api/order';

const router = useRouter();
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const orderList = ref([]);
const loading = ref(false);
const error = ref('');
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0,
});
const activeTab = ref('all');
const searchKeyword = ref('');
const showLogisticsDialog = ref(false);
const logisticsList = ref([]);
const logisticsCompany = ref('待更新');
const logisticsNo = ref('待更新');

let searchTimer = null;

const normalizeImage = (path) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  return `${baseURL}${path}`;
};

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

const normalizeAddress = (address) => {
  if (!address) {
    return { name: '', phone: '', region: '', detail: '' };
  }
  if (typeof address === 'string') {
    return { name: '', phone: '', region: '', detail: address };
  }
  return {
    name: address.name || '',
    phone: address.phone || address.phone_number || '',
    region: address.region || '',
    detail: address.detail || address.address || '',
  };
};

const normalizeLogistics = (payload) => {
  if (Array.isArray(payload?.traces)) {
    return payload.traces.map((item, index) => ({
      id: index + 1,
      text: item.text || item.status || item.content || '物流状态更新',
      time: item.time || item.timestamp || '',
      status: index === 0 ? 'current' : '',
    }));
  }

  if (payload?.express_company || payload?.express_no) {
    return [
      {
        id: 1,
        text: `已发货，承运方：${payload.express_company || '待补充'}，单号：${payload.express_no || '待补充'}`,
        time: payload.shipped_at || payload.updated_at || '',
        status: payload.status === 'pending_receipt' ? 'current' : '',
      },
    ];
  }

  return [
    {
      id: 1,
      text: '订单暂未发货',
      time: '',
      status: 'current',
    },
  ];
};

const fetchOrders = async () => {
  loading.value = true;
  error.value = '';
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
      search: searchKeyword.value.trim() || undefined,
    };

    if (activeTab.value !== 'all') {
      params.status = activeTab.value;
    }

    const res = await orderApi.getOrders(params);
    orderList.value = res.results.map((item) => {
      const firstItem = item.items?.[0] || {};
      return {
        id: item.id,
        orderNo: item.order_no || item.id,
        createTime: item.created_at || '',
        status: item.status,
        aftersaleUsed: Boolean(item.aftersale_used),
        statusText: getStatusText(item.status),
        name: firstItem.product_name || firstItem.title || '商品',
        category: firstItem.category_name || '',
        quantity: item.items?.reduce((sum, current) => sum + (current.quantity || 0), 0) || 0,
        price: item.pay_amount,
        paymentMethod: item.payment_method || '在线支付',
        image: normalizeImage(firstItem.image || firstItem.cover_image),
        productId: firstItem.product_id,
        address: normalizeAddress(item.address),
      };
    });
    pagination.value.total = res.count || 0;
  } catch (err) {
    error.value = err?.message || '加载订单失败';
    ElMessage.error(error.value);
  } finally {
    loading.value = false;
  }
};

const pendingShipCount = computed(() =>
  orderList.value.filter((item) => item.status === 'pending_shipment').length,
);

const switchTab = (tab) => {
  activeTab.value = tab;
  pagination.value.page = 1;
  fetchOrders();
};

const handleSearch = () => {
  if (searchTimer) {
    clearTimeout(searchTimer);
  }
  searchTimer = window.setTimeout(() => {
    pagination.value.page = 1;
    fetchOrders();
  }, 400);
};

const handlePageChange = (page) => {
  pagination.value.page = page;
  fetchOrders();
};

const viewLogistics = async (orderId) => {
  try {
    const res = await orderApi.getLogistics(orderId);
    logisticsCompany.value = res?.express_company || '待更新';
    logisticsNo.value = res?.express_no || '待更新';
    logisticsList.value = normalizeLogistics(res);
    showLogisticsDialog.value = true;
  } catch (err) {
    ElMessage.error(err?.message || '获取物流信息失败');
  }
};

const closeLogisticsDialog = () => {
  showLogisticsDialog.value = false;
  logisticsList.value = [];
  logisticsCompany.value = '待更新';
  logisticsNo.value = '待更新';
};

const applyRefund = (orderId) => {
  ElMessageBox.confirm('确定要申请退款吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      await orderApi.refundOrder(orderId);
      ElMessage.success('退款申请已提交');
      fetchOrders();
    })
    .catch(() => {});
};

const confirmReceive = (orderId) => {
  ElMessageBox.confirm('确认已经收到商品吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info',
  })
    .then(async () => {
      await orderApi.receiveOrder(orderId);
      ElMessage.success('确认收货成功');
      fetchOrders();
    })
    .catch(() => {});
};

const cancelOrder = (orderId) => {
  ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      await orderApi.cancelOrder(orderId);
      ElMessage.success('订单已取消');
      fetchOrders();
    })
    .catch(() => {});
};

const buyAgain = (productId) => {
  if (!productId) {
    ElMessage.warning('该订单商品信息缺失');
    return;
  }
  router.push({ name: 'ProductDetail', params: { productId } });
};

const goToHome = () => router.push('/home');
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');
const goToSupport = () => router.push({ name: 'Support' });

onMounted(() => {
  fetchOrders();
});

watch(searchKeyword, handleSearch);
</script>

<style scoped>
/* 全局容器 */
.order-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航栏：和其他页面保持一致 */
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

/* 搜索栏 */
.search-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 10px 30px;
  gap: 0;
}
.search-select {
  padding: 8px 12px;
  border: 1px solid #ffc0cb;
  border-radius: 6px 0 0 6px;
  font-size: 12px;
  color: #666;
}
.search-input {
  padding: 8px 12px;
  border: 1px solid #ffc0cb;
  border-left: none;
  border-radius: 0;
  font-size: 12px;
  width: 200px;
}
.search-btn {
  background-color: #ff69b4;
  border: none;
  border-radius: 0 6px 6px 0;
  color: #fff;
  padding: 8px 12px;
  cursor: pointer;
}

/* 订单状态筛选标签 */
.order-tabs {
  display: flex;
  align-items: center;
  background-color: #fff;
  border-radius: 12px;
  margin: 10px 30px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}
.tab-item {
  flex: 1;
  padding: 12px 0;
  background: none;
  border: none;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s;
}
.tab-item.active {
  background-color: #ff69b4;
  color: #fff;
  font-weight: 600;
}
.badge {
  background-color: #ff4081;
  color: #fff;
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 50%;
  margin-left: 2px;
}

/* 订单列表 */
.order-list {
  padding: 0 30px;
}
.order-item {
  background-color: #fff;
  border-radius: 12px;
  margin-bottom: 15px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}
/* 订单头部 */
.order-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #fff9f7;
  font-size: 12px;
  color: #666;
}
.order-id {
  font-weight: 600;
}
.order-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}
.order-status.pending_receive {
  background-color: #e3f2fd;
  color: #1976d2;
}
.order-status.pending_ship {
  background-color: #fff3e0;
  color: #f57c00;
}
.order-status.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}
/* 订单内容 */
.order-content {
  display: flex;
  align-items: center;
  padding: 15px;
  gap: 15px;
}
.product-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}
.product-info {
  flex: 1;
}
.product-name {
  font-size: 14px;
  color: #333;
  margin: 0 0 5px 0;
}
.product-desc {
  font-size: 12px;
  color: #999;
  margin: 0;
}
.order-amount {
  text-align: right;
}
.amount-label {
  font-size: 11px;
  color: #999;
  margin: 0;
}
.amount-price {
  font-size: 16px;
  color: #ff69b4;
  font-weight: 600;
  margin: 2px 0;
}
.payment-method {
  font-size: 11px;
  color: #999;
  margin: 0;
}
/* 收货地址 */
.order-address {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background-color: #fff9f7;
  font-size: 12px;
  color: #666;
  gap: 5px;
}
.address-icon {
  color: #ff69b4;
}
.address-text {
  flex: 1;
}
.address-detail {
  flex: 2;
}
/* 订单操作栏 */
.order-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 10px 15px;
  gap: 10px;
  border-top: 1px solid #ffe6ef;
}
.action-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}
.action-btn.logistics {
  background-color: #e3f2fd;
  border: 1px solid #bbdefb;
  color: #1976d2;
}
.action-btn.refund {
  background-color: #fff3e0;
  border: 1px solid #ffcc80;
  color: #f57c00;
}
.action-btn.confirm {
  background-color: #ff69b4;
  border: none;
  color: #fff;
}
.action-btn.buy-again {
  background-color: #fff0f5;
  border: 1px solid #ffc0cb;
  color: #ff69b4;
}
.action-btn:hover {
  opacity: 0.9;
}

/* 物流弹窗 */
.logistics-dialog-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}
.logistics-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(255, 105, 180, 0.3);
  z-index: 1001;
  padding: 15px;
}
.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #ffe6ef;
  margin-bottom: 15px;
}
.dialog-header h3 {
  font-size: 18px;
  color: #333;
  margin: 0;
}
.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
}
.logistics-info {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ffe6ef;
}
.logistics-company, .logistics-no {
  font-size: 14px;
  color: #333;
  margin: 5px 0;
}
/* 物流时间线 */
.logistics-timeline {
  position: relative;
  padding-left: 20px;
}
.logistics-timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #ffc0cb;
}
.timeline-item {
  position: relative;
  margin-bottom: 15px;
}
.timeline-dot {
  position: absolute;
  left: -16px;
  top: 5px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ffc0cb;
}
.timeline-dot.active {
  background-color: #ff69b4;
  transform: scale(1.2);
}
.timeline-content {
  margin-left: 10px;
}
.timeline-text {
  font-size: 13px;
  color: #333;
  margin: 0 0 3px 0;
}
.timeline-time {
  font-size: 11px;
  color: #999;
  margin: 0;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-center {
    display: none;
  }
  .order-tabs {
    margin: 10px 15px;
  }
  .tab-item {
    font-size: 12px;
    padding: 10px 0;
  }
  .order-list {
    padding: 0 15px;
  }
  .order-content {
    padding: 10px;
  }
  .product-img {
    width: 50px;
    height: 50px;
  }
  .order-address {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }
  .order-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>
