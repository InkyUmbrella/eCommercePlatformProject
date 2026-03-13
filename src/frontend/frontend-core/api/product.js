import request from './request';

// 获取商品列表，支持分页和筛选参数
// params: { page, page_size, keyword, category_id, brand, ordering, is_new, is_hot, ... }
export const getProducts = (params) => request.get('/products/', { params });

// 获取商品详情
export const getProductDetail = (id) => request.get(`/products/${id}/`);

// 获取分类列表（如果需要）
export const getCategories = () => request.get('/categories/');