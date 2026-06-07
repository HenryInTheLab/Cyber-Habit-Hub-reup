<template>
  <div v-if="showToast" class="toast" :class="{ 'toast-show': showToast }">
    <div class="toast-content">
      <div class="toast-message">
        <div class="toast-title">{{ toastData.title }}</div>
        <div class="toast-description">{{ toastData.description }}</div>
      </div>
      <div class="toast-points">+{{ toastData.points }}</div>
      <button @click="closeToast" class="toast-close">&times;</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showToast = ref(false)
const toastData = ref({
  title: '',
  description: '',
  points: 0
})

const showActivityToast = async (duration = 6000) => {
  try {
    const token = localStorage.getItem("access_token")
    const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/leaderboard/activity/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const activities = await response.json()
      if (activities && activities.length > 0) {
        const latestActivity = activities[0]
        const rewardType = latestActivity.reward
        const points = latestActivity.points
        const meta = latestActivity.meta

        let title = ''
        let description = ''

        switch (rewardType) {
          case 'READ_ARTICLE':
            title = 'Article Read! You\'ve got points!'
            description = meta.article_title || 'You read an article'
            break
          case 'WATCH_VIDEO':
            title = 'Video Watched! You\'ve got points!'
            description = meta.video_title || 'You watched a video'
            break
          case 'FRIEND_INVITATION':
            title = 'Friend Invited! You\'ve got points!'
            description = 'You successfully invited a friend'
            break
          default:
            title = 'Activity Completed! You\'ve got points!'
            description = 'You completed an activity'
        }

        toastData.value = {
          title,
          description,
          points
        }

        showToast.value = true

        setTimeout(() => {
          showToast.value = false
        }, duration)
      }
    }
  } catch (error) {
    console.error('Error fetching activity log:', error)
  }
}

const closeToast = () => {
  showToast.value = false
}

// Expose methods globally
window.showActivityToast = showActivityToast
</script>

<style scoped>
.toast {
  position: fixed;
  top: 80px;
  right: 20px;
  background: white;
  border-radius: 12px;
  z-index: 1000;
  transform: translateX(100%);
  opacity: 0;
  transition: all 0.3s ease;
}

.toast-show {
  transform: translateX(0);
  opacity: 1;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.toast-title {
  font-weight: 600;
  color: var(--text-primary);
}

.toast-description {
  color: var(--text-secondary);
}

.toast-points {
  font-weight: 700;
  color: var(--violet-deep);
  background: var(--violet-light);
  padding: 8px 12px;
  border-radius: 8px;
}

.toast-close {
  background: none;
  border: none;
  font-size: 20px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.toast-close:hover {
  background: var(--border-light);
}
</style>
