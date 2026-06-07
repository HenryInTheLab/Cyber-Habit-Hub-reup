<template>
  <div class="test-page">
    <!-- 未认证时显示注册提示 -->
    <div v-if="!isAuthenticated" class="auth-required">
      <div class="auth-card">
        <h2>Sign Up Required</h2>
        <p>Please sign up to take the cybersecurity test</p>
        <button @click="redirectToSignUp" class="signup-btn">Sign Up</button>
      </div>
    </div>

    <!-- 认证后显示测试内容 -->
    <div v-else>
      <!-- Test Progress Indicator -->
      <div class="progress-section" v-if="currentStep > 0">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${(currentStep / totalQuestions) * 100}%` }"></div>
        </div>
        <p class="progress-text">Question {{ currentStep }} / {{ totalQuestions }}</p>
      </div>

    <!-- Test Content Area -->
    <div class="test-content">
      <!-- Welcome Page -->
              <div v-if="currentStep === 0" class="welcome-section">
          <div class="welcome-card">


          <!-- Loading State -->
          <div v-if="loading" class="loading-section">
            <div class="loading-spinner"></div>
            <p>Loading...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="error-section">
            <div class="error-icon">⚠️</div>
            <p class="error-message">{{ error }}</p>
            <button @click="startTest" class="retry-btn">Retry</button>
          </div>

          <!-- Category Selection -->
          <div class="category-selection">
            <h3>Choose Test Category</h3>
            <div class="category-options">
              <div
                v-for="category in availableCategories"
                :key="category.value"
                class="category-option"
                :class="{ 'selected': selectedCategory === category.value }"
                @click="selectCategory(category.value)"
              >
                <div class="category-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                    <path :d="category.icon" />
                  </svg>
                </div>
                <div class="category-info">
                  <h4>{{ category.label }}</h4>
                  <p>{{ category.description }}</p>
                  <span class="question-count">{{ category.questionCount }} questions</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Test Info -->
          <div v-if="selectedCategory" class="test-info">
            <div class="info-item">
              <span class="info-label">Selected Category:</span>
              <span class="info-value">{{ getCategoryLabel(selectedCategory) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Test Duration:</span>
              <span class="info-value">About {{ Math.ceil(totalQuestions / 2) }}-{{ Math.ceil(totalQuestions / 1.5) }} minutes</span>
            </div>
            <div class="info-item">
              <span class="info-label">Number of Questions:</span>
              <span class="info-value">{{ totalQuestions }} questions</span>
            </div>
            <div class="info-item">
              <span class="info-label">Test Type:</span>
              <span class="info-value">Multiple Choice</span>
            </div>
          </div>

          <button
            @click="startTest"
            class="start-btn"
            :disabled="loading || !selectedCategory"
          >
            {{ loading ? 'Loading...' : !selectedCategory ? 'Please Select a Category' : 'Start Test' }}
          </button>
        </div>
      </div>

      <!-- Question Page -->
      <div v-else-if="currentStep <= totalQuestions" class="question-section">
        <div class="question-header">
          <h3 class="question-title">{{ currentQuestion.title }}</h3>
          <p class="question-description" v-if="currentQuestion.description">
            {{ currentQuestion.description }}
          </p>
        </div>

        <div class="options-container">
          <div
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            class="option-item"
            :class="{ 'selected': selectedAnswer === index }"
            @click="selectAnswer(index)"
          >
            <div class="option-radio">
              <div class="radio-circle" :class="{ 'checked': selectedAnswer === index }"></div>
            </div>
            <div class="option-text">
              <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span>
              <span class="option-content">{{ option.text }}</span>
            </div>
          </div>
        </div>

        <div class="question-actions">
          <button
            v-if="currentStep > 1"
            @click="previousQuestion"
            class="nav-btn prev-btn"
          >
            Previous
          </button>
          <button
            @click="nextQuestion"
            class="nav-btn next-btn"
            :disabled="selectedAnswer === null"
          >
            {{ currentStep === totalQuestions ? 'Complete Test' : 'Next' }}
          </button>
        </div>
      </div>

      <!-- Results Page -->
      <div v-else class="results-section">
        <div class="results-header">
          <div class="results-icon">🎉</div>
          <h2>Test Completed!</h2>
          <p>Congratulations on completing the cybersecurity knowledge test</p>
        </div>

          <div class="score-section">
            <div class="overall-score">
              <p class="score-label">Overall Score</p>
              <div class="score-circle">
                <span class="score-number">{{ Math.round((correctAnswers / totalQuestions) * 100) }}</span>
                <span class="score-percent">%</span>
              </div>

            </div>

            <!-- 简化版分数显示，移除复杂的类别分数分析 -->
          </div>

                      <div class="feedback-section">
              <div class="feedback-content">
              <p>Based on your test results, we recommend focusing on the following areas:</p>
              <ul class="feedback-list">
                <li>Improve your ability to identify phishing emails</li>
                <li>Strengthen your social media privacy settings</li>
                <li>Regularly update passwords and use strong passwords</li>
              </ul>
            </div>
          </div>

          <div class="results-actions">
            <button @click="retakeTest" class="action-btn retake-btn">Retake Test</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'TestSection',
  emits: ['test-status-changed'],
  setup(props, { emit }) {
    const router = useRouter()

    // Authentication state
    const isAuthenticated = ref(false)
    const currentUser = ref(null)

    // Check user authentication status
    const checkAuthStatus = () => {
      try {
        const accessToken = localStorage.getItem('access_token')
        const userInfoStr = localStorage.getItem('user_info')

        if (accessToken && userInfoStr) {
          isAuthenticated.value = true
          currentUser.value = JSON.parse(userInfoStr)
          console.log('User authenticated:', currentUser.value)
        } else {
          isAuthenticated.value = false
          currentUser.value = null
          console.log('User not authenticated: No token found')
        }
      } catch (error) {
        isAuthenticated.value = false
        currentUser.value = null
        console.log('User not authenticated:', error)
      }
    }

    // Redirect to sign up function
    const redirectToSignUp = () => {
      router.push('/signup')
    }

    // 状态变量
    const currentAttemptId = ref(null)
    const questions = ref([])
    const currentStep = ref(0)
    const selectedAnswer = ref(null)
    const correctAnswers = ref(0)
    const totalQuestions = ref(20)
    const loading = ref(false)
    const error = ref(null)
    const selectedCategory = ref('')

    // 存储用户所有答案
    const userAnswers = ref({})

    // Available categories
    const availableCategories = ref([
      {
        value: 'Cyber Harassment',
        label: 'Cyber Harassment',
        description: 'Test your knowledge about identifying and handling cyber harassment',
        icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
        questionCount: 20
      },
      {
        value: 'Cyber Scam',
        label: 'Cyber Scam',
        description: 'Learn to identify and avoid various cyber scams and fraudulent activities',
        icon: 'M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z',
        questionCount: 20
      },
      {
        value: 'Privacy Protection',
        label: 'Privacy Protection',
        description: 'Learn about protecting personal information and data privacy',
        icon: 'M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6z',
        questionCount: 20
      },
      {
        value: 'mixed',
        label: 'Mixed Categories',
        description: 'Comprehensive test covering all cybersecurity areas',
        icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        questionCount: 20
      }
    ])

    // API configuration
    const API_BASE_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com'

    // 获取Access Token
    const getAccessToken = () => {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          throw new Error('No access token found')
        }
        return token
      } catch (error) {
        console.error('Error getting access token:', error)
        throw error
      }
    }

    // 1. 开始测试 - 调用POST /quizzes/attempt/
    const startTest = async () => {
      if (!selectedCategory.value) return

      try {
        loading.value = true
        error.value = null

        // 构建查询参数
        const params = new URLSearchParams()

        // 根据选择的类别设置参数
        if (selectedCategory.value === 'mixed') {
          // 混合类别不设置 category 参数（或设置为 null）
          params.append('count', totalQuestions.value.toString())
        } else {
          // 特定类别
          params.append('category', selectedCategory.value)
          params.append('count', totalQuestions.value.toString())
        }

        // 使用查询参数而不是请求体
        const response = await fetch(`${API_BASE_URL}/quizzes/attempt/?${params.toString()}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
          }
          // 移除 body，因为参数现在在 URL 中
        })

        if (!response.ok) {
          throw new Error(`Failed to start test: ${response.status}`)
        }

        const data = await response.json()

        // 保存attempt ID和题目
        currentAttemptId.value = data.attempt_id
        questions.value = data.questions || []
        totalQuestions.value = questions.value.length

        if (questions.value.length > 0) {
          currentStep.value = 1
          selectedAnswer.value = null
          correctAnswers.value = 0
          userAnswers.value = {} // 重置用户答案
          // 发射测试开始事件
          emit('test-status-changed', true)
        } else {
          throw new Error('No questions received')
        }

      } catch (err) {
        console.error('Error starting test:', err)
        error.value = `Failed to start test: ${err.message}`
      } finally {
        loading.value = false
      }
    }

    // 2. 下一题逻辑 - 最后一题时完成测试
    const nextQuestion = async () => {
      if (selectedAnswer.value === null || !currentQuestion.value) return

      // 检查答案是否正确 - 比较选中的选项identifier与正确答案
      const selectedOption = currentQuestion.value.options[selectedAnswer.value]
      const correctOption = currentQuestion.value.options.find(opt => opt.is_answer === true)
      const isCorrect = selectedOption && correctOption && selectedOption.identifier === correctOption.identifier

      if (isCorrect) {
        correctAnswers.value++
      }

      // 如果是最后一题，直接完成测试
      if (currentStep.value === totalQuestions.value) {
        await finishTest()
      } else {
        // 继续下一题
        currentStep.value++
        selectedAnswer.value = null
      }
    }

    // 3. 完成测试 - 调用PATCH /quizzes/attempt/{id} with is_final: true
    const finishTest = async () => {
      if (!currentAttemptId.value) return

      try {
        loading.value = true

                // 收集所有用户答案
        const allAnswers = []

        // 遍历所有题目，收集用户的答案
        for (let i = 0; i < questions.value.length; i++) {
          const question = questions.value[i]
          let userAnswer = null
          let isCorrect = false

          if (i < currentStep.value - 1) {
            // 已答题目
            userAnswer = getUserAnswerForQuestion(question.id)
            // 找到正确答案的identifier
            const correctOption = question.options.find(opt => opt.is_answer === true)
            isCorrect = userAnswer !== null && correctOption && userAnswer === correctOption.identifier
          } else if (i === currentStep.value - 1) {
            // 当前题目 - 获取选项的identifier而不是索引
            if (selectedAnswer.value !== null && question.options[selectedAnswer.value]) {
              userAnswer = question.options[selectedAnswer.value].identifier
            }
            // 找到正确答案的identifier
            const correctOption = question.options.find(opt => opt.is_answer === true)
            isCorrect = userAnswer !== null && correctOption && userAnswer === correctOption.identifier
          }

          if (userAnswer !== null) {
            allAnswers.push({
              question_id: question.id,
              chosen_answer: userAnswer,
              is_correct: isCorrect
            })
          }
        }

        const response = await fetch(`${API_BASE_URL}/quizzes/attempt/${currentAttemptId.value}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
          },
          body: JSON.stringify({
            is_final: true,
            quiz_question_attempts: allAnswers
          })
        })

        if (!response.ok) {
          throw new Error(`Failed to finish test: ${response.status}`)
        }

        // 显示结果页面
        currentStep.value = totalQuestions.value + 1

      } catch (err) {
        console.error('Error finishing test:', err)
        // 即使提交失败，也显示结果页面
        currentStep.value = totalQuestions.value + 1
      } finally {
        loading.value = false
      }
    }

    // 4. 存储用户答案（用于最终提交）
    const selectAnswer = (index) => {
      selectedAnswer.value = index
      // 保存用户答案 - 存储选项的identifier
      if (currentQuestion.value && currentQuestion.value.options[index]) {
        userAnswers.value[currentQuestion.value.id] = currentQuestion.value.options[index].identifier
      }
    }

    const getUserAnswerForQuestion = (questionId) => {
      return userAnswers.value[questionId] || null
    }

    // 5. 计算属性
    const currentQuestion = computed(() => {
      if (currentStep.value > 0 && currentStep.value <= totalQuestions.value) {
        const question = questions.value[currentStep.value - 1]
        if (question) {
          // 处理API返回的选项格式，找到正确答案的索引
          const correctIndex = question.options.findIndex(option => option.is_answer === true)
          return {
            ...question,
            title: question.question_text,
            correct: correctIndex >= 0 ? correctIndex : 0
          }
        }
      }
      return null
    })

    // 6. 重置函数
    const resetTest = () => {
      currentAttemptId.value = null
      questions.value = []
      currentStep.value = 0
      selectedAnswer.value = null
      correctAnswers.value = 0
      userAnswers.value = {}
      error.value = null
    }

    const retakeTest = () => {
      resetTest()
      // 发射测试结束事件，重新显示FooterSection
      emit('test-status-changed', false)
    }

    const selectCategory = (category) => {
      selectedCategory.value = category
      resetTest()
    }

    // Get category label
    const getCategoryLabel = (categoryValue) => {
      const category = availableCategories.value.find(cat => cat.value === categoryValue)
      return category ? category.label : ''
    }

    const previousQuestion = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        selectedAnswer.value = null
      }
    }

    // Check authentication on mount
    onMounted(() => {
      checkAuthStatus()
    })

    return {
      // Authentication
      isAuthenticated,
      currentUser,
      checkAuthStatus,
      redirectToSignUp,

      // 状态
      currentStep,
      selectedAnswer,
      correctAnswers,
      totalQuestions,
      currentQuestion,
      questions,
      loading,
      error,
      selectedCategory,
      availableCategories,

      // 方法
      startTest,
      selectAnswer,
      nextQuestion,
      previousQuestion,
      retakeTest,
      selectCategory,
      getCategoryLabel
    }
  }
}
</script>

<style scoped>
.test-page {
  min-height: vh;
  background: var(--violet-light);
  padding: 0;
}

.progress-section {
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: var(--violet-ultra-dark);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  color: var(--violet-ultra-dark);
  font-weight: 500;
  margin: 0;
}

.test-content {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
}

.welcome-card {
  max-width: 1600px;
  margin: 0 auto;
  padding: 40px;
}

.category-selection {
  margin-bottom: 30px;
}

.category-selection h3 {
  color: var(--violet-ultra-dark);
  margin-bottom: 20px;
  font-size: 1.4rem;
  text-align: center;
}

.category-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.category-option {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 2px solid var(--violet-sage);
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.category-option.selected {
  border-color: var(--violet-dark);
  background: var(--violet-light);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.category-icon {
  width: 60px;
  height: 60px;
  margin-right: 15px;
  min-width: 60px;
  background: var(--violet-dark);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.category-info h4 {
  color: var(--violet-ultra-dark);
  margin: 0 0 5px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.category-info p {
  color: var(--violet-deep);
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.question-count {
  color: var(--violet-dark);
  font-size: 0.85rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.8);
  padding: 4px 8px;
  border-radius: 12px;
}



.test-info {
  background: var(--violet-light);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  color: var(--violet-deep);
  font-weight: 500;
}

.info-value {
  color: var(--violet-ultra-dark);
  font-weight: 600;
}

.start-btn {
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px var(--shadow-medium);
}

.start-btn:hover {
  background: var(--violet-dark);
}

.start-btn:disabled {
  background: var(--violet-sage);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-section {
  text-align: center;
  margin: 20px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--violet-sage);
  border-top: 4px solid var(--violet-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-section p {
  color: var(--violet-deep);
  margin: 0;
}

.error-section {
  text-align: center;
  margin: 20px 0;
  padding: 20px;
  background: var(--violet-light);
  border-radius: 12px;
  border: 1px solid var(--violet-sage);
}

.error-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.error-message {
  color: var(--violet-deep);
  margin: 0 0 15px 0;
  font-weight: 500;
}

.retry-btn {
  background: var(--violet-deep);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: var(--violet-dark);
}

.question-section {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 60px;
}



.question-header {
  margin-bottom: 30px;
}

.question-title {
  color: var(--violet-ultra-dark);
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.question-description {
  color: var(--violet-deep);
  margin: 0;
  font-size: 0.95rem;
}

.options-container {
  margin-bottom: 30px;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border: 2px solid var(--violet-sage);
  border-radius: 12px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

.option-item:hover {
  border-color: var(--violet-dark);
  background: var(--violet-light);
}

.option-item.selected {
  border-color: var(--violet-ultra-dark);
  background: var(--violet-light);
}

.option-radio {
  margin-right: 15px;
}

.radio-circle {
  width: 20px;
  height: 20px;
  border: 2px solid var(--violet-sage);
  border-radius: 50%;
  position: relative;
  transition: all 0.3s ease;
}

.radio-circle.checked {
  border-color: var(--violet-ultra-dark);
  background: var(--violet-ultra-dark);
}

.radio-circle.checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.option-text {
  display: flex;
  align-items: flex-start;
  flex: 1;
}

.option-label {
  color: var(--violet-dark);
  font-weight: 600;
  margin-right: 10px;
  min-width: 20px;
}

.option-content {
  color: var(--violet-ultra-dark);
  line-height: 1.5;
}

.question-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.prev-btn {
  background: var(--violet-light);
  color: var(--violet-deep);
  border: 2px solid var(--violet-sage);
}

.prev-btn:hover {
  background: var(--violet-sage);
  border-color: var(--violet-dark);
}

.next-btn {
  background: var(--violet-ultra-dark);
  color: white;
}

.next-btn:hover:not(:disabled) {
  background: var(--violet-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px var(--shadow-medium);
}

.next-btn:disabled {
  background: var(--violet-sage);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.results-section {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 60px;
}



.results-header {
  text-align: center;
  margin-bottom: 40px;
}

.results-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.results-header h2 {
  color: var(--violet-ultra-dark);
  margin-bottom: 10px;
  font-size: 2rem;
}

.results-header p {
  color: var(--violet-deep);
  font-size: 1.1rem;
}

.score-section {
  margin-bottom: 30px;
}

.overall-score {
  text-align: center;
  margin-bottom: 30px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--violet-dark) 0%, var(--violet-ultra-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  position: relative;
  box-shadow: 0 8px 25px var(--shadow-medium);
}

.score-number {
  font-size: 3rem;
  font-weight: 700;
  margin-right: 8px;
}

.score-percent {
  font-size: 1.5rem;
  font-weight: 600;
}

.score-label {
  color: var(--violet-ultra-dark);
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
  text-align: center;
}

/* 移除复杂的类别分数分析样式 */

.feedback-content {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 25px;
  border-left: 4px solid var(--violet-dark);
  box-shadow: 0 4px 15px var(--shadow-light);
  backdrop-filter: blur(10px);
  margin-bottom: 30px;
}

.feedback-content p {
  color: var(--violet-ultra-dark);
  margin: 0 0 20px 0;
  font-weight: 500;
  font-size: 1.5rem;
  line-height: 1.6;
}

.feedback-list {
  color: var(--violet-deep);
  margin: 0;
  padding-left: 0;
  list-style: none;
}

.feedback-list li {
  margin-bottom: 12px;
  line-height: 1.6;
  position: relative;
  padding-left: 25px;
  font-size: 1.2rem;
}

.feedback-list li::before {
  content: '✓';
  color: var(--violet-dark);
  font-weight: bold;
  font-size: 1rem;
  position: absolute;
  left: 0;
  top: 0;
}

.results-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.action-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retake-btn {
  background: var(--violet-ultra-dark);
  color: white;
}

.retake-btn:hover {
  background: var(--violet-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-medium);
}



@media (max-width: 768px) {
  .test-page {
    padding: 10px;
  }

  .test-content {
    padding: 20px;
  }

  .welcome-card {
    padding: 20px;
  }

  .category-options {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .category-option {
    padding: 15px;
  }

  .category-icon {
    width: 50px;
    height: 50px;
    margin-right: 10px;
    min-width: 50px;
  }

  .question-card {
    padding: 20px;
  }

  .option-item {
    padding: 12px 15px;
  }

  .results-actions {
    flex-direction: column;
  }

  .score-circle {
    width: 120px;
    height: 120px;
  }

  .score-number {
    font-size: 2.5rem;
    margin-right: 6px;
  }

  .score-percent {
    font-size: 1.2rem;
  }
}

.auth-required {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.auth-card {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.signup-btn {
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.signup-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-dark);
}
</style>

