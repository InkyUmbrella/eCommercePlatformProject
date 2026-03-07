<template>
  <div class="order-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <img src="@/assets/hello-kitty.jpeg" alt="Beauty" class="logo" />
        <span class="logo-text">Beauty</span>
      </div>
      <div class="header-center">
        <h1 class="page-title">我的订单</h1>
        <p class="tip-text">查看您的美妆订单，追踪物流状态</p>
      </div>
       <div class="header-right">
        <button class="nav-btn" @click="goToHome">🏠 首页</button>
        <button class="nav-btn" @click="goToCart">🛒 购物车</button>
        <button class="nav-btn" @click="goToOrders">📋 订单</button>

        <button class="nav-btn" @click="goToProfile">👤 我的</button>
        <img src="@/assets/hello-kitty.jpg" alt="用户头像" class="avatar">
       </div>   
    </header>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <select class="search-select">
        <option>美妆名称</option>
        <option>订单号</option>
      </select>
      <input type="text" class="search-input" placeholder="搜索美妆" v-model="searchKeyword" />
      <button class="search-btn" @click="handleSearch">🔍</button>
    </div>

    <!-- 订单状态筛选 -->
    <div class="order-tabs">
      <button 
        class="tab-item" 
        :class="{ active: activeTab === 'all' }" 
        @click="switchTab('all')"
      >
        📋 全部订单
      </button>
      <button 
        class="tab-item" 
        :class="{ active: activeTab === 'pending_payment' }" 
        @click="switchTab('pending_payment')"
      >
        💰 待付款
      </button>
      <button 
        class="tab-item" 
        :class="{ active: activeTab === 'pending_ship' }" 
        @click="switchTab('pending_ship')"
      >
        📦 待发货 <span class="badge" v-if="pendingShipCount > 0">{{ pendingShipCount }}</span>
      </button>
      <button 
        class="tab-item" 
        :class="{ active: activeTab === 'pending_receive' }" 
        @click="switchTab('pending_receive')"
      >
        🚚 待收货
      </button>
      <button 
        class="tab-item" 
        :class="{ active: activeTab === 'completed' }" 
        @click="switchTab('completed')"
      >
        ✅ 已完成
      </button>
    </div>

    <!-- 订单列表 -->
    <div class="order-list">
      <div class="order-item" v-for="order in filteredOrders" :key="order.id">
        <!-- 订单头部：订单号+时间+状态 -->
        <div class="order-header">
          <span class="order-id">订单号：{{ order.id }}</span>
          <span class="order-time">{{ order.createTime }}</span>
          <span class="order-status" :class="order.status">{{ order.statusText }}</span>
        </div>

        <!-- 订单商品信息 -->
        <div class="order-content">
          <img :src="order.image" :alt="order.name" class="product-img" />
          <div class="product-info">
            <h4 class="product-name">{{ order.name }}</h4>
            <p class="product-desc">分类：{{ order.category }} | 数量：{{ order.quantity }} 件</p>
          </div>
          <div class="order-amount">
            <p class="amount-label">实付款</p>
            <p class="amount-price">¥{{ order.price }}</p>
            <p class="payment-method">{{ order.paymentMethod }}</p>
          </div>
        </div>

        <!-- 收货地址 -->
        <div class="order-address">
          <span class="address-icon">📍</span>
          <span class="address-text">{{ order.address.name }} · {{ order.address.phone }}</span>
          <span class="address-detail">{{ order.address.region }} {{ order.address.detail }}</span>
        </div>

        <!-- 订单操作栏 -->
        <div class="order-actions">
          <!-- 物流查看（待发货/待收货状态显示） -->
          <button 
            class="action-btn logistics" 
            v-if="['pending_ship', 'pending_receive'].includes(order.status)"
            @click="viewLogistics(order.id)"
          >
            查看物流
          </button>
          
          <!-- 申请退款（所有状态都可申请，可根据业务调整） -->
          <button 
            class="action-btn refund"
            @click="applyRefund(order.id)"
          >
            申请退款
          </button>
          
          <!-- 确认收货（仅待收货状态显示） -->
          <button 
            class="action-btn confirm" 
            v-if="order.status === 'pending_receive'"
            @click="confirmReceive(order.id)"
          >
            确认收货
          </button>
          
          <!-- 再次购买（已完成状态显示） -->
          <button 
            class="action-btn buy-again" 
            v-if="order.status === 'completed'"
            @click="buyAgain(order.productId)"
          >
            再次购买
          </button>
        </div>
      </div>
    </div>

    <!-- 物流信息弹窗 -->
    <div class="logistics-dialog-mask" v-if="showLogisticsDialog" @click="closeLogisticsDialog"></div>
    <div class="logistics-dialog" v-if="showLogisticsDialog">
      <div class="dialog-header">
        <h3>物流信息</h3>
        <button class="close-btn" @click="closeLogisticsDialog">×</button>
      </div>
      <div class="dialog-content">
        <div class="logistics-info">
          <p class="logistics-company">快递公司：顺丰速运</p>
          <p class="logistics-no">运单号码：SF1234567890123</p>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 订单状态筛选
const activeTab = ref('all');
const searchKeyword = ref('');

// 模拟订单数据
const orderList = ref([
  {
    id: '25122716274433',
    createTime: '2025-12-27 16:02:28',
    status: 'pending_receive', // all/pending_payment/pending_ship/pending_receive/completed
    statusText: '待收货',
    name: '古驰红礼盒绒雾217唇膏',
    category: '彩妆类',
    quantity: 1,
    price: 202,
    paymentMethod: '支付宝',
    image: new URL('@/assets/product/gucci.png', import.meta.url).href,
    productId: 1,
    address: {
      name: '李西农',
      phone: '13900000000',
      region: '北京市 市辖区 东城区',
      detail: '某小区1号楼2单元301'
    }
  },
  {
    id: '25122612345678',
    createTime: '2025-12-26 12:34:56',
    status: 'pending_ship',
    statusText: '待发货',
    name: 'YSL圣罗兰方管口红',
    category: '彩妆类',
    quantity: 1,
    price: 410,
    paymentMethod: '微信支付',
    image: new URL('@/assets/product/ysl.png', import.meta.url).href,
    productId: 2,
    address: {
      name: '张三',
      phone: '13800138000',
      region: '上海市 黄浦区',
      detail: '某某路123号'
    }
  }
]);

// 模拟物流数据
const logisticsList = ref([
  { id: 1, text: '您的订单已提交，等待商家发货', time: '2025-12-27 16:02:28' },
  { id: 2, text: '商家已发货，正在等待快递员取件', time: '2025-12-27 18:30:00', status: 'current' },
  { id: 3, text: '快递已发出，预计3天内送达', time: '2025-12-27 20:15:00' }
]);

// 计算待发货订单数量（用于角标）
const pendingShipCount = computed(() => {
  return orderList.value.filter(item => item.status === 'pending_ship').length;
});

// 筛选订单（按状态+搜索关键词）
const filteredOrders = computed(() => {
  let filtered = orderList.value;
  
  // 1. 按状态筛选
  if (activeTab.value !== 'all') {
    filtered = filtered.filter(item => item.status === activeTab.value);
  }
  
  // 2. 按搜索关键词筛选
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.trim().toLowerCase();
    filtered = filtered.filter(item => 
      item.name.toLowerCase().includes(keyword) || 
      item.id.includes(keyword)
    );
  }
  
  return filtered;
});

// 切换订单状态标签
const switchTab = (tab) => {
  activeTab.value = tab;
};

// 搜索功能
const handleSearch = () => {
  // 搜索逻辑已在 computed 中自动触发，这里仅做响应式更新
  searchKeyword.value = searchKeyword.value;
};

// 查看物流（弹窗显示）
const showLogisticsDialog = ref(false);
const viewLogistics = (orderId) => {
  console.log("查看物流：", orderId);
  showLogisticsDialog.value = true;
};
const closeLogisticsDialog = () => {
  showLogisticsDialog.value = false;
};

// 申请退款
const applyRefund = (orderId) => {
  alert(`申请退款：订单号 ${orderId}，请填写退款原因并提交！`);
  // 可跳转到退款申请页：router.push({ name: 'RefundApply', query: { orderId } });
};

// 确认收货
const confirmReceive = (orderId) => {
  if (confirm('确认已收到商品吗？')) {
    const order = orderList.value.find(item => item.id === orderId);
    if (order) {
      order.status = 'completed';
      order.statusText = '已完成';
      alert('收货成功，订单已完成！');
    }
  }
};

// 再次购买
const buyAgain = (productId) => {
  router.push({ name: 'ProductDetail', params: { productId } });
};
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

/* 顶部导航栏（和其他页面完全一致） */
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