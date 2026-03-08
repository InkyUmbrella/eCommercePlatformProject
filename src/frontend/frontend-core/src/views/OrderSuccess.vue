<template>
  <div class="success-container">
    <div class="success-icon">✅</div>
    <h1 class="success-title">订单提交成功！</h1>
    <div class="order-info">
      <p>订单号：{{ route.query.orderId }}</p>
      <p>实付金额：¥{{ route.query.totalAmount }}</p>
      <p>下单时间：{{ new Date().toLocaleString() }}</p>
    </div>
    <div class="btn-group">
      <button class="btn" @click="goToOrderList">查看我的订单</button>
      <button class="btn primary" @click="goToHome">返回首页</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// 查看订单列表
const goToOrderList = () => {
  router.push('/order-list');
};

// 返回首页
const goToHome = () => {
  router.push('/home');
};
</script>

<style scoped>
.success-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.success-icon {
  font-size: 80px;
  color: #4caf50;
  margin-bottom: 20px;
}
.success-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
}
.order-info {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
  margin-bottom: 30px;
  text-align: center;
}
.order-info p {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}
.btn-group {
  display: flex;
  gap: 20px;
}
.btn {
  padding: 10px 25px;
  border: 1px solid #ffc0cb;
  border-radius: 8px;
  background-color: #fff;
  color: #ff69b4;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}
.btn.primary {
  background-color: #ff69b4;
  color: #fff;
  border: none;
}
.btn:hover {
  opacity: 0.9;
}
</style>