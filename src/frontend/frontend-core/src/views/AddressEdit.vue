<template>
  <div class="address-edit-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <button class="back-btn" @click="goBack">← 返回</button>
      <h1 class="page-title">修改收货地址</h1>
      <button class="save-btn" @click="saveAddress">保存</button>
    </header>

    <!-- 地址编辑表单 -->
    <form class="address-form">
      <!-- 收货人 -->
      <div class="form-item">
        <label class="form-label">收货人</label>
        <input 
          type="text" 
          v-model="address.name" 
          class="form-input" 
          placeholder="请输入收货人姓名"
          required
        />
      </div>

      <!-- 手机号 -->
      <div class="form-item">
        <label class="form-label">手机号</label>
        <input 
          type="tel" 
          v-model="address.phone" 
          class="form-input" 
          placeholder="请输入手机号"
          maxlength="11"
          required
        />
      </div>

      <!-- 省市区三级联动 -->
      <div class="form-item">
        <label class="form-label">所在地区</label>
        <div class="region-select">
          <select v-model="address.province" @change="handleProvinceChange" class="region-input">
            <option value="">请选择省份</option>
            <option v-for="province in provinceList" :key="province.code" :value="province.code">
              {{ province.name }}
            </option>
          </select>
          <select v-model="address.city" @change="handleCityChange" class="region-input">
            <option value="">请选择城市</option>
            <option v-for="city in cityList" :key="city.code" :value="city.code">
              {{ city.name }}
            </option>
          </select>
          <select v-model="address.area" class="region-input">
            <option value="">请选择区县</option>
            <option v-for="area in areaList" :key="area.code" :value="area.code">
              {{ area.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- 详细地址 -->
      <div class="form-item">
        <label class="form-label">详细地址</label>
        <input 
          type="text" 
          v-model="address.detail" 
          class="form-input" 
          placeholder="请输入街道、小区、门牌号等"
          required
        />
      </div>

      <!-- 邮政编码（可选） -->
      <div class="form-item">
        <label class="form-label">邮政编码</label>
        <input 
          type="text" 
          v-model="address.zipCode" 
          class="form-input" 
          placeholder="选填"
          maxlength="6"
        />
      </div>

      <!-- 默认地址 -->
      <div class="form-item checkbox-item">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="address.isDefault" 
            class="checkbox-input"
          />
          <span class="checkbox-text">设为默认收货地址</span>
        </label>
      </div>
    </form>

    <!-- 底部操作栏 -->
    <div class="bottom-actions">
      <button class="cancel-btn" @click="goBack">取消</button>
      <button class="confirm-btn" @click="saveAddress">确认修改</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus'; // 使用 Element Plus 提示
import * as addressApi from '@/api/address';

const router = useRouter();
const route = useRoute();

// 加载状态
const loading = ref(false);

// 省市区模拟数据（保持不变，如果后端提供省市区接口，也可以改为从后端获取）
const provinceList = ref([/* ... 保持不变 ... */]);
const cityList = ref([]);

const areaList = ref([]);
const regionData = { /* ... 保持不变 ... */ };

// 路由参数：addressId 存在时为编辑模式，否则为新增
const addressId = route.query.addressId;

// 地址表单数据（与后端字段对应）
const address = reactive({
  id: null,
  name: '',          // 收货人
  phone: '',          // 手机号（前端字段）
  province: '',
  city: '',
  area: '',
  detail: '',
  zipCode: '',
  isDefault: false    // 是否默认
});

// 初始化
onMounted(async () => {
  if (addressId) {
    // 编辑模式：获取地址详情
    loading.value = true;
    try {
      // 假设后端有详情接口，返回数据格式如：{ id, name, phone_number, address, is_default, ... }
      const res = await addressApi.getAddressDetail(addressId);
      // 填充表单，需要将后端字段映射到前端
      address.id = res.id;
      address.name = res.name;
      address.phone = res.phone_number;
      address.isDefault = res.is_default;
      
      // 地址字符串解析（假设后端存储的 address 是完整地址，如 "北京市东城区某某小区1号楼2单元301"）
      // 这里简单处理：无法反向解析出省市区，所以省市区可能无法回显，需要后端分别返回省市区字段。
      // 如果后端只返回完整字符串，那么编辑时省市区下拉框无法自动选中，需要用户重新选择。
      // 为了更好体验，建议后端增加 province_code, city_code, area_code 字段。
      // 此处先模拟解析，实际开发需要与后端协调。
      // 我们暂时将完整地址赋值给 detail，省市区留空让用户重新选择。
      address.detail = res.address || '';
      
      // 初始化省市区下拉框（根据解析出的编码，此处无编码，所以无法自动选中）
      // 可以清空已选值
      address.province = '';
      address.city = '';
      address.area = '';
    } catch (err) {
      ElMessage.error('获取地址详情失败：' + err.message);
    } finally {
      loading.value = false;
    }
  }
});

// 省份切换事件
const handleProvinceChange = () => {
  if (address.province) {
    cityList.value = regionData[address.province] || [];
    address.city = '';
    address.area = '';
    areaList.value = [];
  }
};

// 城市切换事件
const handleCityChange = () => {
  if (address.city) {
    areaList.value = regionData[address.city] || [];
    address.area = '';
  }
};

// 保存地址
const saveAddress = async () => {
  // 表单验证
  if (!address.name) {
    ElMessage.warning('请输入收货人姓名！');
    return;
  }
  if (!/^1[3-9]\d{9}$/.test(address.phone)) {
    ElMessage.warning('请输入正确的手机号！');
    return;
  }
  if (!address.province || !address.city || !address.area) {
    ElMessage.warning('请选择完整的省市区！');
    return;
  }
  if (!address.detail) {
    ElMessage.warning('请输入详细地址！');
    return;
  }

  loading.value = true;

   try {
    if (addressId) {
      await addressApi.updateAddress(addressId, payload);
    } else {
      await addressApi.createAddress(payload);
    }
    ElMessage.success(addressId ? '地址修改成功' : '地址添加成功');
    const redirect = route.query.redirect || '/addresses';
    if (redirect === '/checkout') {
      // 返回确认页并添加时间戳参数，触发刷新
      router.push({ path: redirect, query: { _t: Date.now() } });
    } else {
      router.push(redirect);
    }
  } catch (err) {
    ElMessage.error('保存失败：' + err.message);
  }
};

// 返回上一页
const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
/* 全局容器 */
.address-edit-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 15px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}
.back-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  padding: 5px 10px;
}
.page-title {
  font-size: 18px;
  color: #333;
  font-weight: 600;
  margin: 0;
}
.save-btn {
  background-color: #ff69b4;
  border: none;
  border-radius: 6px;
  color: #fff;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}

/* 表单容器 */
.address-form {
  padding: 15px;
  background-color: #fff;
  margin: 10px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}

/* 表单项 */
.form-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ffe6ef;
}
.form-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}
.form-input {
  padding: 10px 12px;
  border: 1px solid #ffc0cb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}
.form-input:focus {
  border-color: #ff69b4;
}

/* 省市区选择 */
.region-select {
  display: flex;
  gap: 8px;
}
.region-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ffc0cb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}
.region-input:focus {
  border-color: #ff69b4;
}

/* 复选框项 */
.checkbox-item {
  border-bottom: none;
}
.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.checkbox-input {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  accent-color: #ff69b4;
}
.checkbox-text {
  font-size: 14px;
  color: #333;
}

/* 底部操作栏 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background-color: #fff;
  padding: 15px;
  box-shadow: 0 -2px 8px rgba(255, 192, 203, 0.1);
  z-index: 99;
}
.cancel-btn {
  flex: 1;
  padding: 12px;
  background-color: #fff;
  border: 1px solid #ffc0cb;
  border-radius: 8px;
  color: #ff69b4;
  font-size: 16px;
  cursor: pointer;
  margin-right: 10px;
}
.confirm-btn {
  flex: 1;
  padding: 12px;
  background-color: #ff69b4;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}
.confirm-btn:hover {
  background-color: #ff87b8;
}

/* 响应式适配 */
@media (min-width: 768px) {
  .address-form {
    width: 600px;
    margin: 20px auto;
  }
  .bottom-actions {
    width: 600px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 12px 12px 0 0;
  }
}
</style>