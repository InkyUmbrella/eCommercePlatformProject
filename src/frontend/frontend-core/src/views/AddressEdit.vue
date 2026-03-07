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
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// 模拟省市区数据（实际项目中可从后端接口获取）
const provinceList = ref([
  { code: '110000', name: '北京市' },
  { code: '310000', name: '上海市' },
  { code: '440000', name: '广东省' },
  { code: '330000', name: '浙江省' },
  { code: '510000', name: '四川省' }
]);

// 城市列表（根据省份切换）
const cityList = ref([]);
// 区县列表（根据城市切换）
const areaList = ref([]);

// 模拟省市区映射数据
const regionData = {
  '110000': [
    { code: '110100', name: '北京市' },
  ],
  '310000': [
    { code: '310100', name: '上海市' },
  ],
  '440000': [
    { code: '440100', name: '广州市' },
    { code: '440300', name: '深圳市' },
    { code: '440600', name: '佛山市' }
  ],
  '330000': [
    { code: '330100', name: '杭州市' },
    { code: '330200', name: '宁波市' },
    { code: '330300', name: '温州市' }
  ],
  '510000': [
    { code: '510100', name: '成都市' },
    { code: '510200', name: '重庆市' },
    { code: '510300', name: '自贡市' }
  ],
  // 城市对应的区县
  '110100': [
    { code: '110101', name: '东城区' },
    { code: '110102', name: '西城区' },
    { code: '110105', name: '朝阳区' },
    { code: '110106', name: '丰台区' }
  ],
  '310100': [
    { code: '310101', name: '黄浦区' },
    { code: '310104', name: '徐汇区' },
    { code: '310105', name: '长宁区' }
  ],
  '440100': [
    { code: '440103', name: '荔湾区' },
    { code: '440104', name: '越秀区' },
    { code: '440105', name: '海珠区' }
  ],
  '440300': [
    { code: '440303', name: '罗湖区' },
    { code: '440304', name: '福田区' },
    { code: '440305', name: '南山区' }
  ]
};

// 接收路由传递的地址ID（编辑已有地址）
const addressId = route.query.addressId;

// 地址表单数据
const address = ref({
  id: addressId || Date.now(), // 地址ID
  name: '', // 收货人
  phone: '', // 手机号
  province: '', // 省份编码
  city: '', // 城市编码
  area: '', // 区县编码
  detail: '', // 详细地址
  zipCode: '', // 邮政编码
  isDefault: false // 是否默认地址
});

// 初始化：如果是编辑已有地址，加载原有数据
onMounted(() => {
  // 模拟从接口获取原有地址数据
  if (addressId) {
    const defaultAddress = {
      id: addressId,
      name: '张三',
      phone: '13800138000',
      province: '110000',
      city: '110100',
      area: '110101',
      detail: '东城区某某小区1号楼2单元301',
      zipCode: '100010',
      isDefault: true
    };
    address.value = defaultAddress;
    
    // 初始化省市区下拉框
    handleProvinceChange();
    handleCityChange();
  }
});

// 省份切换事件
const handleProvinceChange = () => {
  if (address.value.province) {
    cityList.value = regionData[address.value.province] || [];
    // 清空城市和区县
    address.value.city = '';
    address.value.area = '';
    areaList.value = [];
  }
};

// 城市切换事件
const handleCityChange = () => {
  if (address.value.city) {
    areaList.value = regionData[address.value.city] || [];
    // 清空区县
    address.value.area = '';
  }
};

// 保存地址
const saveAddress = () => {
  // 表单验证
  if (!address.value.name) {
    alert('请输入收货人姓名！');
    return;
  }
  if (!/^1[3-9]\d{9}$/.test(address.value.phone)) {
    alert('请输入正确的手机号！');
    return;
  }
  if (!address.value.province || !address.value.city || !address.value.area) {
    alert('请选择完整的省市区！');
    return;
  }
  if (!address.value.detail) {
    alert('请输入详细地址！');
    return;
  }

  // 模拟提交到后端
  console.log('修改后的地址数据：', address.value);
  alert('地址修改成功！');
  // 跳回上一页（商品详情页）
  router.go(-1);
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