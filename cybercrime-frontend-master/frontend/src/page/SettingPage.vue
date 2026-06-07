<template>
  <div class="settings-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Settings</h1>
        <p class="page-subtitle">Manage your account settings and privacy preferences</p>
      </div>
    </div>

    <div class="page-content">
      <div class="container">
        <TeamInfoSection />
        <PrivacySettingSection />
      </div>
    </div>
  </div>
</template>

<script>
import PrivacySettingSection from '../section/SettingPage/PrivacySettingSection.vue'
import TeamInfoSection from '../section/SettingPage/TeamInfoSection.vue'

export default {
  name: 'SettingPage',
  components: {
    PrivacySettingSection,
    TeamInfoSection
  }
}
</script>

<style scoped>
.settings-page {
  background: var(--bg-primary);
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
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
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
