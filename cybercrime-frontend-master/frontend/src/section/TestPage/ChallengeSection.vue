<template>
  <div class="challenge-page">
    <!-- 未认证时显示注册提示 -->
    <div v-if="!isAuthenticated" class="auth-required">
      <div class="auth-card">
        <h2>Sign In Required</h2>
        <p>Please sign in to access the cybersecurity challenges</p>
        <button @click="redirectToSignUp" class="signup-btn">Sign In</button>
      </div>
    </div>

    <!-- 认证后显示挑战内容 -->
    <div v-else>
      <!-- Module Selection Page -->
      <div v-if="!selectedModule" class="challenge-content">
        <!-- Loading State for Task Data -->
        <div v-if="taskDataLoading" class="loading-section">
          <div class="loading-spinner"></div>
          <p>Loading challenge data...</p>
        </div>

        <!-- Error State for Task Data -->
        <div v-else-if="taskDataError" class="error-section">
          <div class="error-icon">⚠️</div>
          <p class="error-message">{{ taskDataError }}</p>
          <button @click="fetchTaskData" class="retry-btn">Retry</button>
        </div>

        <!-- Challenge Levels Page -->
        <div v-else class="challenge-levels">
          <!-- Progress Indicator -->
          <div class="progress-indicator">
            <div class="progress-steps">
              <div
                v-for="step in 3"
                :key="step"
                class="progress-step"
                :class="{
                  'active': step === currentLevel,
                  'completed': isLevelCompleted(step),
                  'locked': !isLevelUnlocked(step)
                }"
                @click="switchLevel(step)"
              >
                <div class="step-number">
                  <svg v-if="isLevelCompleted(step)" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                  <span v-else>{{ step }}</span>
                </div>
                <div class="step-line" v-if="step < 3"></div>
              </div>
            </div>
            <ScoringRulesButton />
          </div>

          <!-- Level Header -->
          <div class="level-header">
            <h1 class="level-title">Level {{ currentLevel }}: {{ getTaskTitle(currentLevel) }}</h1>
            <p class="level-description">{{ getTaskDescription(currentLevel) }}</p>
            <div class="module-progress">
              <span class="progress-text">{{ getCompletedModuleCount(currentLevel) }}/{{ getTaskModules(currentLevel).length }} modules completed</span>
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: `${(getCompletedModuleCount(currentLevel) / getTaskModules(currentLevel).length) * 100}%` }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Module Cards -->
          <div class="module-cards">
            <div
              v-for="module in getTaskModules(currentLevel)"
              :key="module.id"
              class="module-card"
              :class="{ 'completed': isModuleCompleted(module.name) }"
            >
              <div v-if="isModuleCompleted(module.name)" class="completion-badge">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                <span>Completed ({{ getModuleScore(module.name) }}%)</span>
              </div>

              <div class="module-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                  <path :d="module.icon" />
                </svg>
              </div>
              <div class="module-info">
                <h3 class="module-title">{{ module.name }}</h3>
                <p class="module-description">{{ module.description }}</p>
              </div>
              <button
                v-if="isLevelUnlocked(currentLevel)"
                class="start-module-btn"
                @click="() => selectModule(module)"
              >
                {{ isModuleCompleted(module.name) ? 'Retake →' : 'Start Learning →' }}
              </button>
              <div v-else class="locked-module">
                Complete previous level to unlock
              </div>
            </div>
          </div>
            </div>

      </div>

      <!-- Module Test Page -->
      <div v-if="selectedModule" class="module-test">

        <!-- Back Button -->
        <div class="test-header">
          <button @click="goBackToModules" class="back-to-modules-btn">Back</button>
        </div>

        <!-- Progress Indicator -->
        <div class="progress-section" v-if="currentStep > 0 && currentStep <= testQuestions.length">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${(currentStep / testQuestions.length) * 100}%` }"></div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <p>Loading questions...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-section">
          <div class="error-icon">⚠️</div>
          <p class="error-message">{{ error }}</p>
          <button @click="startModuleTest" class="retry-btn">Retry</button>
        </div>

        <!-- Question Page -->
        <div v-else-if="currentStep > 0 && currentStep <= testQuestions.length" class="question-section">
            <div class="question-header">
              <h3 class="question-title">{{ currentQuestion.question_text }}</h3>
            <p class="question-description" v-if="currentQuestion.description">
              {{ currentQuestion.description }}
            </p>
            </div>

            <div class="options-container">
              <div
                v-for="(option, index) in currentQuestionOptions"
                :key="index"
                class="option-item"
                :class="{ 'selected': selectedAnswer === index }"
                @click="selectAnswer(index)"
              >
                <div class="option-radio">
                  <div class="radio-circle" :class="{ 'checked': selectedAnswer === index }"></div>
                </div>
                <div class="option-text">
                <span class="option-label">{{ option.identifier }}.</span>
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
                {{ currentStep === testQuestions.length ? 'Complete Test' : 'Next' }}
              </button>
          </div>
        </div>

        <!-- Results Page -->
        <div v-else-if="currentStep > testQuestions.length" class="results-section">
            <div class="results-header">
              <h2>Test Completed!</h2>
            </div>

            <!-- Combined Score and Feedback Container -->
            <div class="results-container">
              <div class="score-section">
                <div class="overall-score">
                  <p class="score-label">Your Score</p>
                  <div class="score-circle">
                    <span class="score-number">{{ Math.round((correctAnswers / testQuestions.length) * 100) }}</span>
                    <span class="score-percent">%</span>
                  </div>
                  <p class="score-detail">{{ correctAnswers }} out of {{ testQuestions.length }} correct</p>
                </div>
              </div>

              <!-- Stats Update Messages -->
              <div v-if="testResult && testResult.stats_update && testResult.stats_update.messages && testResult.stats_update.messages.length > 0" class="messages-content">
                <div v-for="(message, index) in testResult.stats_update.messages" :key="index">
                  {{ message }}
                </div>
              </div>

              <!-- Test Details Section -->
              <div v-if="currentTestResult" class="test-details-section">
                <div class="test-details-header">
                  <h3 class="test-details-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="test-details-icon">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Test Details
                    <button @click="viewHistoryDetails(currentTestResult)" class="view-details-btn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15 12L9 12M12 9L12 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      View Details
                    </button>
                  </h3>
                </div>

              </div>

              <!-- AI Feedback Section -->
              <div v-if="testResult && testResult.feedback" class="feedback-section">
                <div class="feedback-header">
                  <h3 class="feedback-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="feedback-icon">
                      <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
                    </svg>
                    Feedback (AI Generated)
                  </h3>
                </div>

                <div class="feedback-content">
                  <div class="feedback-summary">
                    <h4 class="feedback-subtitle">Summary</h4>
                    <p class="feedback-text">{{ testResult.feedback.summary }}</p>
                  </div>

                  <div v-if="testResult.feedback.action_items && testResult.feedback.action_items.length > 0" class="feedback-actions">
                    <h4 class="feedback-subtitle">Action Items</h4>
                    <ul class="action-items-list">
                      <li v-for="(item, index) in testResult.feedback.action_items" :key="index" class="action-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="action-icon">
                          <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        {{ item }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>


            <div class="results-actions">
              <button @click="retakeTest" class="retake-btn">Retake Test</button>
              <button @click="goBackToModules" class="results-back-btn">Back to Modules</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Test History Details Modal -->
    <div v-if="selectedHistoryAttempt" class="modal-overlay" @click="closeHistoryModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Test Details</h3>
          <button @click="closeHistoryModal" class="close-btn">&times;</button>
        </div>

        <div class="modal-body">
          <div class="test-summary">
            <div class="summary-row">
              <span>Category:</span>
              <span>{{ getCategoryDisplayName(selectedHistoryAttempt.category, selectedHistoryAttempt) }}</span>
            </div>
            <div class="summary-row">
              <span>Score:</span>
              <span>{{ getFormattedScore(selectedHistoryAttempt.accuracy_pct) }}%</span>
            </div>
            <div class="summary-row">
              <span>Correct Answers:</span>
              <span>{{ selectedHistoryAttempt.correct_count }}/{{ selectedHistoryAttempt.total_questions }}</span>
            </div>
            <div class="summary-row">
              <span>Date:</span>
              <span>{{ formatDate(selectedHistoryAttempt.finished_at) }}</span>
            </div>
            <div class="summary-row">
              <span>Duration:</span>
              <span>{{ calculateDuration(selectedHistoryAttempt.started_at, selectedHistoryAttempt.finished_at) }}</span>
            </div>
          </div>

          <!-- Question Details -->
          <div v-if="selectedHistoryAttempt.quiz_question_attempts" class="questions-detail">
            <h4>Question Details</h4>
            <div
              v-for="(qa, index) in selectedHistoryAttempt.quiz_question_attempts"
              :key="index"
              class="question-item"
            >
              <div v-if="qa.question" class="question-content">
                <div class="question-header">
                  <div class="question-number">Q{{ index + 1 }}</div>
                  <div class="question-status" :class="qa.is_correct ? 'correct' : 'incorrect'">
                    {{ qa.is_correct ? '✓ Correct' : '✗ Incorrect' }}
                  </div>
                </div>

                <div class="question-text">
                  {{ qa.question.question_text }}
                </div>

                <div class="options-list">
                  <div
                    v-for="(option, optIndex) in qa.question.options"
                    :key="optIndex"
                    class="option-item"
                    :class="{
                      'correct': option.is_answer,
                      'selected': qa.chosen_answer === option.identifier,
                      'wrong-selected': qa.chosen_answer === option.identifier && !option.is_answer
                    }"
                  >
                    <span class="option-identifier">{{ option.identifier }}.</span>
                    <span class="option-text">{{ option.text }}</span>
                    <span v-if="option.is_answer" class="correct-indicator">✓ Correct Answer</span>
                    <span v-if="qa.chosen_answer === option.identifier && !option.is_answer" class="wrong-indicator">✗ Your Answer</span>
                  </div>
                </div>

                <!-- Explanation if available -->
                <div v-if="qa.question.explanation" class="question-explanation">
                  <h5>Explanation:</h5>
                  <p>{{ qa.question.explanation }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div v-if="showToast" class="level-toast">
      <div class="toast-content">
        <div class="toast-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
          </svg>
        </div>
        <div class="toast-message">{{ toastMessage }}</div>
        <button @click="showToast = false" class="toast-close">&times;</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import ScoringRulesButton from '@/components/ScoringRulesButton.vue'

export default {
  name: 'ChallengeSection',
  components: {
    ScoringRulesButton
  },
  emits: ['challenge-status-changed'],
  setup(props, { emit }) {
    const router = useRouter()

    // Authentication state
    const isAuthenticated = ref(false)
    const currentUser = ref(null)

    // Challenge state
    const currentLevel = ref(1) // 当前显示的level
    const selectedModule = ref(null)

    // Test state
    const testQuestions = ref([])
    const currentStep = ref(0) //
    const selectedAnswer = ref(null)
    const correctAnswers = ref(0)
    const userAnswers = ref([]) // 保持原有的数组格式用于API提交
    const savedAnswers = ref({}) // 新增：用于记住用户选择的对象格式

    // API configuration
    const API_BASE_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com'

    // Quiz attempt state
    const currentAttemptId = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const testResult = ref(null)

    // Test history state
    const currentTestResult = ref(null)
    const historyLoading = ref(false)
    const selectedHistoryAttempt = ref(null)

    // Check user authentication status
    const checkAuthStatus = async () => {
      try {
        const accessToken = localStorage.getItem('access_token')
        const userInfoStr = localStorage.getItem('user_info')

        if (accessToken && userInfoStr) {
          isAuthenticated.value = true
          currentUser.value = JSON.parse(userInfoStr)

          // 获取用户的challenge_level
          await fetchUserStats()

        } else {
          isAuthenticated.value = false
          currentUser.value = null
        }
      } catch {
        isAuthenticated.value = false
        currentUser.value = null
      }
    }

    // 获取用户统计信息（包括challenge_level）
    const fetchUserStats = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/stats/`, {
          headers: {
            'Authorization': `Bearer ${getAccessToken()}`
          }
        })

        if (response.ok) {
          const stats = await response.json()
          // 更新用户的challenge_level
          if (currentUser.value) {
            currentUser.value.challenge_level = stats.challenge_level
          }
        }
      } catch (error) {
        console.error('Error fetching user stats:', error)
      }
    }

    // Redirect to sign up function
    const redirectToSignUp = () => {
      router.push('/signin')
    }

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


    // Task data - 通过API获取模块名称，硬编码其他信息
    const taskData = ref({})
    const taskDataLoading = ref(false)
    const taskDataError = ref(null)

    // 硬编码的模块信息映射
    const moduleInfoMapping = {
      'Cyber Harassment Basic Recognition': {
            description: 'Learn to identify and respond to cyberbullying behavior',
        icon: 'M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z',
          },
      'Common Scam Identification': {
            description: 'Master basic techniques for identifying scams',
        icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
          },
      'Personal Privacy Protection Basics': {
            description: 'Learn basic methods for protecting personal information',
        icon: 'M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z',
      },
      'Deep Threat Understanding': {
            description: 'Understand the underlying principles of network threats',
        icon: 'M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'
          },
      'Scam Technique Analysis': {
            description: 'Analyze the operational mechanisms of complex scams',
        icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z',
          },
      'Technical Protection Application': {
            description: 'Learn to use technical tools for protection',
        icon: 'M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.56-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z',
      },
      'Regulatory Policy Understanding': {
            description: 'Understand relevant legal and regulatory requirements',
        icon: 'M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z',
          },
      'Organizational Security Management': {
            description: 'Learn enterprise-level security strategy development',
        icon: 'M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10z',
      }
    }

    // 获取单个级别的模块数据
    const fetchLevelModules = async (level) => {
      const response = await fetch(`${API_BASE_URL}/quizzes/modules/?challenge_level=${level}`, {
        headers: {
          'Authorization': `Bearer ${getAccessToken()}`
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch level ${level} modules: ${response.status}`)
      }

      return response.json()
    }

    // 构建级别数据
    const buildLevelData = (level, modules, startId) => {
      const levelConfig = {
        1: {
          title: 'Network Newbie Protection',
          description: 'Learn basic security protection knowledge as you start exploring the online world.'
        },
        2: {
          title: 'Security Awareness Enhancement',
          description: 'Face more complex network threat scenarios as you develop deeper security awareness.'
        },
        3: {
          title: 'Security Expert Advancement',
          description: 'Master professional-level security management and compliance knowledge.'
        }
      }

      return {
        ...levelConfig[level],
        modules: modules.map((moduleName, index) => ({
          id: startId + index,
          name: moduleName,
          challenge_level: level,
          ...moduleInfoMapping[moduleName]
        }))
      }
    }

    // 获取任务数据
    const fetchTaskData = async () => {
      try {
        taskDataLoading.value = true
        taskDataError.value = null

        // 获取三个挑战级别的模块数据
        const [level1Modules, level2Modules, level3Modules] = await Promise.all([
          fetchLevelModules(1),
          fetchLevelModules(2),
          fetchLevelModules(3)
        ])

        // 构建任务数据
        taskData.value = {
          1: buildLevelData(1, level1Modules, 1),
          2: buildLevelData(2, level2Modules, 4),
          3: buildLevelData(3, level3Modules, 7)
        }

      } catch (err) {
        console.error('Error fetching task data:', err)
        taskDataError.value = err.message
        // 如果API失败，使用默认数据作为fallback
        taskData.value = {
          1: buildLevelData(1, [
            'Cyber Harassment Basic Recognition',
            'Common Scam Identification',
            'Personal Privacy Protection Basics'
          ], 1)
        }
      } finally {
        taskDataLoading.value = false
      }
    }

    // Methods

    // 切换level显示
    // Toast state
    const showToast = ref(false)
    const toastMessage = ref('')

    const showToastMessage = (message) => {
      toastMessage.value = message
      showToast.value = true
      setTimeout(() => {
        showToast.value = false
      }, 3000)
    }

    const switchLevel = (level) => {
      if (isLevelUnlocked(level)) {
        currentLevel.value = level
        selectedModule.value = null
      } else {
        // Show toast for locked level
        if (level === 3) {
          showToastMessage('Please complete Level 2 first to unlock Level 3')
        } else if (level === 2) {
          showToastMessage('Please complete Level 1 first to unlock Level 2')
        }
      }
    }

    const selectModule = (module) => {
      selectedModule.value = module
      startModuleTest()
    }


    // Start module test - 使用新的API
    const startModuleTest = async () => {
      if (!selectedModule.value) return

      try {
        loading.value = true
        error.value = null

        // 构建查询参数 - 直接使用模块数据
        const challengeLevel = selectedModule.value.challenge_level
        const moduleName = selectedModule.value.name


        const params = new URLSearchParams()
        params.append('challenge_level', challengeLevel.toString())
        params.append('module_name', moduleName)
        params.append('count', '5') // 固定5道题

        const apiUrl = `${API_BASE_URL}/quizzes/attempt/?${params.toString()}`
        console.log('API URL:', apiUrl)
        console.log('Request params:', {
          challenge_level: challengeLevel.toString(),
          module_name: moduleName,
          count: '5'
        })

        // 调用API开始测试
        const response = await fetch(`${API_BASE_URL}/quizzes/attempt/?${params.toString()}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to start test: ${response.status}`)
        }

        const data = await response.json()

        // 保存attempt ID和题目
        currentAttemptId.value = data.attempt_id
        testQuestions.value = data.questions || []

        if (testQuestions.value.length > 0) {
      currentStep.value = 1
      selectedAnswer.value = null
      correctAnswers.value = 0
      userAnswers.value = []
      savedAnswers.value = {}
          // 发射挑战开始事件
          emit('challenge-status-changed', true)
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

    // Get current question
    const currentQuestion = computed(() => {
      if (currentStep.value > 0 && currentStep.value <= testQuestions.value.length) {
        return testQuestions.value[currentStep.value - 1]
      }
      return null
    })

    // Get current question options - 使用API格式
    const currentQuestionOptions = computed(() => {
      if (!currentQuestion.value) return []

      // API返回的格式: options数组，每个选项有identifier, text, is_answer
      return currentQuestion.value.options || []
    })

    // Select answer
    const selectAnswer = (index) => {
      selectedAnswer.value = index
      // 保存用户答案到savedAnswers中
      if (currentQuestion.value && currentQuestion.value.options[index]) {
        savedAnswers.value[currentQuestion.value.id] = currentQuestion.value.options[index].identifier
      }
    }

    // 获取保存的答案
    const getSavedAnswer = (questionId) => {
      return savedAnswers.value[questionId] || null
    }

    // 恢复当前题目的已选答案
    const restoreSelectedAnswer = () => {
      if (currentQuestion.value) {
        const savedAnswer = getSavedAnswer(currentQuestion.value.id)
        if (savedAnswer) {
          // 根据保存的identifier找到对应的选项索引
          const optionIndex = currentQuestion.value.options.findIndex(
            option => option.identifier === savedAnswer
          )
          selectedAnswer.value = optionIndex >= 0 ? optionIndex : null
        } else {
          selectedAnswer.value = null
        }
      } else {
        selectedAnswer.value = null
      }
    }

    // Next question
    const nextQuestion = async () => {
      if (selectedAnswer.value === null || !currentQuestion.value) return

      // Check if this question has already been answered
      const currentQuestionIndex = currentStep.value - 1
      const existingAnswer = userAnswers.value.find(ans => ans.questionIndex === currentQuestionIndex)

      if (existingAnswer) {
        // Question already answered, just move to next
        if (currentStep.value < testQuestions.value.length) {
          currentStep.value++
          // watch会自动恢复答案，不需要手动调用
        } else {
          await finishTest()
        }
        return
      }

      // Check if answer is correct - 使用API格式
      const selectedOption = currentQuestion.value.options[selectedAnswer.value]
      const correctOption = currentQuestion.value.options.find(opt => opt.is_answer === true)
      const isCorrect = selectedOption && correctOption && selectedOption.identifier === correctOption.identifier

      if (isCorrect) {
        correctAnswers.value++
      }

      // Store user answer
      userAnswers.value.push({
        questionIndex: currentQuestionIndex,
        selectedAnswer: selectedAnswer.value,
        isCorrect: isCorrect
      })

      // Move to next question or finish test
      if (currentStep.value < testQuestions.value.length) {
        currentStep.value++
        // watch会自动恢复答案，不需要手动调用
      } else {
        // Test completed - 调用完成测试API
        await finishTest()
      }
    }

    // 完成测试 - 调用PATCH /quizzes/attempt/{id}
    const finishTest = async () => {
      if (!currentAttemptId.value) return

      try {
        loading.value = true

        // 收集所有用户答案
        const allAnswers = []

        // 遍历所有题目，收集用户的答案
        for (let i = 0; i < testQuestions.value.length; i++) {
          const question = testQuestions.value[i]
          let userAnswer = null
          let isCorrect = false

          if (i < currentStep.value - 1) {
            // 已答题目
            const userAnswerData = userAnswers.value.find(ans => ans.questionIndex === i)
            if (userAnswerData) {
              userAnswer = question.options[userAnswerData.selectedAnswer]?.identifier
              isCorrect = userAnswerData.isCorrect
            }
          } else if (i === currentStep.value - 1) {
            // 当前题目
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

        const resultData = await response.json()
        testResult.value = resultData

        // 显示结果页面
        currentStep.value = testQuestions.value.length + 1

        // 重新加载用户进度以获取最新分数
        await loadUserProgress()

        // 重新获取用户stats以更新challenge_level
        await fetchUserStats()

        // 加载测试历史以显示在结果页面
        await loadTestHistory()

      } catch (err) {
        console.error('Error finishing test:', err)
        // 即使提交失败，也显示结果页面
        currentStep.value = testQuestions.value.length + 1
      } finally {
        loading.value = false
      }
    }

    // Previous question
    const previousQuestion = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        // watch会自动恢复答案，不需要手动调用
      }
    }


    // Retake test
    const retakeTest = () => {
      if (selectedModule.value) {
        startModuleTest(selectedModule.value)
      }
    }


    const goBackToModules = () => {
      selectedModule.value = null
      currentStep.value = 0
      testQuestions.value = []
      selectedAnswer.value = null
      correctAnswers.value = 0
      userAnswers.value = []
      savedAnswers.value = {}
      testResult.value = null
    }

    // 获取任务信息的通用方法
    const getTaskInfo = (taskNumber, field) => {
      return taskData.value[taskNumber]?.[field] || (field === 'modules' ? [] : '')
    }

    const getTaskTitle = (taskNumber) => getTaskInfo(taskNumber, 'title')
    const getTaskDescription = (taskNumber) => getTaskInfo(taskNumber, 'description')
    const getTaskModules = (taskNumber) => getTaskInfo(taskNumber, 'modules')

    // 用户进度数据 - 使用API获取
    const userProgress = ref({})
    const progressLoading = ref(false)

    // 从API获取用户进度
    const loadUserProgress = async () => {
      try {
        progressLoading.value = true
        const response = await fetch(`${API_BASE_URL}/quizzes/attempts/`, {
          headers: {
            'Authorization': `Bearer ${getAccessToken()}`
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to fetch user progress: ${response.status}`)
        }

        const data = await response.json()
        // 只处理已完成的测试 (有finished_at的记录)
        const completedAttempts = (Array.isArray(data) ? data : [])
          .filter(attempt => attempt.finished_at)

        // 按模块名称分组，获取每个模块的最高分数
        const moduleProgress = {}
        completedAttempts.forEach(attempt => {
          const moduleName = attempt.module_name

          if (moduleName) {
            const currentAccuracy = parseFloat(attempt.accuracy_pct)
            const existingAccuracy = moduleProgress[moduleName] ? parseFloat(moduleProgress[moduleName].accuracy_pct) : 0

            if (!moduleProgress[moduleName] || currentAccuracy > existingAccuracy) {
              moduleProgress[moduleName] = {
                accuracy_pct: attempt.accuracy_pct,
                correct_count: attempt.correct_count,
                total_questions: attempt.total_questions,
                isCompleted: currentAccuracy >= 80,
                completedAt: attempt.finished_at
              }
            }
          }
        })

        userProgress.value = moduleProgress

      } catch (err) {
        console.error('Error loading user progress:', err)
        userProgress.value = {}
      } finally {
        progressLoading.value = false
      }
    }

    // 模块进度相关方法
    const getModuleProgress = (moduleName) => {
      return userProgress.value[moduleName] || null
    }

    const isModuleCompleted = (moduleName) => {
      return getModuleProgress(moduleName)?.isCompleted || false
    }

    const getModuleScore = (moduleName) => {
      const progress = getModuleProgress(moduleName)
      return progress ? Math.round(progress.accuracy_pct) : 0
    }

    // Level相关方法
    const getLevelModules = (level) => {
      return getTaskModules(level) || []
    }

    const isLevelCompleted = (level) => {
      const modules = getLevelModules(level)
      return modules.length > 0 && modules.every(module => isModuleCompleted(module.name))
    }

    const isLevelUnlocked = (level) => {
      if (level === 1) return true
      return currentUser.value?.challenge_level >= level
    }

    const getCompletedModuleCount = (level) => {
      const modules = getLevelModules(level)
      return modules.filter(module => isModuleCompleted(module.name)).length
    }

    // 获取level图标
    const getLevelIcon = (level) => {
      const icons = {
        1: "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z", // Shield
        2: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z", // Check circle
        3: "M13 10V3L4 14h7v7l9-11h-7z" // Lightning
      }
      return icons[level] || icons[1]
    }

    // Test history methods
    const loadTestHistory = async () => {
      try {
        historyLoading.value = true
        const response = await fetch(`${API_BASE_URL}/quizzes/attempts/`, {
          headers: {
            'Authorization': `Bearer ${getAccessToken()}`
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to fetch test history: ${response.status}`)
        }

        const data = await response.json()
        // 只处理已完成的测试 (有finished_at的记录)
        const completedAttempts = (Array.isArray(data) ? data : [])
          .filter(attempt => attempt.finished_at)
          .sort((a, b) => new Date(b.finished_at) - new Date(a.finished_at)) // 按时间倒序排列

        // 只取最新的一个测试结果
        currentTestResult.value = completedAttempts.length > 0 ? completedAttempts[0] : null

      } catch (err) {
        console.error('Error loading test history:', err)
        currentTestResult.value = null
      } finally {
        historyLoading.value = false
      }
    }

    const refreshTestHistory = () => {
      loadTestHistory()
    }

    const viewHistoryDetails = async (attempt) => {
      try {
        // 使用与TestHistorySection相同的API端点获取详细信息
        const response = await fetch(`${API_BASE_URL}/quizzes/attempts/${attempt.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${getAccessToken()}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const detailedAttempt = await response.json()
          selectedHistoryAttempt.value = detailedAttempt
        } else {
          selectedHistoryAttempt.value = attempt // 如果无法获取详情，使用基本信息
        }
      } catch (error) {
        console.error('Error loading test details:', error)
        selectedHistoryAttempt.value = attempt
      }
    }

    const closeHistoryModal = () => {
      selectedHistoryAttempt.value = null
    }

    // Helper methods for test history display
    const getCategoryDisplayName = (category, attempt) => {
      // 优先使用 module_name
      if (attempt && attempt.module_name) {
        return attempt.module_name
      }
      // 如果没有 module_name，显示默认文本
      return 'Mixed Categories'
    }

    const getFormattedScore = (accuracyPct) => {
      if (accuracyPct === null || accuracyPct === undefined || isNaN(accuracyPct)) return 0
      return Math.round(Number(accuracyPct))
    }

    const getScoreClass = (accuracy) => {
      if (!accuracy) return 'poor'
      const percentage = accuracy * 100
      if (percentage >= 90) return 'excellent'
      if (percentage >= 75) return 'good'
      if (percentage >= 60) return 'fair'
      return 'poor'
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const calculateDuration = (startTime, endTime) => {
      if (!startTime || !endTime) return 'N/A'
      const start = new Date(startTime)
      const end = new Date(endTime)
      const diffInMinutes = Math.round((end - start) / (1000 * 60))
      return `${diffInMinutes} min`
    }

    // 监听当前步骤变化，自动恢复已保存的答案
    watch(currentStep, (newStep) => {
      if (newStep > 0 && newStep <= testQuestions.value.length) {
        // 使用nextTick确保currentQuestion计算属性已更新
        nextTick(() => {
          restoreSelectedAnswer()
        })
      }
    })

    // Check authentication on mount
    onMounted(async () => {
      await checkAuthStatus()
      await fetchTaskData()
      await loadUserProgress()
    })

    return {
      // Authentication
      isAuthenticated,
      currentUser,
      checkAuthStatus,
      redirectToSignUp,

      // Challenge state
      currentLevel,
      selectedModule,

      // Test state
      testQuestions,
      currentStep,
      selectedAnswer,
      correctAnswers,
      currentQuestion,
      currentQuestionOptions,
      loading,
      error,
      testResult,

      // Task data state
      taskData,
      taskDataLoading,
      taskDataError,

      // User progress state
      userProgress,
      progressLoading,
      isModuleCompleted,
      getModuleScore,
      isLevelCompleted,
      isLevelUnlocked,
      getCompletedModuleCount,
      getLevelIcon,

      // Test history state
      currentTestResult,
      historyLoading,
      selectedHistoryAttempt,

      // Toast state
      showToast,
      toastMessage,

      // Methods
      switchLevel,
      selectModule,
      goBackToModules,
      getTaskTitle,
      getTaskDescription,
      getTaskModules,
      selectAnswer,
      nextQuestion,
      previousQuestion,
      retakeTest,
      loadTestHistory,
      refreshTestHistory,
      viewHistoryDetails,
      closeHistoryModal,
      getCategoryDisplayName,
      getFormattedScore,
      getScoreClass,
      formatDate,
      calculateDuration
    }
  }
}
</script>

<style scoped>
.challenge-page {
  background: var(--violet-light);
  padding: 0;
}

.progress-section {
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  margin-bottom: 15px;
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


.challenge-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}


/* Progress Indicator */
.progress-indicator {
  margin-bottom: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
}

.progress-step {
  display: flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.progress-step:hover:not(.locked) {
  transform: scale(1.05);
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  color: white;
  background: var(--violet-sage);
  transition: all 0.3s ease;
  z-index: 2;
}

.progress-step.active .step-number {
  background: var(--violet-dark);
}

.progress-step.completed .step-number {
  background: var(--violet-ultra-dark);
}

.progress-step.locked .step-number {
  background: var(--violet-sage);
  opacity: 0.5;
}

.step-line {
  width: 60px;
  height: 3px;
  background: var(--violet-sage);
  margin-left: -1px;
  z-index: 1;
}

.progress-step.active .step-line {
  background: var(--violet-dark);
}

.progress-step.completed .step-line {
  background: var(--violet-ultra-dark);
}

/* Task Section */
.task-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Card Styles */
.task-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.task-header {
  text-align: center;
  margin-bottom: 40px;
}

.task-title {
  color: var(--violet-ultra-dark);
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.task-description {
  color: var(--violet-deep);
  font-size: 1.2rem;
  line-height: 1.6;
  max-width: 1000px;
  margin: 0 auto;
}

/* Module Cards */
.module-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-top: 40px;
  margin-bottom: 40px;
}

.module-card {
  background: #ffffff;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid var(--violet-sage);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 350px; /* 固定高度确保所有卡片一致 */
  justify-content: space-between; /* 内容均匀分布 */
}

.module-card:hover {
  border-color: var(--violet-dark);
}

.module-card.completed {
  border-color: var(--violet-dark);
  background: var(--violet-sage);
}

/* Completion Badge */
.completion-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #10B981;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  z-index: 10;
}

.completion-badge svg {
  width: 16px;
  height: 16px;
}

/* Module Icon */
.module-icon {
  width: 60px;
  height: 60px;
  background: var(--violet-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--violet-dark);
  margin-bottom: 1.5rem;
  flex-shrink: 0;
}

.module-info {
  flex: 1;
  margin-bottom: 20px;
}

.module-title {
  color: var(--violet-ultra-dark);
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.module-description {
  color: var(--violet-deep);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 15px;
}


/* Button Styles */
.start-module-btn,
.back-to-modules-btn {
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.start-module-btn:hover,
.back-to-modules-btn:hover {
  background: var(--violet-dark);
}

/* Module Test */
.module-test {
  max-width: 1200px;
  margin: 0 auto;
}

.test-header {
  margin-top: 1rem;
  margin-bottom: 1rem;
}


.question-section {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 60px;
}

.question-header {
  margin-bottom: 15px;
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
  margin-bottom: 15px;
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

.question-actions .next-btn:only-child {
  margin-left: auto;
}

/* Navigation Buttons */
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
}

.next-btn:disabled {
  background: var(--violet-sage);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Results Section */
.results-section {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 60px;
}

.results-header {
  text-align: center;
  margin-bottom: 40px;
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

/* Results Container */
.results-container {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 20px var(--shadow-light);
  border: 1px solid var(--border-light);
}

.score-section {
  margin-bottom: 2rem;
}

.overall-score {
  text-align: center;
  margin-bottom: 15px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: var(--violet-ultra-dark);
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
  margin: 0 0 10px 0;
}

.score-detail {
  color: var(--violet-deep);
  font-size: 1rem;
  margin: 0;
}

.results-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

/* Action Buttons */
.retake-btn {
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retake-btn:hover {
  background: var(--violet-dark);
}

.results-back-btn {
  background: var(--violet-deep);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.results-back-btn:hover {
  background: var(--violet-dark);
}

/* Messages Content */
.messages-content {
  background: transparent;
  color: var(--text-primary);
  line-height: 1.5;
  font-size: 0.95rem;
  text-align: center;
}

/* Test Details Section */
.test-details-section {
  margin-top: 1.5rem;
}

.test-details-header {
  margin-bottom: 1.5rem;
}

.test-details-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.test-details-icon {
  color: var(--violet-deep);
}

.view-details-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: var(--violet-deep);
  border: none;
  border-radius: 6px;
  color: var(--text-light);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  margin-left: 1rem;
}

.view-details-btn:hover {
  background: var(--violet-dark);
}


/* Feedback Section */
.feedback-section {
  margin-top: 1.5rem;
}

.feedback-header {
  margin-bottom: 1.5rem;
}

.feedback-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--violet-ultra-dark);
  margin: 0;
}

.feedback-icon {
  color: var(--violet-deep);
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feedback-summary {
  background: var(--violet-light);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--violet-sage);
}

.feedback-subtitle {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--violet-dark);
  margin: 0 0 0.75rem 0;
}

.feedback-text {
  color: var(--text-primary);
  line-height: 1.6;
  margin: 0;
  font-size: 1rem;
}

.feedback-actions {
  background: var(--violet-light);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--violet-sage);
}

.action-items-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.action-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  line-height: 1.5;
}

.action-item:last-child {
  border-bottom: none;
}

.action-icon {
  color: var(--violet-deep);
  flex-shrink: 0;
  margin-top: 0.125rem;
}

/* Responsive Design for Results */
@media (max-width: 768px) {
  .results-container {
    padding: 1.5rem;
    margin: 1.5rem 0;
  }

  .messages-content {
    padding: 1rem;
  }

  .feedback-title {
    font-size: 1.25rem;
  }

  .feedback-summary,
  .feedback-actions {
    padding: 1.25rem;
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

/* Challenge Levels Styles */
.challenge-levels {
  max-width: 1200px;
  margin: 0 auto;
}

.current-level {
  margin-top: 2rem;
}

.level-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--violet-dark);
  margin-bottom: 0.5rem;
}

.level-description {
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.5;
}


.module-progress {
  margin-top: 1rem;
}

.progress-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: block;
}

.locked-module {
  color: var(--violet-medium);
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  padding: 1rem;
  background: var(--violet-light);
  border-radius: 8px;
  border: 1px dashed var(--border-light);
}


.nav-back-btn {
  background: var(--violet-medium);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.nav-back-btn:hover {
  background: var(--text-secondary);
  transform: translateY(-1px);
}


/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  max-width: 1000px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid var(--violet-sage);
}

.modal-header h3 {
  color: var(--violet-dark);
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: var(--violet-deep);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(83, 43, 136, 0.1);
}

.modal-body {
  padding: 0;
}

.test-summary {
  margin-bottom: 25px;
  background: var(--violet-light);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--violet-sage);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 15px;
}

.summary-row span:first-child {
  color: var(--violet-deep);
  font-weight: 500;
}

.summary-row span:last-child {
  color: var(--violet-dark);
  font-weight: 600;
}

.questions-detail h4 {
  color: var(--violet-dark);
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: 600;
}

.question-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid var(--violet-sage);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.question-number {
  color: var(--violet-dark);
  font-weight: 600;
  font-size: 1.1rem;
}

.question-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.question-status.correct {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.question-status.incorrect {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.question-text {
  color: var(--violet-dark);
  margin-bottom: 15px;
  line-height: 1.5;
  font-size: 15px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal-content .option-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  position: relative;
  border-radius: 6px;
  border: 1px solid rgba(200, 177, 228, 0.3);
  background: rgba(255, 255, 255, 0.5);
}

.modal-content .option-item.correct {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.3);
}
.modal-content .option-item.selected {
  background: rgba(0, 123, 255, 0.1);
  border: 1px solid rgba(0, 123, 255, 0.3);
}
.modal-content .option-item.wrong-selected {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.modal-content .option-identifier {
  font-weight: bold;
  color: var(--violet-dark);
  margin-right: 10px;
}

.modal-content .option-text {
  color: var(--violet-dark);
  flex: 1;
}

.correct-indicator {
  color: #28a745;
  font-weight: bold;
}

.wrong-indicator {
  color: #dc3545;
  font-weight: bold;
}

/* 选项状态样式 */
.modal-content .option-item.correct .option-text { color: #28a745; font-weight: 600; }
.modal-content .option-item.selected .option-text { color: #007bff; font-weight: 600; }
.modal-content .option-item.wrong-selected .option-text { color: #dc3545; font-weight: 600; }

.question-explanation {
  margin-top: 15px;
  padding: 15px;
  background: var(--violet-light);
  border-radius: 8px;
  border-left: 3px solid var(--violet-deep);
}

.question-explanation h5 {
  margin: 0 0 12px 0;
  color: var(--violet-dark);
  font-weight: 600;
}

.question-explanation p {
  margin: 0;
  color: var(--violet-deep);
  line-height: 1.7;
}

/* Level Toast Styles */
.level-toast {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 10000;
  animation: slideInRight 0.3s ease-out;
}

.toast-content {
  background: var(--violet-deep);
  color: white;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(83, 43, 136, 0.3);
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 300px;
  max-width: 400px;
}

.toast-icon {
  flex-shrink: 0;
  color: white;
}

.toast-message {
  flex: 1;
  font-size: 0.95rem;
  font-weight: 500;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .level-toast {
    top: 10px;
    right: 10px;
    left: 10px;
  }

  .toast-content {
    min-width: auto;
    padding: 12px 16px;
  }

  .toast-message {
    font-size: 0.9rem;
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .module-cards {
    grid-template-columns: 1fr;
    gap: 25px;
  }
}

@media (max-width: 768px) {
  .challenge-content {
    padding: 10px;
  }

  .task-title {
    font-size: 2rem;
  }

  .task-description {
    font-size: 1rem;
  }

  .module-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .module-card {
    padding: 20px;
    height: auto;
    min-height: 250px;
  }

  .module-icon {
    width: 50px;
    height: 50px;
  }

  .module-icon svg {
    width: 40px;
    height: 40px;
  }

  .progress-steps {
    flex-wrap: wrap;
    gap: 10px;
  }

  .step-line {
    width: 40px;
  }
}
</style>
