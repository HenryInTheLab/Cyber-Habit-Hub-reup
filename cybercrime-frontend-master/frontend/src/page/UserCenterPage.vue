<template>
  <div class="user-center">
    <UserInfoSection />
    <TestHistorySection />
  </div>
</template>

<script>
import UserInfoSection from '../section/UserCenterPage/UserInfoSection.vue'
import TestHistorySection from '../section/UserCenterPage/TestHistorySection.vue'

export default {
  name: 'UserCenterPage',
  components: {
    UserInfoSection,
    TestHistorySection
  }
}
</script>

<style scoped>
.user-center {
  min-height: 90vh;
}
</style>
