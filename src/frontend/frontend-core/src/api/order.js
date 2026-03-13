// src/api/order.js
import request from './request';

// 获取订单列表（支持查询参数：status, page, page_size, search）
export const getOrders = (params) => request.get('/orders/', { params });

// 获取单个订单详情
export const getOrderDetail = (orderId) => request.get(`/orders/${orderId}/`);

// 取消订单
export const cancelOrder = (orderId) => request.post(`/orders/${orderId}/cancel/`);

// 确认收货
export const receiveOrder = (orderId) => request.post(`/orders/${orderId}/receive/`);

// 再次购买（一般是通过商品ID跳转到详情页，不需要后端接口）
// 查看物流（假设后端有接口）
export const getLogistics = (orderId) => request.get(`/orders/${orderId}/logistics/`);

// 申请退款（通常需要单独退款接口，暂未提供，先模拟）