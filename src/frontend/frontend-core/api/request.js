// src/api/request.js
import axios from 'axios';

// 创建 axios 实例，配置基础 URL 和超时时间
const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // 根据你的后端实际地址修改
  timeout: 10000,
});

// 请求拦截器：自动添加 token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：统一处理业务状态码，提取 data
request.interceptors.response.use(
  (response) => {
    // 后端返回格式：{ code: 0, message: '...', data: ... }
    const res = response.data;
    if (res.code === 0) {
      return res.data; // 直接返回 data 部分，方便 store 使用
    } else {
      // 业务失败（code=1），抛出错误信息
      return Promise.reject(new Error(res.message || '请求失败'));
    }
  },
  (error) => {
    // 处理 HTTP 错误状态（401 等）
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        // token 过期或未登录，可以跳转到登录页
        // 注意：这里不要用 router.push，因为 interceptors 里可能无法直接访问 router
        // 建议抛出一个特殊错误，在组件中处理跳转，或者使用事件总线
        return Promise.reject(new Error('未登录或登录已过期'));
      }
      // 其他 HTTP 错误
      return Promise.reject(new Error(error.response.data?.message || '服务器错误'));
    }
    return Promise.reject(error);
  }
);

export default request;