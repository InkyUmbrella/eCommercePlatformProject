// src/store/userStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import * as userApi from '@/api/user';
import router from '@/router';

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('access_token') || '');
  const refreshToken = ref(localStorage.getItem('refresh_token') || '');
  const userInfo = ref(null);
  const loading = ref(false);
  const error = ref(null);

  // 登录
  const login = async (username, password) => {
    loading.value = true;
    error.value = null;
    try {
      const res = await userApi.login({ username, password });
      // 根据文档，登录成功返回 data 包含 access 和 refresh
      // 注意：request 拦截器已经提取了 data，所以 res 就是 { access, refresh }
      token.value = res.access;
      refreshToken.value = res.refresh;
      
      // 保存到 localStorage
      localStorage.setItem('access_token', res.access);
      localStorage.setItem('refresh_token', res.refresh);
      
      // 登录成功后获取用户信息
      await fetchUserInfo();
      
      // 跳转到首页或之前页面
      router.push('/home');
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 注册
  const register = async (username, password) => {
    loading.value = true;
    error.value = null;
    try {
      const res = await userApi.register({ username, password });
      // 注册成功后，可以自动登录或跳转到登录页
      // 这里我们跳转到登录页，让用户手动登录
      router.push('/login');
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return;
    try {
      const res = await userApi.getUserInfo();
      userInfo.value = res; // res 应该包含 id, username 等
    } catch (err) {
      console.error('获取用户信息失败', err);
      // 如果 token 失效，清除本地存储并跳转登录
      if (err.message.includes('401') || err.message.includes('未登录')) {
        logout();
      }
    }
  };

  // 退出登录
  const logout = () => {
    token.value = '';
    refreshToken.value = '';
    userInfo.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  };

  // 刷新 token（可选，可以在 axios 拦截器中自动调用）
  const refresh = async () => {
    if (!refreshToken.value) throw new Error('无刷新 token');
    try {
      const res = await userApi.refreshToken(refreshToken.value);
      token.value = res.access;
      localStorage.setItem('access_token', res.access);
      return res.access;
    } catch (err) {
      logout();
      throw err;
    }
  };

  return {
    token,
    refreshToken,
    userInfo,
    loading,
    error,
    login,
    register,
    logout,
    fetchUserInfo,
    refresh,
  };
});