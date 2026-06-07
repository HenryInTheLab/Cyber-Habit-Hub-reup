<template>
  <div
    v-if="showButton"
    class="back-to-top"
    @click="scrollToTop"
    :class="{ 'visible': showButton }"
  >
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'BackToTop',
  setup() {
    const showButton = ref(false)

    const handleScroll = () => {
      // 当页面滚动超过300px时显示按钮
      showButton.value = window.scrollY > 200
    }

    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }

    onMounted(() => {
      window.addEventListener('scroll', handleScroll)
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
    })

    return {
      showButton,
      scrollToTop
    }
  }
}
</script>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 100px; /* 在chatbot上面 */
  right: 20px;
  width: 40px;
  height: 40px;
  background: var(--violet-dark);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2000;
  opacity: 0;
  transform: translateY(20px);
}

.back-to-top.visible {
  opacity: 1;
  transform: translateY(0);
}

.back-to-top:hover {
  background: var(--violet-ultra-dark);
}

.back-to-top:active {
  transform: translateY(0);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .back-to-top {
    bottom: 100px;
    right: 15px;
    width: 45px;
    height: 45px;
  }
}
</style>
