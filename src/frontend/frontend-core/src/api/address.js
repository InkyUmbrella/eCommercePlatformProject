// src/api/address.js
import request from './request';

// 获取地址列表
export const getAddresses = () => request.get('/users/addresses/');

// 获取单个地址详情（后端可能未提供单独详情接口，可以走列表过滤，但建议后端提供）
// 如果后端没有提供 GET /addresses/{id}，可以先从列表中过滤，这里我们模拟一下
export const getAddressDetail = (id) => request.get(`/users/addresses/${id}/`); // 假设后端有

// 新增地址
export const createAddress = (data) => request.post('/users/addresses/', data);

// 更新地址
export const updateAddress = (id, data) => request.patch(`/users/addresses/${id}/`, data);

// 删除地址
export const deleteAddress = (id) => request.delete(`/users/addresses/${id}/`);

// 设为默认地址
export const setDefaultAddress = (id) => request.post(`/users/addresses/${id}/set-default/`);