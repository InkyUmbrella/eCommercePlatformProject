import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/views/Register.vue' // 注册页
import Login from '@/views/Login.vue' // 登录页

const routes = [
  {
    path: '/', // 默认打开注册页
    name: 'Register',
    component: Register
  },
  {
    path: '/login', // 登录页路由地址
    name: 'Login',
    component: Login
  }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router