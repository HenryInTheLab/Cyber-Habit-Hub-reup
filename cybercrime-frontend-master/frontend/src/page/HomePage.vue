<template>
  <div class="home-page">
    <HeroSection
      :isAuthenticated="isAuthenticated"
      :loading="loading"
      @sign-in="signIn"
    />

    <LinkCheckSection />

    <ExploreLibrarySection />

    <ExploreChallengeSection />

    <FooterSection />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HomeHeroSection from '@/section/HomePage/HomeHeroSection.vue'
import LinkCheckSection from '@/section/HomePage/ExploreLinkSection.vue'
import ExploreLibrarySection from '@/section/HomePage/ExploreLibrarySection.vue'
import ExploreChallengeSection from '@/section/HomePage/ExploreChallengeSection.vue'
import FooterSection from '@/section/HomePage/FooterSection.vue'

export default {
  name: 'HomePage',
  components: {
    HeroSection: HomeHeroSection,
    LinkCheckSection,
    ExploreLibrarySection,
    ExploreChallengeSection,
    FooterSection,
  },
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)
    const loading = ref(false)

    const signIn = () => {
      router.push('/signin')
    }

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

    onMounted(() => {
      checkAuthStatus()
    })

    return {
      isAuthenticated,
      loading,
      signIn,
    }
  },
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

</style>
