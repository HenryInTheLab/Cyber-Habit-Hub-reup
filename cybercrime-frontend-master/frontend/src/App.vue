<template>
  <div id="app">
    <NavigationBar v-if="!isAuthPage" />

    <router-view />

    <!-- AI ChatBot -->
    <ChatBot v-if="!isAuthPage && !isChallengePage" />

    <!-- Back to Top Button -->
    <BackToTop />

    <!-- Global Toast -->
    <Toast />
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'
import ChatBot from '@/components/ChatBot.vue'
import BackToTop from '@/components/BackToTop.vue'
import Toast from '@/components/PopToast.vue'
import { startTokenExpirationCheck, stopTokenExpirationCheck } from '@/utils/auth.js'

export default {
  name: 'App',
  components: {
    NavigationBar,
    ChatBot,
    BackToTop,
    Toast,
  },
  computed: {
    isAuthPage() {
      return this.$route.path === '/signup' || this.$route.path === '/signin'
    },
    isChallengePage() {
      return this.$route.path === '/challenge'
    }
  },
  mounted() {
    // 只在非认证页面启动token过期检查
    if (!this.isAuthPage) {
      startTokenExpirationCheck()
    }
  },
  beforeUnmount() {
    // 停止token过期检查
    stopTokenExpirationCheck()
  },
  watch: {
    // 监听路由变化，在认证页面和非认证页面之间切换时管理token检查
    '$route'(to) {
      const isAuthPage = to.path === '/signup' || to.path === '/signin'

      if (isAuthPage) {
        // 进入认证页面时停止检查
        stopTokenExpirationCheck()
      } else {
        // 离开认证页面时开始检查
        startTokenExpirationCheck()
      }
    }
  }
}
</script>

<style scoped>
#app {
  width: 100%;
  min-height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
}
</style>
