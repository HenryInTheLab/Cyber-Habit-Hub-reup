<template>
  <div class="challenge-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Cybersecurity Learning Challenges</h1>
        <p class="page-subtitle">Progressive cybersecurity learning system with three contextualized tasks</p>
      </div>
    </div>

    <div class="page-content">
      <div class="container">
        <!-- Challenge Section -->
        <ChallengeSection @challenge-status-changed="handleChallengeStatusChanged" />
      </div>
    </div>

    <!-- Footer only shows when authenticated and challenge is not active -->
    <FooterSection v-if="isAuthenticated && !isChallengeActive" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ChallengeSection from '../section/TestPage/ChallengeSection.vue'
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'ChallengePage',
  components: {
    ChallengeSection,
    FooterSection
  },
  setup() {
    const isAuthenticated = ref(false)
    const isChallengeActive = ref(false)

    const checkAuthStatus = () => {
      try {
        const accessToken = localStorage.getItem('access_token')
        const userInfoStr = localStorage.getItem('user_info')

        if (accessToken && userInfoStr) {
          isAuthenticated.value = true
        } else {
          isAuthenticated.value = false
        }
      } catch (error) {
        console.error('Error checking auth status:', error)
        isAuthenticated.value = false
      }
    }

    const handleChallengeStatusChanged = (isActive) => {
      isChallengeActive.value = isActive
    }

    onMounted(() => {
      checkAuthStatus()
    })

    return {
      isAuthenticated,
      isChallengeActive,
      handleChallengeStatusChanged
    }
  }
}
</script>

<style scoped>
.challenge-page {
  background-color: var(--bg-primary);
}

.page-header {
  background: var(--violet-dark);
  color: var(--text-light);
  padding: 4rem 0;
  text-align: center;
}

.page-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px var(--shadow-dark);
}

.page-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto;
}

.page-content {
  padding: 0;
}

.container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 8rem;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.5rem;
  }

  .page-subtitle {
    font-size: 1.1rem;
  }

  .container {
    padding: 0 1rem;
  }
}
</style>
