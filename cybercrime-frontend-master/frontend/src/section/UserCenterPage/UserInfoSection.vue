<template>
  <div class="user-info-section">
    <div class="user-info-container">
      <h2 class="section-title">User Center</h2>

          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading user information...</p>
          </div>

          <!-- User Info Display -->
          <div v-else-if="isAuthenticated && userInfo" class="user-info-display">
            <div class="user-profile">
              <div class="user-avatar">
                {{ getUserInitial() }}
              </div>
              <div class="user-details">
                <div class="username-container">
                  <h3 class="username">{{ userInfo.username || 'User' }}</h3>
                  <div v-if="getUserBadges().length > 0" class="user-badges">
                    <div
                      v-for="badge in getUserBadges()"
                      :key="badge.name"
                      class="user-badge"
                    >
                      <img :src="badge.src" :alt="badge.name" class="badge-image" />
                    </div>
                  </div>
                </div>
                <div v-if="badgeInfo" class="badge-container">
                  <span class="badge-label">Title:</span>
                  <span class="badge">{{ badgeInfo.name }}</span>
                </div>
                <p v-if="userInfo.createdAt" class="member-since">
                  Member since: {{ formatDate(userInfo.createdAt) }}
                </p>
              </div>
              <div class="points-section">
                <div class="points-display">
                  <div class="points-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
                    </svg>
                  </div>
                  <div class="points-info">
                    <div class="points-number">{{ points }}</div>
                    <div class="points-label">Points</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Not Authenticated State -->
          <div v-else-if="!isAuthenticated" class="not-authenticated">
            <div class="empty-state">
              <div class="empty-icon">🔒</div>
              <h3>Not Signed In</h3>
              <p>Please sign in to view your user information.</p>
              <button @click="goToSignIn" class="btn btn-signin">
                Sign In
              </button>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="authError" class="error-state">
            <div class="alert alert-danger">
              <h6 class="alert-heading">Error loading user information:</h6>
              <p>{{ authError }}</p>
              <button @click="retryLoad" class="btn btn-retry">
                Try Again
              </button>
            </div>
          </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getValidAccessToken } from '@/utils/auth.js'
// 导入badge图片
import NoviceScholarBadge from '@/assets/Badges/Novice Scholar.png'
import KnowledgeExplorerBadge from '@/assets/Badges/Knowledge Explorer.png'
import LearningExpertBadge from '@/assets/Badges/Learning Expert.png'
import CybersecurityMasterBadge from '@/assets/Badges/Cybersecurity Master.png'

export default {
  name: 'UserInfoSection',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const isAuthenticated = ref(false)
    const userInfo = ref(null)
    const authError = ref(null)
    const points = ref(0)
    const badgeInfo = ref(null)

    const checkAuthStatus = async () => {
      try {
        loading.value = true
        authError.value = null

        // Check if user has access token
        const accessToken = localStorage.getItem('access_token')
        const userInfoStr = localStorage.getItem('user_info')

        if (!accessToken || !userInfoStr) {
          isAuthenticated.value = false
          userInfo.value = null
          return
        }

        // Parse user info from localStorage
        const storedUserInfo = JSON.parse(userInfoStr)

        isAuthenticated.value = true
        userInfo.value = {
          username: storedUserInfo.username || 'User',
          createdAt: storedUserInfo.date_joined || new Date().toISOString(),
        }

        // 获取用户积分
        await fetchUserStats()

      } catch (error) {
        console.error('Error checking auth status:', error)
        isAuthenticated.value = false
        userInfo.value = null
        authError.value = 'Failed to load user information. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const getUserInitial = () => {
      if (!userInfo.value) return '?'
      const name = userInfo.value.username
      return name.charAt(0).toUpperCase()
    }

    const formatDate = (dateString) => {
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return 'Unknown date'
      }
    }

    // 获取Access Token
    const getAccessToken = () => {
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
    }

    // 获取用户积分和徽章信息
    const fetchUserStats = async () => {
      try {
        const accessToken = localStorage.getItem('access_token')
        if (!accessToken) {
          points.value = 0
          badgeInfo.value = null
          return
        }

        const API_BASE_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com'
        const response = await fetch(`${API_BASE_URL}/leaderboard/me/`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
          }
        })

        if (response.ok) {
          const data = await response.json()
          points.value = data.points || 0
          badgeInfo.value = data.badge || null
        } else {
          points.value = 0
          badgeInfo.value = null
        }
      } catch (err) {
        console.error('Error fetching user stats:', err)
        points.value = 0
        badgeInfo.value = null
      }
    }



    const goToSignIn = () => {
      router.push('/signin')
    }

    const retryLoad = () => {
      checkAuthStatus()
    }

    // 根据积分获取所有符合条件的徽章
    const getUserBadges = () => {
      const badges = []
      const userPoints = points.value

      if (userPoints >= 10) {
        badges.push({
          name: 'Novice Scholar',
          src: NoviceScholarBadge
        })
      }

      if (userPoints >= 30) {
        badges.push({
          name: 'Knowledge Explorer',
          src: KnowledgeExplorerBadge
        })
      }

      if (userPoints >= 60) {
        badges.push({
          name: 'Learning Expert',
          src: LearningExpertBadge
        })
      }

      if (userPoints >= 90) {
        badges.push({
          name: 'Cybersecurity Master',
          src: CybersecurityMasterBadge
        })
      }

      return badges
    }

    onMounted(() => {
      checkAuthStatus()
    })

    return {
      loading,
      isAuthenticated,
      userInfo,
      authError,
      points,
      badgeInfo,
      getUserInitial,
      formatDate,
      goToSignIn,
      retryLoad,
      getUserBadges,
    }
  },
}
</script>

<style scoped>
.user-info-section {
  padding: 2rem 0;
}

.user-info-container {
  max-width: 1600px;
  margin: 0 auto;
}

.section-title {
  color: var(--violet-ultra-dark);
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 3rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--violet-sage);
  border-top: 4px solid var(--violet-ultra-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* User Profile */
.user-profile {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  box-shadow: 0 4px 15px var(--shadow-light);
  max-width: 1200px;
  margin: 0 auto;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--violet-ultra-dark);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  flex-shrink: 0;
  box-shadow: 0 4px 15px var(--shadow-medium);
}

.user-details {
  flex: 1;
}

.points-section {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.points-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: var(--violet-light);
  border-radius: 12px;
  border: 1px solid var(--violet-sage);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.points-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--violet-deep);
}

.points-icon svg {
  width: 24px;
  height: 24px;
}

.points-info {
  text-align: center;
}

.points-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--violet-ultra-dark);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.points-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--violet-deep);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.username-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.username {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--violet-ultra-dark);
}

.user-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.user-badge {
  display: flex;
  align-items: center;
}

.badge-image {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.member-since {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: var(--violet-deep);
}

.badge-container {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge-label {
  font-size: 1rem;
  color: var(--violet-deep);
  font-weight: 500;
}

.badge {
  background: var(--violet-deep);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  display: inline-block;
}

/* Not Authenticated State */
.not-authenticated {
  text-align: center;
  padding: 3rem 0;
}

.empty-state {
  padding: 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: var(--violet-ultra-dark);
  margin-bottom: 1rem;
}

.empty-state p {
  color: var(--violet-deep);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.btn-signin {
  background: var(--violet-ultra-dark);
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-signin:hover {
  background: var(--violet-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow-medium);
}

/* Error State */
.error-state {
  padding: 2rem;
}

.alert {
  padding: 1.5rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.alert-danger {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.alert-heading {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.btn-retry {
  background: #dc3545;
  color: white;
  margin-top: 1rem;
}

.btn-retry:hover {
  background: #c82333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .user-info-container {
    padding: 0 1rem;
  }

  .user-profile {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
    padding: 1.5rem;
    max-width: 100%;
  }

  .user-avatar {
    width: 70px;
    height: 70px;
    font-size: 2rem;
  }

  .username {
    font-size: 1.5rem;
  }

  .username-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .badge-image {
    width: 35px;
    height: 35px;
  }

  .points-section {
    margin-left: 0;
    justify-content: center;
  }

  .points-display {
    padding: 0.75rem 1rem;
  }

  .points-number {
    font-size: 1.25rem;
  }
}

</style>
