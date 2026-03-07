import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/views/Register.vue' // 注册页
import Login from '@/views/Login.vue' // 登录页
import Home from '@/views/Home.vue' 
import ProductList from '@/views/ProductList.vue'
import ProductDetail from '@/views/ProductDetail.vue'
import AddressEdit from '@/views/AddressEdit.vue'
import Support from '@/views/Support.vue'
import Cart from '@/views/Cart.vue'
const routes = [
  
  {
    path: '/', // 打开注册页
    name: 'Register',
    component: Register
  },
  {
    path: '/home',          // 首页的路径
    name: 'Home',
    component: Home
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
  },
  {
    path: '/product-detail/:productId', 
    name: 'ProductDetail',
    component: ProductDetail,
    props: true 
  },
  {
    path: '/address-edit',
    name: 'AddressEdit',
    component: AddressEdit
  },
  {
    path: '/support',
    name: 'Support',
    component: Support
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart 
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router