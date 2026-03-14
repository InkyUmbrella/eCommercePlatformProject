<template>
  <div class="address-edit-container">
    <header class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h1 class="page-title">{{ addressId ? '修改收货地址' : '新增收货地址' }}</h1>
      <button class="save-btn" @click="saveAddress">保存</button>
    </header>

    <form class="address-form" @submit.prevent="saveAddress">
      <div class="form-item">
        <label class="form-label">收货人</label>
        <input
          v-model="address.name"
          type="text"
          class="form-input"
          placeholder="请输入收货人姓名"
          required
        />
      </div>

      <div class="form-item">
        <label class="form-label">手机号</label>
        <input
          v-model="address.phone"
          type="tel"
          class="form-input"
          placeholder="请输入手机号"
          maxlength="11"
          required
        />
      </div>

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

      <div class="form-item">
        <label class="form-label">详细地址</label>
        <input
          v-model="address.detail"
          type="text"
          class="form-input"
          placeholder="请输入街道、小区、门牌号等"
          required
        />
      </div>

      <div class="form-item">
        <label class="form-label">邮政编码</label>
        <input
          v-model="address.zipCode"
          type="text"
          class="form-input"
          placeholder="选填"
          maxlength="6"
        />
      </div>

      <div class="form-item checkbox-item">
        <label class="checkbox-label">
          <input
            v-model="address.isDefault"
            type="checkbox"
            class="checkbox-input"
          />
          <span class="checkbox-text">设为默认收货地址</span>
        </label>
      </div>
    </form>

    <div class="bottom-actions">
      <button class="cancel-btn" @click="goBack">取消</button>
      <button class="confirm-btn" @click="saveAddress">确认保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import * as addressApi from '@/api/address';
import regionMap from '@/data/regions.json';

const ROOT_REGION_CODE = '86';
const MUNICIPALITY_CODES = new Set(['110000', '120000', '310000', '500000']);
const DIRECT_COUNTY_NAMES = new Set(['市辖区', '县']);

const router = useRouter();
const route = useRoute();

const buildOptions = (map = {}, transformName) =>
  Object.entries(map).map(([code, name]) => ({
    code,
    name: transformName ? transformName(code, name) : name,
  }));

const loading = ref(false);
const provinceList = ref(buildOptions(regionMap[ROOT_REGION_CODE]));
const cityList = ref([]);
const areaList = ref([]);

const addressId = route.query.addressId;

const address = reactive({
  id: null,
  name: '',
  phone: '',
  province: '',
  city: '',
  area: '',
  detail: '',
  zipCode: '',
  isDefault: false,
});

const getProvinceName = (provinceCode) => regionMap[ROOT_REGION_CODE]?.[provinceCode] || '';
const getCityMap = (provinceCode) => regionMap[provinceCode] || {};
const getCityName = (provinceCode, cityCode) => getCityMap(provinceCode)?.[cityCode] || '';
const getAreaMap = (cityCode) => regionMap[cityCode] || {};
const getAreaName = (cityCode, areaCode) => getAreaMap(cityCode)?.[areaCode] || '';

const getCityDisplayName = (provinceCode, cityCode) => {
  const cityName = getCityName(provinceCode, cityCode);
  if (MUNICIPALITY_CODES.has(provinceCode) && DIRECT_COUNTY_NAMES.has(cityName)) {
    return getProvinceName(provinceCode);
  }
  return cityName;
};

const shouldIncludeCityName = (provinceCode, cityCode) => {
  const cityName = getCityName(provinceCode, cityCode);
  return !DIRECT_COUNTY_NAMES.has(cityName);
};

const syncCityList = () => {
  cityList.value = buildOptions(getCityMap(address.province), (code) =>
    getCityDisplayName(address.province, code),
  );
};

const syncAreaList = () => {
  areaList.value = buildOptions(getAreaMap(address.city));
};

const inferRegionFromAddress = (fullAddress = '') => {
  for (const [provinceCode, provinceName] of Object.entries(regionMap[ROOT_REGION_CODE] || {})) {
    if (!fullAddress.includes(provinceName)) continue;

    for (const [cityCode, rawCityName] of Object.entries(getCityMap(provinceCode))) {
      const cityInAddress = shouldIncludeCityName(provinceCode, cityCode) ? rawCityName : '';
      if (cityInAddress && !fullAddress.includes(cityInAddress)) continue;

      for (const [areaCode, areaName] of Object.entries(getAreaMap(cityCode))) {
        if (!fullAddress.includes(areaName)) continue;

        const regionText = `${provinceName}${cityInAddress}${areaName}`;
        return {
          province: provinceCode,
          city: cityCode,
          area: areaCode,
          detail: fullAddress.replace(regionText, '').trim(),
        };
      }
    }
  }

  return {
    province: '',
    city: '',
    area: '',
    detail: fullAddress,
  };
};

const fillAddressForm = (res) => {
  address.id = res.id;
  address.name = res.name || '';
  address.phone = res.phone_number || '';
  address.isDefault = Boolean(res.is_default);

  const parsed = inferRegionFromAddress(res.address || '');
  address.province = parsed.province;
  syncCityList();
  address.city = parsed.city;
  syncAreaList();
  address.area = parsed.area;
  address.detail = parsed.detail;
};

onMounted(async () => {
  if (!addressId) return;

  loading.value = true;
  try {
    let res;
    try {
      res = await addressApi.getAddressDetail(addressId);
    } catch {
      const addresses = await addressApi.getAddresses();
      res = addresses.find((item) => String(item.id) === String(addressId));
    }

    if (!res) {
      throw new Error('地址不存在');
    }

    fillAddressForm(res);
  } catch (err) {
    ElMessage.error(err?.message || '获取地址详情失败');
  } finally {
    loading.value = false;
  }
});

const handleProvinceChange = () => {
  syncCityList();
  address.city = '';
  address.area = '';
  areaList.value = [];
};

const handleCityChange = () => {
  syncAreaList();
  address.area = '';
};

const buildRedirectLocation = (redirect) => {
  const [path, queryString = ''] = String(redirect || '').split('?');
  const query = Object.fromEntries(new URLSearchParams(queryString).entries());
  return {
    path: path || '/checkout',
    query: { ...query, _t: Date.now() },
  };
};

const saveAddress = async () => {
  if (!address.name.trim()) {
    ElMessage.warning('请输入收货人姓名');
    return;
  }

  if (!/^1[3-9]\d{9}$/.test(address.phone)) {
    ElMessage.warning('请输入正确的手机号');
    return;
  }

  if (!address.province || !address.city || !address.area) {
    ElMessage.warning('请选择完整的省市区');
    return;
  }

  if (!address.detail.trim()) {
    ElMessage.warning('请输入详细地址');
    return;
  }

  const provinceName = getProvinceName(address.province);
  const cityName = shouldIncludeCityName(address.province, address.city)
    ? getCityName(address.province, address.city)
    : '';
  const areaName = getAreaName(address.city, address.area);
  const payload = {
    name: address.name.trim(),
    phone_number: address.phone.trim(),
    address: `${provinceName}${cityName}${areaName}${address.detail.trim()}`,
    is_default: address.isDefault,
  };

  loading.value = true;
  try {
    if (addressId) {
      await addressApi.updateAddress(addressId, payload);
    } else {
      await addressApi.createAddress(payload);
    }

    ElMessage.success(addressId ? '地址修改成功' : '地址添加成功');

    const redirect = route.query.redirect || '/checkout';
    router.push(buildRedirectLocation(redirect));
  } catch (err) {
    ElMessage.error(err?.message || '保存失败');
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
/* 页面容器样式 */
.address-edit-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #fff9f7;
  font-family: 'Microsoft YaHei', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 顶部导航栏 */
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

/* 表单容器样式 */
.address-form {
  padding: 15px;
  background-color: #fff;
  margin: 10px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}

/* 表单项样式 */
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

/* 地区选择区域样式 */
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

/* 默认地址复选框样式 */
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

/* 底部操作按钮区域 */
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

/* 桌面端适配布局 */
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
