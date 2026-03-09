import { defineStore } from 'pinia'

// 定义购物车 store
export const useCartStore = defineStore('cart', {
  // 全局状态（购物车商品列表）
  state: () => ({
    cartItems: [] // 结构：[{ id, name, price, quantity, checked, image }]
  }),
  
  // 计算属性（和组件的 computed 类似）
  getters: {
    // 计算已选商品数量
    checkedCount: (state) => {
      return state.cartItems.filter(item => item.checked).length
    },
    // 计算已选商品总金额
    totalAmount: (state) => {
      return state.cartItems
        .filter(item => item.checked)
        .reduce((sum, item) => sum + item.price * item.quantity, 0)
        .toFixed(2)
    },
    // 计算购物车商品总数
    cartTotalCount: (state) => {
      return state.cartItems.reduce((sum, item) => sum + item.quantity, 0)
    }
  },
  
  // 方法（修改状态的逻辑）
  actions: {
   
    // 加入购物车（核心方法）
    addToCart(product) {
      // 1. 检查商品是否已在购物车中
      const existingItem = this.cartItems.find(item => item.id === product.id)
      
      if (existingItem) {
        // 2. 已存在：数量累加
        existingItem.quantity += product.quantity
      } else {
        // 3. 不存在：新增商品（默认未勾选）
        this.cartItems.push({
          ...product,
          checked: false // 默认不勾选
        })
      }
    },
    
    // 增减商品数量
    updateQuantity(id, type) {
      const item = this.cartItems.find(item => item.id === id)
      if (item) {
        if (type === 'increase') {
          item.quantity++
        } else if (type === 'decrease' && item.quantity > 1) {
          item.quantity--
        }
      }
    },
    
    // 删除单个商品
    removeItem(id) {
      this.cartItems = this.cartItems.filter(item => item.id !== id)
    },
    
    // 清空购物车
    clearCart() {
      this.cartItems = []
    },
    
    // 切换商品勾选状态
    toggleCheck(id) {
      const item = this.cartItems.find(item => item.id === id)
      if (item) {
        item.checked = !item.checked
      }
    }
    // cartStore.js actions 中添加
    
}
  
})