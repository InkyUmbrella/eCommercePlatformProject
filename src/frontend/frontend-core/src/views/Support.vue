<template>
  <div class="support-page">
    <h1>客服留言</h1>

    <el-card class="form-card">
      <template #header>提交留言</template>
      <el-form label-position="top">
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="请输入昵称（不填则匿名）" />
        </el-form-item>
        <el-form-item label="联系方式（选填）">
          <el-input v-model="form.contact" placeholder="邮箱或手机号" />
        </el-form-item>
        <el-form-item label="留言内容">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="4"
            maxlength="500"
            show-word-limit
            placeholder="请输入留言内容"
          />
        </el-form-item>
        <el-button type="primary" :loading="submitting" @click="submitMessage">提交留言</el-button>
      </el-form>
    </el-card>

    <el-card class="list-card">
      <template #header>
        <div class="header-row">
          <span>留言列表</span>
          <el-button text @click="fetchMessages">刷新</el-button>
        </div>
      </template>

      <el-empty v-if="!loading && messages.length === 0" description="暂无留言" />

      <div v-loading="loading" class="message-list">
        <el-card v-for="item in messages" :key="item.id" class="message-item" shadow="never">
          <div class="meta">
            <span class="nickname">{{ item.nickname }}</span>
            <span class="time">{{ formatTime(item.created_at) }}</span>
          </div>
          <p class="content">{{ item.content }}</p>

          <div v-if="item.is_replied && item.reply_content" class="reply-box">
            <div class="reply-title">客服回复</div>
            <div>{{ item.reply_content }}</div>
            <div class="reply-time" v-if="item.replied_at">{{ formatTime(item.replied_at) }}</div>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || ''
})

const loading = ref(false)
const submitting = ref(false)
const messages = ref([])
const form = reactive({
  nickname: '',
  contact: '',
  content: ''
})

const fetchMessages = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/support/messages/')
    if (data.code === 0) {
      messages.value = Array.isArray(data.data) ? data.data : []
      return
    }
    ElMessage.error(data.message || '获取留言失败')
  } catch {
    ElMessage.error('获取留言失败，请检查后端服务')
  } finally {
    loading.value = false
  }
}

const submitMessage = async () => {
  if (!form.content.trim()) {
    ElMessage.warning('请先输入留言内容')
    return
  }
  submitting.value = true
  try {
    const payload = {
      nickname: form.nickname,
      contact: form.contact,
      content: form.content
    }
    const { data } = await api.post('/api/support/messages/', payload)
    if (data.code === 0) {
      ElMessage.success('留言提交成功')
      form.nickname = ''
      form.contact = ''
      form.content = ''
      await fetchMessages()
      return
    }
    ElMessage.error(data.message || '留言提交失败')
  } catch {
    ElMessage.error('留言提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const formatTime = (value) => {
  if (!value) {
    return ''
  }
  const dt = new Date(value)
  if (Number.isNaN(dt.getTime())) {
    return value
  }
  return dt.toLocaleString('zh-CN', { hour12: false })
}

onMounted(fetchMessages)
</script>

<style scoped>
.support-page {
  max-width: 900px;
  margin: 24px auto;
  padding: 0 16px 24px;
}

.form-card,
.list-card {
  margin-top: 16px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-list {
  min-height: 100px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  border: 1px solid #ebeef5;
}

.meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 13px;
}

.nickname {
  font-weight: 600;
  color: #303133;
}

.content {
  margin: 10px 0;
  white-space: pre-wrap;
}

.reply-box {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 10px 12px;
}

.reply-title {
  font-weight: 600;
  margin-bottom: 6px;
}

.reply-time {
  margin-top: 6px;
  color: #909399;
  font-size: 12px;
}
</style>