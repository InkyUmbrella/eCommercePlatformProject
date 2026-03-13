// src/api/cart.js
import request from './request';

// 获取购物车
export const getCart = () => request.get('/cart/');

// 加入购物车
export const addCartItem = (data) => request.post('/cart/items/', data);

// 更新购物车项（数量/勾选）
export const updateCartItem = (itemId, data) => request.patch(`/cart/items/${itemId}/`, data);

// 删除购物车项
export const deleteCartItem = (itemId) => request.delete(`/cart/items/${itemId}/`);

// 全选/全不选
export const selectAll = (selected) => request.patch('/cart/select-all/', { selected });