<template>
  <div class="community-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Community</h1>
        <p class="page-subtitle">Connect with fellow cybersecurity enthusiasts, compete in challenges, and climb the leaderboard</p>
      </div>
    </div>

    <div class="page-content">
      <div class="container">
        <div class="community-grid">
          <div class="leaderboard-section">
            <LeaderboardSection />
          </div>
        </div>
      </div>

      <router-link to="/library" class="continue-button">
        Go to Library Section
      </router-link>
    </div>
    <FooterSection />
  </div>
</template>

<script>
import LeaderboardSection from '../section/CommunityPage/LeaderboardSection.vue'
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'CommunityPage',
  components: {
    LeaderboardSection,
    FooterSection
  }
}
</script>

<style scoped>
.community-page {
  background-color: var(--violet-light);
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
  max-width: 1000px;
  margin: 0 auto;
}

.page-content {
  padding: 4rem 0;
}

.container {
  max-width: 100%;
  margin: 0 auto;
}

.community-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.leaderboard-section {
  order: 1;
}

.continue-button {
  display: block;
  width: fit-content;
  margin: 2rem auto 3rem auto;
  padding: 1rem 2rem;
  background: var(--violet-deep);
  color: var(--violet-light);
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 12px var(--shadow-dark);
}

.continue-button:hover {
  background: var(--violet-dark);
  transform: translateY(-2px);
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

  .community-grid {
    gap: 1.5rem;
  }
}
</style>
