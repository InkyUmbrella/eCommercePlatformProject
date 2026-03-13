// src/store/cartStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import * as cartApi from '@/api/cart';

export const useCartStore = defineStore('cart', () => {
  // 状态
  const cartItems = ref([]);      // 购物车商品列表
  const loading = ref(false);     // 是否正在加载
  const error = ref(null);        // 错误信息

  // 计算属性：已选商品数量
  const checkedCount = computed(() => {
    return cartItems.value.filter(item => item.selected).length;
  });

  // 计算属性：已选商品总金额（注意 price 是字符串，需要转成数字）
  const totalAmount = computed(() => {
    return cartItems.value
      .filter(item => item.selected)
      .reduce((sum, item) => sum + parseFloat(item.price) * item.quantity, 0)
      .toFixed(2);
  });

  // 计算属性：购物车商品总件数
  const cartTotalCount = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.quantity, 0);
  });

  // 获取购物车（初始化/刷新）
  const fetchCart = async () => {
    loading.value = true;
    error.value = null;
    try {
      const data = await cartApi.getCart();
      // 后端返回的 data 结构：{ items: [...], total_amount, selected_count, item_count }
      // 我们需要将 items 映射成前端需要的格式，并确保字段名一致
      cartItems.value = data.items.map(item => ({
        id: item.id,
        product_id: item.product_id,
        name: item.title,                 // 后端字段 title 对应前端的 name
        price: parseFloat(item.price),     // 转成数字方便计算
        quantity: item.quantity,
        selected: item.selected,
        image: item.image || '@/assets/default-product.png', // 可能需要处理图片 URL
        stock: item.stock,
        is_active: item.is_active,
        subtotal: parseFloat(item.subtotal) // 如果有需要
      }));
    } catch (err) {
      error.value = err.message;
      console.error('获取购物车失败', err);
    } finally {
      loading.value = false;
    }
  };
  const addToCart = async (product, quantity = 1) => {
    try {
      await cartApi.addCartItem({ product_id: product.id, quantity });
      await fetchCart(); // 重新拉取购物车
      return true;
    } catch (err) {
      throw err;
    }
  };
  

  // 更新数量（增加/减少）或直接设置数量
  const updateQuantity = async (itemId, type) => {
    const item = cartItems.value.find(i => i.id === itemId);
    if (!item) return;

    let newQuantity = item.quantity;
    if (type === 'increase') {
      newQuantity += 1;
    } else if (type === 'decrease') {
      newQuantity -= 1;
    } else {
      return;
    }

    if (newQuantity < 1) return;

    // 乐观更新：先改本地，请求失败再回滚
    const oldQuantity = item.quantity;
    item.quantity = newQuantity;

    try {
      await cartApi.updateCartItem(itemId, { quantity: newQuantity });
      // 成功后最好重新拉取，确保库存等数据一致
      await fetchCart();
    } catch (err) {
      // 回滚
      item.quantity = oldQuantity;
      error.value = err.message;
      alert('更新数量失败：' + err.message);
    }
  };

  // 切换勾选状态
  const toggleCheck = async (itemId) => {
    const item = cartItems.value.find(i => i.id === itemId);
    if (!item) return;

    const newSelected = !item.selected;
    const oldSelected = item.selected;
    item.selected = newSelected;

    try {
      await cartApi.updateCartItem(itemId, { selected: newSelected });
      await fetchCart(); // 重新拉取确保全选/全不选汇总准确
    } catch (err) {
      item.selected = oldSelected;
      error.value = err.message;
      alert('更新勾选状态失败：' + err.message);
    }
  };

  // 删除商品
  const removeItem = async (itemId) => {
    const index = cartItems.value.findIndex(i => i.id === itemId);
    if (index === -1) return;

    const oldItem = cartItems.value[index];
    cartItems.value.splice(index, 1);

    try {
      await cartApi.deleteCartItem(itemId);
      // 删除成功，可选重新拉取
    } catch (err) {
      // 恢复
      cartItems.value.splice(index, 0, oldItem);
      error.value = err.message;
      alert('删除失败：' + err.message);
    }
  };

  // 清空购物车
  const clearCart = async () => {
    // 获取所有商品ID
    const ids = cartItems.value.map(item => item.id);
    // 逐个删除（后端无批量删除接口）
    for (const id of ids) {
      await removeItem(id);
    }
    // 最后重新获取（确保完全清除）
    await fetchCart();
  };

  // 全选/全不选
  const toggleSelectAll = async (selected) => {
    // 乐观更新所有项的选中状态
    const oldSelectedMap = {};
    cartItems.value.forEach(item => {
      oldSelectedMap[item.id] = item.selected;
      item.selected = selected;
    });

    try {
      await cartApi.selectAll(selected);
      await fetchCart(); // 重新拉取汇总数据
    } catch (err) {
      // 回滚
      cartItems.value.forEach(item => {
        item.selected = oldSelectedMap[item.id];
      });
      error.value = err.message;
      alert('全选操作失败：' + err.message);
    }
  };

  return {
    cartItems,
    loading,
    error,
    checkedCount,
    totalAmount,
    cartTotalCount,
    fetchCart,
    addToCart,
    updateQuantity,
    toggleCheck,
    removeItem,
    clearCart,
    toggleSelectAll,
  };
});