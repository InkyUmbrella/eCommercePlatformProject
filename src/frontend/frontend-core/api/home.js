// src/api/home.js
import request from './request';

// 获取轮播图
export const getBanners = () => request.get('/home/banners/');

// 获取新品商品（假设有专门的新品接口）
export const getNewProducts = () => request.get('/products/new/');

// 如果新品就是通用商品列表加参数，可以这样：
// export const getNewProducts = () => request.get('/products/', { params: { is_new: true, limit: 5 } });