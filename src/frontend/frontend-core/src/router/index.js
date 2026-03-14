import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/views/Register.vue' // 注册页
import Login from '@/views/Login.vue' // 登录页
import Home from '@/views/Home.vue' 
import ProductList from '@/views/ProductList.vue'
import ProductDetail from '@/views/ProductDetail.vue'
import AddressEdit from '@/views/AddressEdit.vue'
import Support from '@/views/Support.vue'
import Cart from '@/views/Cart.vue'
import Checkout from '@/views/Checkout.vue';
import OrderSuccess from '@/views/OrderSuccess.vue';
import OrderList from '@/views/OrderList.vue'

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
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: Checkout
  },
  {
    path: '/order-success',
    name: 'OrderSuccess',
    component: OrderSuccess
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: OrderList
  }
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

const publicRouteNames = new Set(['Login', 'Register'])

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  const isPublicRoute = publicRouteNames.has(to.name)

  if (!token && !isPublicRoute) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  if (token && isPublicRoute) {
    return { name: 'Home' }
  }

  return true
})

export default router
