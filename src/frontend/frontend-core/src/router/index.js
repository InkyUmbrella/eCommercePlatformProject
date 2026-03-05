import { createRouter, createWebHistory } from 'vue-router'
// import Home from '../views/Home.vue'      
import Login from '../views/Login.vue'
import Support from '../views/Support.vue'

const routes = [
  // { path: '/', name: 'home', component: Home },
  { path: '/', redirect: '/support' },
  { path: '/login', name: 'login', component: Login },
  { path: '/support', name: 'support', component: Support }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router