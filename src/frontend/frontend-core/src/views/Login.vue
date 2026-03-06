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
        <h1 class="brand-title">Beauty</h1>
        <p class="brand-slogan">美妆，为精致生活加分</p>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <!-- 表单标题 -->
        <h2>登录账号</h2>
        
        <el-form :model="loginForm" ref="loginFormRef" label-width="0px" class="login-form">
          <el-form-item prop="email">
            <el-input v-model="loginForm.email" placeholder="请输入邮箱" size="large" prefix-icon="el-icon-message" />
          </el-form-item>

          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" size="large" prefix-icon="el-icon-lock" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" size="large" class="submit-btn" @click="handleLogin">立即登录</el-button>
          </el-form-item>
        </el-form>

        <!-- 跳回注册页的链接 -->
        <div class="form-footer">
          <span>还没有账号？</span>
          <router-link to="/" class="link-btn">去注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 表单引用（必须与模板中的 ref="loginFormRef" 一致）
const loginFormRef = ref(null)
const router = useRouter()     

// 登录表单数据（必须与模板中的 :model="loginForm" 一致）
const loginForm = reactive({
  email: '',

  password: ''
})

// 登录按钮点击事件（必须与模板中的 @click="handleLogin" 一致）
const handleLogin = () => {
  // 调用 Element Plus 表单验证
  loginFormRef.value.validate((valid) => {
    if (valid) {
      console.log('登录数据:', loginForm)
      ElMessage.success('登录成功！')
      router.push('/home')   // 跳转到首页
    } else {
      ElMessage.error('请填写邮箱和密码')
    }
  })
}
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

/* 验证码按钮样式 */
.code-btn {
  width: 100%;
  background-color: #FFB6C1;
  border: none;
}

.code-btn:hover {
  background-color: #FFC0CB;
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