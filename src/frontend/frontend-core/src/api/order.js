import request from './request';

// 获取订单列表（兼容后端返回数组与分页结构）
export const getOrders = async (params) => {
  const data = await request.get('/orders/', { params });
  if (Array.isArray(data)) {
    return { count: data.length, results: data };
  }
  if (data && Array.isArray(data.results)) {
    return data;
  }
  return { count: 0, results: [] };
};

// 获取订单详情
export const getOrderDetail = (orderId) => request.get(`/orders/${orderId}/`);

// 订单确认页
export const confirmOrder = () => request.post('/orders/confirm/', {});

// 创建订单
export const createOrder = (addressId) =>
  request.post('/orders/', { address_id: addressId });

// 支付订单
export const payOrder = (orderId) => request.post(`/orders/${orderId}/pay/`);

// 取消订单
export const cancelOrder = (orderId) => request.post(`/orders/${orderId}/cancel/`);

// 确认收货
export const receiveOrder = (orderId) =>
  request.post(`/orders/${orderId}/confirm-receive/`);

// 发起售后
export const refundOrder = (orderId) => request.post(`/orders/${orderId}/refund/`);

// 售后完成
export const completeRefund = (orderId) =>
  request.post(`/orders/${orderId}/refund-complete/`);

// 查看物流（如后端实现）
export const getLogistics = (orderId) => request.get(`/orders/${orderId}/logistics/`);
