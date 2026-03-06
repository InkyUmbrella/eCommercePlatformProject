import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/views/Register.vue' // 注册页
import Login from '@/views/Login.vue' // 登录页
import Home from '@/views/Home.vue' 
import ProductList from '../views/ProductList.vue'
const routes = [
  {
    path: '/',          // 首页的路径
    name: 'Home',
    component: Home
  },
  {
    path: '/register', // 打开注册页
    name: 'Register',
    component: Register
  },
  {
    path: '/login', // 登录页路由地址
    name: 'Login',
    component: Login
  },
  
  { 
    path: '/products', 
    name: 'product-list', 
    component: ProductList 
  }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router