<template>
  <div class="home-container">
    <header class="header">
      <h2>Beauty 商城</h2>
      <div class="nav">
        <button @click="goToCart">购物车</button>
        <button @click="goToOrders">订单</button>
      </div>
    </header>

    <div v-if="loading" class="info">加载中...</div>
    <div v-else-if="error" class="info error">{{ error }}</div>

    <template v-else>
      <section class="banners" v-if="banners.length">
        <div class="banner" v-for="item in banners" :key="item.id" @click="openLink(item.link)">
          <img :src="item.image" :alt="item.title" />
          <div class="overlay">
            <h3>{{ item.title }}</h3>
            <p>{{ item.subtitle }}</p>
          </div>
        </div>
      </section>

      <section>
        <h3>新品上架</h3>
        <div class="products">
          <div class="product" v-for="item in newProducts" :key="item.id" @click="goToDetail(item.id)">
            <img :src="item.cover_image" :alt="item.name" />
            <p>{{ item.name }}</p>
            <strong>￥{{ item.price }}</strong>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import * as homeApi from '@/api/home';

const router = useRouter();
const banners = ref([]);
const newProducts = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchHomeData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const [bannerData, newProductData] = await Promise.all([
      homeApi.getBanners(),
      homeApi.getNewProducts(),
    ]);
    banners.value = bannerData || [];
    newProducts.value = newProductData || [];
  } catch (err) {
    error.value = err.message;
    ElMessage.error(`加载首页失败: ${err.message}`);
  } finally {
    loading.value = false;
  }
};

const openLink = (link) => {
  if (link) router.push(link);
};

const goToDetail = (id) => router.push(`/product-detail/${id}`);
const goToCart = () => router.push('/cart');
const goToOrders = () => router.push('/orders');

onMounted(fetchHomeData);
</script>

<style scoped>
.home-container { padding: 16px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.nav button { margin-left: 8px; }
.banners { display: grid; gap: 10px; margin-bottom: 16px; }
.banner { position: relative; border-radius: 8px; overflow: hidden; cursor: pointer; }
.banner img { width: 100%; height: 200px; object-fit: cover; }
.overlay { position: absolute; left: 0; right: 0; bottom: 0; padding: 8px; color: #fff; background: linear-gradient(transparent, rgba(0,0,0,.6)); }
.products { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px,1fr)); gap: 12px; }
.product { border: 1px solid #eee; border-radius: 8px; padding: 8px; cursor: pointer; }
.product img { width: 100%; height: 140px; object-fit: cover; border-radius: 6px; }
.info { padding: 16px; }
.info.error { color: #c00; }
</style>
