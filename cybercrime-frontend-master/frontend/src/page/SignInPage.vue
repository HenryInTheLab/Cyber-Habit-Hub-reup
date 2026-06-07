<template>
  <div class="signin-container">
    <div class="signin-card">
      <div class="step-content">
        <h2 class="step-title">Sign In</h2>
        <p class="step-description">Enter your username and Google Authenticator verification code</p>

        <div class="signin-form">
          <div class="form-group">
            <input
              v-model="signinData.username"
              type="text"
              placeholder="Enter username"
              required
              :disabled="isLoading"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <input
              v-model="signinData.code"
              @input="handleCodeInput"
              type="text"
              placeholder="Enter 6-digit code"
              maxlength="6"
              required
              :disabled="isLoading"
              class="form-input"
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button
            @click="handleSignIn"
            class="btn-primary"
            :disabled="!isFormValid || isLoading"
          >
            <span v-if="isLoading">Signing In...</span>
            <span v-else>Sign In</span>
          </button>
        </div>

        <div class="signin-footer">
          <p class="signup-link">
            Don't have an account?
            <router-link to="/signup" class="link">Sign Up</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SignIn',
  setup() {
    const router = useRouter()

    // 响应式数据
    const signinData = ref({
      username: '',
      code: ''
    })

    const isLoading = ref(false)
    const errorMessage = ref('')

    // 计算属性
    const isFormValid = computed(() => {
      return signinData.value.username.trim() !== '' &&
             /^\d{6}$/.test(signinData.value.code)
    })

    // 方法
    const handleCodeInput = () => {
      // 只允许数字，最多6位
      signinData.value.code = signinData.value.code.replace(/\D/g, '').slice(0, 6)
      errorMessage.value = ''
    }

    const handleSignIn = async () => {
      if (!isFormValid.value) return

      isLoading.value = true
      errorMessage.value = ''

      try {
        const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/users/signin/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: signinData.value.username.trim(),
            code: signinData.value.code
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || '登录失败')
        }

        const result = await response.json()
        console.log('Sign in successful:', result)

        // 保存token到localStorage
        if (result.access_token) {
          localStorage.setItem('access_token', result.access_token)
        }
        if (result.refresh_token) {
          localStorage.setItem('refresh_token', result.refresh_token)
        }

        // 保存用户信息
        if (result.user) {
          localStorage.setItem('user_info', JSON.stringify(result.user))
        }

        // 登录成功，跳转到首页或用户中心
        router.push('/user-center')

      } catch (error) {
        console.error('Sign in failed:', error)
        errorMessage.value = error.message || '登录失败，请检查用户名和验证码'
      } finally {
        isLoading.value = false
      }
    }

    return {
      signinData,
      isLoading,
      errorMessage,
      isFormValid,
      handleCodeInput,
      handleSignIn
    }
  }
}
</script>

<style scoped>
.signin-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--violet-ultra-dark);
  padding: 20px;
}

.signin-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  max-width: 600px;
  width: 100%;
}

.step-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  text-align: center;
}

.step-description {
  color: #666;
  margin-bottom: 30px;
  text-align: center;
}

.signin-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid var(--violet-light);
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--violet-medium);
}

.form-input:disabled {
  background: var(--violet-light);
  cursor: not-allowed;
}


.btn-primary {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  background: var(--violet-dark);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--violet-deep);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: var(--violet-dark);
  background: var(--violet-light);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--violet-light);
  text-align: center;
}

.signin-footer {
  margin-top: 30px;
  text-align: center;
}

.signup-link {
  color: #666;
  font-size: 14px;
}

.link {
  color: var(--violet-dark);
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .signin-card {
    padding: 20px;
    margin: 10px;
  }

}
</style>
