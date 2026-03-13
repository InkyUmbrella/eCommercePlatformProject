<template>
  <div class="login-container">
    <!-- 背景装饰图（可选，模拟美妆环绕效果） -->
    <div class="background-decoration"></div>

    <!-- 登录卡片主体 -->
    <div class="login-card">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <!-- Hello Kitty 图片 -->
        <img src="@/assets/hello-kitty.jpeg" alt="Hello Kitty" class="brand-logo" />
        <h1 class="brand-title">beauty</h1>
        <p class="brand-slogan">美妆，为精致生活加分</p>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <!-- 表单标题 -->
        <h2>创建账号</h2>
        
        <el-form :model="form" ref="formRef" :rules="rules" label-width="0px" class="login-form">
    <el-form-item prop="username">
      <el-input v-model="form.username" placeholder="请输入昵称" size="large" prefix-icon="el-icon-user" />
    </el-form-item>

    <el-form-item prop="password">
      <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="el-icon-lock" />
    </el-form-item>

    <!-- 可选：添加确认密码字段（前端验证） -->
    <el-form-item prop="confirmPassword">
      <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" size="large" prefix-icon="el-icon-lock" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" size="large" class="submit-btn" @click="handleSubmit">立即注册</el-button>
    </el-form-item>
  </el-form>

        <!-- 底部链接 -->
        <div class="form-footer">
          <span>已经有美妆商城账号？</span>
          <!-- router-link 会自动渲染为 a 标签，to 属性对应路由地址 -->
          <router-link to="/login" class="link-btn">去登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

import { ElMessage } from 'element-plus';
import { useUserStore } from '@/store/userStore';
const formRef = ref(null);
const router = useRouter();
const userStore = useUserStore();
const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入密码不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
};
const handleSubmit = async () => {
  if (!formRef.value) return;
  try {
    await formRef.value.validate();
    // 调用 store 的注册方法
    await userStore.register(form.username, form.password);
    // 注册成功后会跳转到登录页（已经在 store 中处理）
    ElMessage.success('注册成功，请登录');
  } catch (error) {
    // 验证不通过或注册失败
    if (error.message) {
      ElMessage.error(error.message);
    }
  }
};
</script>

<style scoped>
/* 全局容器，实现全屏居中 */
.login-container {
  width: 100vw;
  height: 100vh;
  background-color: #FFF0F5; /* 淡粉色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 模拟背景美妆图片的模糊效果（可选） */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/bg-makeup.jpg') no-repeat center center;
  background-size: cover;
  opacity: 0.3; /* 降低透明度作为底纹 */
  z-index: 0;
}

/* 登录卡片 */
.login-card {
  width: 800px;
  height: 500px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(255, 192, 203, 0.3);
  display: flex;
  z-index: 1;
  overflow: hidden;
}
.login-card {
  width: 800px;
  height: 500px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 15px 40px rgba(255, 105, 180, 0.3),  
    0 5px 15px rgba(255, 192, 203, 0.4),    
    inset 0 1px 0 rgba(255, 255, 255, 0.8); 
  display: flex;
  z-index: 1;
  overflow: hidden;
  transform: perspective(1000px) translateY(-2px) rotateX(2deg);
}

/* 左侧品牌区域 */
.brand-section {
  width: 40%;
  height: 100%;
  background-color: #FFC0CB; /* 粉色背景 */
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  text-align: center;
}

.brand-logo {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
  border-radius: 50%;
  object-fit: cover;
  overflow: hidden;
  border: 3px solid #ffffff; /* 白色边框 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 轻微阴影，增强立体感 */
}

.brand-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.brand-slogan {
  font-size: 14px;
  opacity: 0.8;
}

/* 右侧表单区域 */
.form-section {
  width: 60%;
  height: 100%;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
}
.form-section h2 {
  text-align: center;
  margin-bottom: 50px;  /* 当前间距 */
  color: #333;
  font-size: 20px;
}

.login-form {
  margin-bottom: 20px;
}



/* 提交按钮样式 */
.submit-btn {
  width: 100%;
  background-color: #FFB6C1;
  border: none;
  height: 45px;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #FFC0CB;
}

/* 底部链接 */
.form-footer {
  text-align: center;
  font-size: 12px;
  color: #666;
  margin-top: 10px;
}

.link-btn {
  color: #FF69B4;
  text-decoration: none;
  margin-left: 5px;
}

.link-btn:hover {
  text-decoration: underline;
}

/* 响应式适配：在小屏幕（如手机）上改为上下布局 */
@media (max-width: 768px) {
  .login-card {
    flex-direction: column;
    width: 90%;
    height: auto;
  }

  .brand-section, .form-section {
    width: 100%;
  }

  .brand-section {
    padding: 20px;
    height: 200px;
  }
}
</style>