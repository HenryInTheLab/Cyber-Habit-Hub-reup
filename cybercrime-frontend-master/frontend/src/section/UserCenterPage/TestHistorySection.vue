<template>
  <!-- 测试历史区域 -->
  <div class="test-history-section">
    <div class="section-header">
      <h2>Challenge History</h2>
      <div class="stats-summary">
        <div class="stat-item-challenge">
          <router-link to="/challenge">
            Continue to Challenge Page
          </router-link>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ totalTests }}</span>
          <span class="stat-label">Total Tests</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ averageScore }}%</span>
          <span class="stat-label">Average Score</span>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading your test history...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadTestHistory" class="retry-btn">Retry</button>
    </div>

    <!-- 测试记录列表 -->
    <div v-else-if="testAttempts.length > 0" class="test-list">
      <div
        v-for="attempt in paginatedTestAttempts"
        :key="attempt.id"
        class="test-card"
        @click="viewTestDetails(attempt)"
      >
        <div class="test-header">
          <div class="test-info">
            <h3>{{ getCategoryDisplayName(attempt.category, attempt) }}</h3>
            <p class="test-date">{{ formatDate(attempt.finished_at) }}</p>
          </div>
          <div class="test-score" :class="getScoreClass(attempt.accuracy_pct)">
            {{ getFormattedScore(attempt.accuracy_pct) }}%
          </div>
        </div>

        <div class="test-details">
          <div class="detail-row">
            <span>Questions: {{ attempt.correct_count }}/{{ attempt.total_questions }}</span>
            <span>Duration: {{ calculateDuration(attempt.started_at, attempt.finished_at) }}</span>
          </div>

          <!-- 进度条 -->
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: Math.min(attempt.accuracy_pct, 100) + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 分页控件 -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="page-btn prev-btn"
        >
          Previous
        </button>

        <div class="page-numbers">
          <span
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="['page-number', { active: page === currentPage }]"
          >
            {{ page }}
          </span>
        </div>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="page-btn next-btn"
        >
          Next
        </button>
      </div>
    </div>

    <!-- 无测试记录 -->
    <div v-else class="no-tests">
      <p>No test records found</p>
      <router-link to="/challenge" class="take-test-btn">Take Your First Challenge</router-link>
    </div>
  </div>

  <!-- Test History Details Modal -->
  <div v-if="selectedAttempt" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Test Details</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>

      <div class="modal-body">
        <div class="test-summary">
          <div class="summary-row">
            <span>Category:</span>
            <span>{{ getCategoryDisplayName(selectedAttempt.category, selectedAttempt) }}</span>
          </div>
          <div class="summary-row">
            <span>Score:</span>
            <span>{{ getFormattedScore(selectedAttempt.accuracy_pct) }}%</span>
          </div>
          <div class="summary-row">
            <span>Correct Answers:</span>
            <span>{{ selectedAttempt.correct_count }}/{{ selectedAttempt.total_questions }}</span>
          </div>
          <div class="summary-row">
            <span>Date:</span>
            <span>{{ formatDate(selectedAttempt.finished_at) }}</span>
          </div>
          <div class="summary-row">
            <span>Duration:</span>
            <span>{{ calculateDuration(selectedAttempt.started_at, selectedAttempt.finished_at) }}</span>
          </div>
        </div>

        <!-- Question Details -->
        <div v-if="selectedAttempt.quiz_question_attempts" class="questions-detail">
          <h4>Question Details</h4>
          <div
            v-for="(qa, index) in selectedAttempt.quiz_question_attempts"
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
                    'correct-option': option.is_answer,
                    'user-selected': qa.chosen_answer === option.identifier,
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
</template>

<script>

import { getValidAccessToken } from '@/utils/auth.js'

export default {
  name: 'TestHistorySection',
  data() {
    return {
      testAttempts: [],
      loading: true,
      error: null,
      selectedAttempt: null,
      currentPage: 1,
      itemsPerPage: 5,
      expandedQuestions: new Set() // 跟踪展开的问题
    }
  },
  computed: {
    totalTests() {
      return this.testAttempts.length
    },
    averageScore() {
      if (this.testAttempts.length === 0) return 0

      const validAttempts = this.testAttempts.filter(attempt =>
        attempt.accuracy_pct !== null &&
        attempt.accuracy_pct !== undefined &&
        !isNaN(attempt.accuracy_pct)
      )

      if (validAttempts.length === 0) return 0

      const total = validAttempts.reduce((sum, attempt) => sum + Number(attempt.accuracy_pct), 0)
      return Math.round(total / validAttempts.length)
    },
    totalPages() {
      return Math.ceil(this.testAttempts.length / this.itemsPerPage)
    },
    paginatedTestAttempts() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.testAttempts.slice(start, end)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)

      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      return pages
    }
  },
  async mounted() {
    await this.loadTestHistory()
  },
  methods: {
    // 获取Access Token
    async getAccessToken() {
      try {
        const token = getValidAccessToken()
        if (!token) {
          throw new Error('No valid access token found')
        }
        return token
      } catch (error) {
        console.error('Error getting access token:', error)
        throw error
      }
    },

    // 加载测试历史
    async loadTestHistory() {
      try {
        this.loading = true
        this.error = null

        const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/quizzes/attempts/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${await this.getAccessToken()}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to load test history: ${response.status}`)
        }

        const data = await response.json()
        // 只显示已完成的测试 (有finished_at的记录)
        this.testAttempts = (Array.isArray(data) ? data : [])
          .filter(attempt => attempt.finished_at)
          .sort((a, b) => new Date(b.finished_at) - new Date(a.finished_at)) // 按时间倒序

      } catch (error) {
        console.error('Error loading test history:', error)
        this.error = 'Failed to load test history. Please try again.'
      } finally {
        this.loading = false
      }
    },

    // 查看测试详情
    async viewTestDetails(attempt) {
      try {
        const response = await fetch(`https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/quizzes/attempts/${attempt.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${await this.getAccessToken()}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const detailedAttempt = await response.json()
          this.selectedAttempt = detailedAttempt
        } else {
          this.selectedAttempt = attempt // 如果无法获取详情，使用基本信息
        }
      } catch (error) {
        console.error('Error loading test details:', error)
        this.selectedAttempt = attempt
      }
    },

    // 关闭模态框
    closeModal() {
      this.selectedAttempt = null
      this.expandedQuestions.clear() // 清空展开状态
    },

    // 切换问题展开状态
    toggleQuestionExpansion(index) {
      if (this.expandedQuestions.has(index)) {
        this.expandedQuestions.delete(index)
      } else {
        this.expandedQuestions.add(index)
      }
    },

    // 检查问题是否已展开
    isQuestionExpanded(index) {
      return this.expandedQuestions.has(index)
    },

    // 检查选项是否被用户选中
    isUserSelectedOption(qa, option) {
      if (!qa.chosen_answer) return false

      // 直接匹配identifier（现在所有答案都存储为字母标识符）
      return qa.chosen_answer === option.identifier
    },

    // 获取用户答案的文本
    getUserAnswerText(qa) {
      if (!qa.chosen_answer) return 'No answer provided'

      if (qa.question && qa.question.options) {
        // 直接匹配identifier（现在所有答案都存储为字母标识符）
        const selectedOption = qa.question.options.find(opt => opt.identifier === qa.chosen_answer)

        if (selectedOption) {
          return `${selectedOption.identifier}. ${selectedOption.text}`
        }
      }

      return `Option ${qa.chosen_answer}`
    },

    // 获取正确答案的文本
    getCorrectAnswerText(qa) {
      if (qa.question && qa.question.options) {
        const correctOption = qa.question.options.find(opt => opt.is_answer)
        if (correctOption) {
          return `${correctOption.identifier}. ${correctOption.text}`
        }
      }

      return 'Correct answer not available'
    },

    // 获取解释文本
    getExplanationText(qa) {
      // 首先检查question对象中是否有explanation
      if (qa.question && qa.question.explanation) {
        return qa.question.explanation
      }

      // 如果question对象中没有，检查qa对象本身是否有explanation
      if (qa.explanation) {
        return qa.explanation
      }

      // 返回null表示没有解释
      return null
    },

    // 获取正确答案的索引
    getCorrectAnswerIndex(qa) {
      // 如果API响应中有正确答案信息，使用它
      if (qa.correct_answer_index !== undefined) {
        return qa.correct_answer_index
      }

      // 如果API响应中有正确答案的identifier，尝试找到对应的索引
      if (qa.correct_answer_identifier) {
        // 这里需要根据实际的题目数据结构来查找
        // 暂时返回一个占位符
        return 'A' // 显示为Option A
      }

      // 默认返回A选项
      return 0
    },

    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    // 计算测试时长
    calculateDuration(startTime, endTime) {
      if (!startTime || !endTime) return 'N/A'
      const start = new Date(startTime)
      const end = new Date(endTime)
      const diffInMinutes = Math.round((end - start) / (1000 * 60))
      return `${diffInMinutes} min`
    },

    // 获取分数样式类
    getScoreClass(accuracy) {
      if (!accuracy) return 'poor'
      const percentage = accuracy * 100
      if (percentage >= 90) return 'excellent'
      if (percentage >= 75) return 'good'
      if (percentage >= 60) return 'fair'
      return 'poor'
    },

    // 获取类别显示名称
    getCategoryDisplayName(category, attempt) {
      // 优先使用 module_name
      if (attempt && attempt.module_name) {
        return attempt.module_name
      }

      // 如果没有 module_name，显示默认文本
      return 'Mixed Categories'
    },

    // 获取正确格式的分数
    getFormattedScore(accuracyPct) {
      if (accuracyPct === null || accuracyPct === undefined || isNaN(accuracyPct)) return 0
      return Math.round(Number(accuracyPct))
    },

    // 分页方法
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  }
}
</script>

<style scoped>
/* 测试历史样式 */

.stat-item-challenge {
  border-radius: 12px;
  padding: 0;            /* let the link control spacing */
  border: none;
  background: transparent;
  box-shadow: none;
}

/* make the link look exactly like your continue-button */
.stat-item-challenge a {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 100%;
  padding: 1rem 2rem;

  background: var(--violet-deep);
  color: var(--violet-light);
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;

  box-shadow: 0 4px 12px var(--shadow-dark);
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.stat-item-challenge a:hover {
  background: var(--violet-dark);
  transform: translateY(-2px);
}

.stat-item-challenge:active {
  transform: translateY(-1px) scale(0.99);
  box-shadow: 0 3px 8px rgba(80, 60, 140, 0.15);
}

.test-history-section {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  max-width: 1200px;
  margin: 0 auto;
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--violet-sage);
}

.section-header h2 {
  margin: 0;
  color: var(--violet-dark);
  font-size: 1.8rem;
  font-weight: 600;
}

.stats-summary {
  display: flex;
  gap: 30px;
}

.stat-item{
  text-align: center;
  background: var(--violet-light);
  padding: 15px 20px;
  border-radius: 12px;
  border: 1px solid var(--violet-sage);
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: var(--violet-medium);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 13px;
  color: var(--violet-deep);
  font-weight: 500;
}

.test-card {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid var(--violet-sage);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  backdrop-filter: blur(5px);
}

.test-card:hover {
  background: var(--violet-light);
  border-color: var(--violet-dark);
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.test-info h3 {
  margin: 0 0 8px 0;
  color: var(--violet-dark);
  font-size: 18px;
  font-weight: 600;
}

.test-date {
  margin: 0;
  color: var(--violet-deep);
  font-size: 13px;
  font-weight: 500;
}

.test-score {
  font-size: 20px;
  font-weight: bold;
  padding: 8px 15px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.test-score.excellent { background: var(--violet-light); color: var(--violet-ultra-dark); }
.test-score.good { background: var(--violet-sage); color: var(--violet-dark); }
.test-score.fair { background: var(--violet-light); color: var(--violet-deep); }
.test-score.poor { background: var(--violet-sage); color: var(--violet-deep); }

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--violet-deep);
  margin-bottom: 12px;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: var(--violet-ultra-dark);
  border-radius: 4px;
}

.loading, .error, .no-tests {
  text-align: center;
  padding: 40px 20px;
  color: var(--violet-deep);
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  margin: 20px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--violet-sage);
  border-top: 4px solid var(--violet-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-btn, .take-test-btn {
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  margin-top: 15px;
  font-weight: 600;
  box-shadow: 0 4px 15px var(--shadow-medium);
}

.retry-btn:hover, .take-test-btn:hover {
  background: var(--violet-dark);
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
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
}

.close-btn:hover {
  color: var(--violet-dark);
  background: var(--violet-light);
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
  margin-bottom: 12px;
  font-size: 15px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.summary-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.summary-row span:first-child {
  font-weight: 600;
  color: var(--violet-deep);
}

.summary-row span:last-child {
  font-weight: 600;
  color: var(--violet-dark);
}

.questions-detail h4 {
  margin: 25px 0 15px 0;
  color: var(--violet-dark);
  font-size: 1.3rem;
  font-weight: 600;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--violet-sage);
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

.modal-content .option-item.correct-option {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.3);
}
.modal-content .option-item.user-selected {
  background: rgba(0, 123, 255, 0.1);
  border: 1px solid rgba(0, 123, 255, 0.3);
}
.modal-content .option-item.wrong-selected {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.correct-indicator {
  color: #28a745;
  font-weight: bold;
}

.wrong-indicator {
  color: #dc3545;
  font-weight: bold;
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

.correct-mark {
  color: #28a745;
  font-weight: bold;
  font-size: 16px;
  margin-left: 10px;
}

/* 选项状态样式 */
.modal-content .option-item.correct-option .option-text { color: #28a745; font-weight: 600; }
.modal-content .option-item.user-selected .option-text { color: #007bff; font-weight: 600; }
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

/* 分页控件样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
  padding: 20px 0;
}

.page-btn {
  padding: 10px 20px;
  border: 2px solid var(--violet-medium);
  background: white;
  color: var(--violet-dark);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--violet-medium);
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 8px;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--violet-sage);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  background: white;
  color: var(--violet-dark);
}

.page-number:hover {
  border-color: var(--violet-medium);
  background: var(--violet-light);
}

.page-number.active {
  background: var(--violet-dark);
  color: white;
  border-color: var(--violet-dark);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 20px;
  }

  .page-numbers {
    order: 2;
  }

  .page-btn {
    order: 1;
  }
}
</style>

