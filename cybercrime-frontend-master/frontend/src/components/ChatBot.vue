<template>
  <div class="chatbot-container">
    <!-- 聊天按钮 -->
    <div v-if="!isOpen" class="chat-toggle" @click="toggleChat">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </div>

    <!-- 聊天窗口 -->
    <div v-if="isOpen" class="chat-window">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="chat-title">
          <div class="bot-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="title-text">
            <h3>Guardey</h3>
          </div>
        </div>
        <button class="close-btn" @click="toggleChat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <div class="message bot-message">
          <div class="message-avatar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="message-content">
            <p>Hi! I'm Guardey, your AI assistant. How can I help you with cybersecurity questions today?</p>
            <span class="message-time">{{ getCurrentTime() }}</span>
          </div>
        </div>

        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.type + '-message'">
          <div class="message-avatar" v-if="message.type === 'bot'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="message-avatar" v-if="message.type === 'user'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <div class="message-content">
            <p v-if="message.type === 'error'" class="error-text">{{ message.text }}</p>
            <p v-else>{{ message.text }}</p>
            <span class="message-time">{{ message.time }}</span>
          </div>
        </div>

        <!-- 打字指示器 -->
        <div v-if="isTyping" class="message bot-message typing">
          <div class="message-avatar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>

        <!-- 追问建议（跟随消息区域滚动） -->
        <div v-if="followUps.length && !isTyping" class="followups">
          <div class="followup-title">You may also ask:</div>
          <div class="followup-chips">
            <button v-for="q in followUps" :key="q" class="chip" @click="chooseFollowUp(q)">{{ q }}</button>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <div class="input-container">
          <input
            v-model="inputMessage"
            @keypress.enter="sendMessage"
            placeholder="Ask a cybersecurity question..."
            class="message-input"
            :disabled="isTyping"
          />
          <button @click="sendMessage" class="send-btn" :disabled="!inputMessage.trim() || isTyping">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </div>
        <div class="retry-container" v-if="showRetry">
          <button @click="retryLastMessage" class="retry-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 4v6h6M23 20v-6h-6"/>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
            </svg>
            Retry
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)
const showRetry = ref(false)
const lastFailedMessage = ref('')
const followUps = ref([])

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => {
      scrollToBottom()
    })
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isTyping.value) return

  const userMessage = {
    type: 'user',
    text: inputMessage.value,
    time: getCurrentTime()
  }

  messages.value.push(userMessage)
  const currentInput = inputMessage.value
  inputMessage.value = ''
  showRetry.value = false
  followUps.value = []

  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })

  // 显示打字指示器
  isTyping.value = true

  try {
    // 首先尝试普通API
    await callGenerateAPI(currentInput)
  } catch (generateError) {
    console.error('Generate API failed, trying stream API:', generateError)

    try {
      // 如果普通API失败，尝试流式API
      await callStreamAPI(currentInput)
    } catch (streamError) {
      console.error('Both APIs failed:', streamError)

      // 检查是否是 CORS 错误
      if (generateError.message.includes('CORS') || generateError.message.includes('fetch')) {
        lastFailedMessage.value = currentInput
        showRetry.value = true
        addErrorMessage("Connection blocked by browser security. This may be due to CORS policy. Please ensure you're accessing this from the correct domain or consider using a proxy.")
      } else {
        lastFailedMessage.value = currentInput
        showRetry.value = true
        addErrorMessage("Connection failed. Please check your network and try again.")
      }
    }
  }
}

// 流式API调用（备用方案）
const callStreamAPI = async (prompt) => {
  const API_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/ai/chatbot/stream'

  // 创建bot消息占位符
  const botMessage = {
    type: 'bot',
    text: '',
    time: getCurrentTime()
  }
  messages.value.push(botMessage)

  // 隐藏打字指示器，显示流式回复
  isTyping.value = false

  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30秒超时

    // 最简化的请求头，避免 CORS 问题
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt: prompt.trim() }),
      signal: controller.signal
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    // 尝试流式读取
    if (response.body && response.body.getReader) {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      try {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || '' // 保留最后一个不完整的行

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6).trim()
              if (data && data !== '[DONE]') {
                botMessage.text += data
                // 实时滚动到底部
                nextTick(() => {
                  scrollToBottom()
                })
              }
            }
          }
        }
      } catch (streamError) {
        console.warn('Stream reading error, falling back to text:', streamError)
        // 如果流式读取失败，尝试读取完整响应
        const text = await response.text()
        if (text) {
          botMessage.text = text.replace(/^data: /gm, '').replace(/\n+/g, ' ').trim()
        }
      }
    } else {
      // 如果不支持流式读取，直接读取文本
      const text = await response.text()
      if (text) {
        botMessage.text = text.replace(/^data: /gm, '').replace(/\n+/g, ' ').trim()
      }
    }

    // 如果没有收到任何数据，抛出错误
    if (!botMessage.text.trim()) {
      throw new Error('No data received from API')
    }

  } catch (error) {
    console.error('Stream API error:', error)
    // 移除占位符消息
    messages.value.pop()
    throw error
  }
}

// 普通API调用
const callGenerateAPI = async (prompt) => {
  const API_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/ai/chatbot/generate'

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt.trim() }),
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()

    if (data.response) {
      addBotMessage(data.response)
      // 设置追问
      if (Array.isArray(data.follow_up_questions) && data.follow_up_questions.length) {
        followUps.value = data.follow_up_questions
      } else {
        followUps.value = []
      }
    } else {
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('Fallback API error:', error)
    throw error
  }
}

// 重试上次失败的消息
const retryLastMessage = () => {
  if (lastFailedMessage.value) {
    inputMessage.value = lastFailedMessage.value
    sendMessage()
  }
}

// 添加bot消息的辅助函数
const addBotMessage = (text) => {
  const botMessage = {
    type: 'bot',
    text: text,
    time: getCurrentTime()
  }
  messages.value.push(botMessage)
  isTyping.value = false

  nextTick(() => {
    scrollToBottom()
  })
}

// 选择追问
const chooseFollowUp = (q) => {
  inputMessage.value = q
  sendMessage()
}

// 添加错误消息
const addErrorMessage = (text) => {
  const errorMessage = {
    type: 'error',
    text: text,
    time: getCurrentTime()
  }
  messages.value.push(errorMessage)
  isTyping.value = false

  nextTick(() => {
    scrollToBottom()
  })
}

const getCurrentTime = () => {
  const now = new Date()
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 10000; /* top-most */
}

/* 聊天按钮 */
.chat-toggle {
  width: 60px;
  height: 60px;
  background: var(--violet-deep);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
  transition: all 0.3s ease;
  color: white;
}

.chat-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(139, 92, 246, 0.4);
}

/* 聊天窗口 */
.chat-window {
  width: 380px;
  height: 550px;
  background: white;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 聊天头部 */
.chat-header {
  background: var(--violet-deep);
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bot-avatar {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-text h3 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
}


.close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  max-width: 85%;
}

.bot-message {
  align-self: flex-start;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bot-message .message-avatar {
  background: var(--violet-sage);
  color: var(--violet-dark);
}

.user-message .message-avatar {
  background: var(--violet-dark);
  color: white;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  position: relative;
}

.bot-message .message-content {
  background: var(--bg-secondary);
  color: var(--violet-ultra-dark);
}

.user-message .message-content {
  background: var(--violet-dark);
  color: white;
  border: none;
}

.message-content p {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.message-content ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.message-content ul li {
  font-size: 0.85rem;
  margin: 0.25rem 0;
}

.error-text {
  color: #e53e3e !important;
  font-weight: 500;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: var(--violet-medium);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* 输入区域 */
.chat-input {
  padding: 1rem;
  border-top: 1px solid var(--border-light);
  background: white;
}

/* follow-ups */
.followups { padding: 0 1rem; }

.followup-title {
  font-size: 0.85rem;
  color: var(--violet-ultra-dark);
  opacity: 0.8;
  margin: 0 0 0.5rem 0;
}

.followup-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.chip {
  background: var(--violet-light);
  color: var(--violet-deep);
  border: 1px solid var(--violet-sage);
  padding: 0.35rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  cursor: pointer;
}

.chip:hover {
  background: #e9ddff;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-light);
  border-radius: 20px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.message-input:focus {
  border-color: var(--violet-medium);
}

.message-input:disabled {
  background: var(--bg-light);
  cursor: not-allowed;
}

.send-btn {
  width: 40px;
  height: 40px;
  background: var(--violet-dark);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  background: var(--violet-deep);
  transform: scale(1.05);
}

.send-btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
}

/* 重试按钮 */
.retry-container {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--violet-medium);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: var(--violet-dark);
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .chatbot-container {
    bottom: 10px;
    right: 10px;
  }

  .chat-window {
    width: calc(100vw - 20px);
    height: calc(100vh - 20px);
    max-height: 550px;
  }

  .chat-toggle {
    width: 50px;
    height: 50px;
  }
}
</style>
