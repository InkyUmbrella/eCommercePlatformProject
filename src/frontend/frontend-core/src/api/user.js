// src/api/user.js
import request from './request'; // 使用之前创建的 request 实例

// 注册
export const register = (data) => {
  return request({
    url: '/users/register/',
    method: 'POST',
    data,
  });
};

// 登录
export const login = (data) => {
  return request({
    url: '/users/login/',
    method: 'POST',
    data,
  });
};

// 刷新 token
export const refreshToken = (refresh) => {
  return request({
    url: '/users/refresh/',
    method: 'POST',
    data: { refresh },
  });
};

// 获取当前用户信息
export const getUserInfo = () => {
  return request({
    url: '/users/me/',
    method: 'GET',
  });
};