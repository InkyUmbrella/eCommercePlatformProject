<template>
  <div class="support-page">
    <div class="page-actions">
      <el-button @click="goHome">返回首页</el-button>
      <el-button @click="handleSwitchAccount">切换账号</el-button>
      <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
    </div>
    <h1>留言板</h1>

    <el-card class="staff-card">
      <template #header>客服回复模式（管理员）</template>
      <div class="staff-row">
        <el-input
          v-model="staffToken"
          type="password"
          show-password
          clearable
          placeholder="粘贴管理员 access token（仅回复时需要）"
        />
        <el-button type="primary" @click="saveStaffToken">保存 Token</el-button>
        <el-button @click="clearStaffToken">清空</el-button>
      </div>
      <p class="staff-tip">
        当前状态：
        <el-tag :type="isReplyMode ? 'success' : 'info'" size="small">
          {{ isReplyMode ? '已启用回复模式' : '未启用回复模式' }}
        </el-tag>
      </p>
    </el-card>

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
          <span>留言列表（最新 50 条）</span>
          <el-button text @click="fetchMessages">刷新</el-button>
        </div>
      </template>

      <el-empty v-if="!loading && messages.length === 0" description="暂无留言" />

      <div v-loading="loading" class="message-list">
        <el-card v-for="item in messages" :key="item.id" class="message-item" shadow="never">
          <div class="meta">
            <span class="nickname">{{ item.nickname }}</span>
            <div class="meta-right">
              <el-tag size="small" :type="item.is_replied ? 'success' : 'warning'">
                {{ item.is_replied ? '已回复' : '待回复' }}
              </el-tag>
              <span class="time">{{ formatTime(item.created_at) }}</span>
            </div>
          </div>
          <p class="content">{{ item.content }}</p>

          <div v-if="item.is_replied && item.reply_content" class="reply-box">
            <div class="reply-title">客服回复</div>
            <div>{{ item.reply_content }}</div>
            <div class="reply-time" v-if="item.replied_at">{{ formatTime(item.replied_at) }}</div>
          </div>

          <div v-else-if="isReplyMode" class="reply-editor">
            <el-input
              v-model="replyDrafts[item.id]"
              type="textarea"
              :rows="2"
              maxlength="500"
              show-word-limit
              placeholder="输入客服回复内容..."
            />
            <div class="reply-actions">
              <el-button
                type="primary"
                size="small"
                :loading="replyingId === item.id"
                @click="submitReply(item.id)"
              >
                提交回复
              </el-button>
            </div>
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
import { useRouter } from 'vue-router'
import { useAuthActions } from '@/composables/useAuthActions'

const SUPPORT_STAFF_TOKEN_KEY = 'support_staff_token'
const router = useRouter()
const { logout, switchAccount } = useAuthActions()

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || ''
})

const loading = ref(false)
const submitting = ref(false)
const replyingId = ref(null)
const messages = ref([])
const replyDrafts = reactive({})
const staffToken = ref('')
const isReplyMode = ref(false)

const form = reactive({
  nickname: '',
  contact: '',
  content: ''
})

const saveStaffToken = () => {
  const token = staffToken.value.trim()
  if (!token) {
    ElMessage.warning('请先输入 token')
    return
  }
  localStorage.setItem(SUPPORT_STAFF_TOKEN_KEY, token)
  isReplyMode.value = true
  ElMessage.success('已保存 token，回复模式已启用')
}

const clearStaffToken = () => {
  localStorage.removeItem(SUPPORT_STAFF_TOKEN_KEY)
  staffToken.value = ''
  isReplyMode.value = false
  ElMessage.success('已清空 token')
}

const getAuthHeader = () => {
  const token = localStorage.getItem(SUPPORT_STAFF_TOKEN_KEY) || ''
  if (!token) {
    return {}
  }
  return {
    Authorization: `Bearer ${token}`
  }
}

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

const submitReply = async (messageId) => {
  const replyContent = String(replyDrafts[messageId] || '').trim()
  if (!replyContent) {
    ElMessage.warning('请先输入回复内容')
    return
  }

  if (!isReplyMode.value) {
    ElMessage.warning('请先启用回复模式并保存 token')
    return
  }

  replyingId.value = messageId
  try {
    const { data } = await api.patch(
      `/api/support/messages/${messageId}/reply/`,
      { reply_content: replyContent },
      { headers: getAuthHeader() }
    )
    if (data.code === 0) {
      ElMessage.success('回复成功')
      replyDrafts[messageId] = ''
      await fetchMessages()
      return
    }
    ElMessage.error(data.message || '回复失败')
  } catch (error) {
    const status = error?.response?.status
    if (status === 401) {
      ElMessage.error('未授权，请检查 token 是否有效')
    } else if (status === 403) {
      ElMessage.error('权限不足，仅管理员可回复')
    } else {
      ElMessage.error('回复失败，请稍后重试')
    }
  } finally {
    replyingId.value = null
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

const goHome = () => router.push('/home')

const handleLogout = async () => {
  try {
    await logout()
  } catch (_) {}
}

const handleSwitchAccount = async () => {
  try {
    await switchAccount()
  } catch (_) {}
}

onMounted(() => {
  staffToken.value = localStorage.getItem(SUPPORT_STAFF_TOKEN_KEY) || ''
  isReplyMode.value = Boolean(staffToken.value.trim())
  fetchMessages()
})
</script>

<style scoped>
.support-page {
  max-width: 900px;
  margin: 24px auto;
  padding: 0 16px 24px;
}

.page-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.staff-card,
.form-card,
.list-card {
  margin-top: 16px;
}

.staff-row {
  display: flex;
  gap: 10px;
}

.staff-tip {
  margin: 10px 0 0;
  color: #606266;
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
  align-items: center;
  gap: 8px;
}

.meta-right {
  display: inline-flex;
  align-items: center;
  gap: 8px;
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

.reply-editor {
  margin-top: 10px;
}

.reply-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .staff-row {
    flex-direction: column;
  }
}
</style>
