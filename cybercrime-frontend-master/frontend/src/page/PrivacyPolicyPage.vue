<template>
  <div class="privacy-page">
    <div class="page-content">
      <div class="page-header">
        <div class="container">
          <h1 class="page-title">Privacy Policy</h1>
          <p class="page-subtitle">Your privacy is our priority - learn how we protect your data</p>
        </div>
      </div>

      <div class="container">
        <div class="page-body">
          <div class="privacy-section">
            <h2>Privacy Policy - CyberHabit Hub</h2>
            <p class="last-updated">Last updated: October 6, 2025</p>
            <p>Hey there! We know privacy policies can be boring, so we'll keep this short and sweet.</p>
          </div>

          <div class="privacy-section">
            <h2>What We Do</h2>
            <p>Our URL safety checker helps you stay safe online by analyzing links for malware, phishing attempts, and suspicious content before you click them. We also have a login system and community features to enhance your experience!</p>
          </div>

          <div class="privacy-section">
            <h2>What We DON'T Collect</h2>
            <p>Zero. Zilch. Nada.</p>
            <p>We don't collect, store, or track any of your personal information. That means:</p>
            <ul>
              <li>❌ No names, emails, or phone numbers</li>
              <li>❌ No passwords or personal credentials</li>
              <li>❌ No browsing history</li>
              <li>❌ No location data</li>
              <li>❌ No cookies or tracking pixels</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Login System</h2>
            <p>Our login system is built on Google Authenticator technology, but here's the cool part:</p>
            <ul>
              <li>Your username is auto-generated (no personal info needed!)</li>
              <li>We don't store any Google account details</li>
              <li>Authentication happens through secure tokens only</li>
              <li>You stay completely anonymous while still having a personalized experience</li>
            </ul>
            <p>Think of it like having a secret code name that only you know!</p>
          </div>

          <div class="privacy-section">
            <h2>Community System</h2>
            <p>Our community features let you connect with other safety-conscious users:</p>
            <ul>
              <li><strong>Your choice:</strong> You can choose whether to show your progress publicly or keep it private</li>
              <li><strong>What others see:</strong> Other users can only see progress stats you've chosen to share</li>
              <li><strong>What we store:</strong> Just anonymous progress data (like "User ABC checked 50 links this week")</li>
              <li><strong>No personal details:</strong> Your auto-generated username is the only identifier</li>
            </ul>
            <p>It's like a leaderboard where everyone has cool codenames instead of real names!</p>
          </div>

          <div class="privacy-section">
            <h2>What Happens to Your URLs</h2>
            <p>When you check a URL:</p>
            <ol>
              <li>We analyze it in real-time for safety</li>
              <li>We give you the results</li>
              <li>We forget about it completely</li>
            </ol>
            <p>Your URLs are processed temporarily just to check if they're safe, then immediately discarded. We don't store them anywhere.</p>
          </div>

          <div class="privacy-section">
            <h2>Progress Data</h2>
            <p>If you choose to participate in the community:</p>
            <ul>
              <li>We track anonymous usage stats (number of links checked, safety score, etc.)</li>
              <li>This data is tied only to your auto-generated username</li>
              <li>You control what's visible to others</li>
              <li>No personal information is ever connected to this data</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>How We Keep You Safe</h2>
            <p>We use industry-standard security measures to protect our service, but since we don't collect your personal data anyway, there's nothing personal to protect!</p>
          </div>

          <div class="privacy-section">
            <h2>Third Parties</h2>
            <p>We don't share anything with third parties because, well, we don't have anything personal to share. The Google Authenticator integration only handles authentication tokens - no personal Google data touches our servers.</p>
          </div>

          <div class="privacy-section">
            <h2>Your Control</h2>
            <p>You're in the driver's seat:</p>
            <ul>
              <li>Choose your privacy level in the community</li>
              <li>Hide or show your progress anytime</li>
              <li>Use the service completely anonymously</li>
              <li>No account deletion needed (there's nothing personal to delete!)</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Changes to This Policy</h2>
            <p>If we ever change this policy, we'll update the date at the top and let the community know.</p>
          </div>

          <div class="privacy-section">
            <h2>Questions?</h2>
            <p>Got questions about our privacy practices? Feel free to reach out - though honestly, there's still not much to explain since we literally collect nothing personal!</p>
          </div>

          <div class="privacy-section quote">
            <h2>Quick Summary</h2>
            <p><strong>We check if your links are safe, give you an anonymous login, let you join our community with zero personal info, and forget everything except the progress stats you choose to share. Your privacy = still 100% protected.</strong></p>
          </div>
        </div>
      </div>
    </div>
    <FooterSection />
  </div>
</template>

<script>
import FooterSection from '../section/HomePage/FooterSection.vue'
import { onMounted } from 'vue'

export default {
  name: 'PrivacyPolicyPage',
  components: {
    FooterSection
  },
  setup() {
    // 页面加载时滚动到顶部
    onMounted(() => {
      window.scrollTo(0, 0)
    })
  }
}
</script>

<style scoped>
.privacy-page {
  background: var(--violet-dark);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-body {
  background: var(--violet-light);
  border-radius: 12px;
  padding: 3rem;
  margin-bottom: 4rem;
}

.privacy-section {
  padding: 2rem 2rem 1rem;
}

.privacy-section h2 {
  color: var(--text-primary);
  font-size: 2rem;
  font-weight: 600;
  border-bottom: 3px solid var(--border-medium);
  margin-bottom: 1.5rem;
}

.privacy-section p {
  color: var(--text-secondary);
  font-size: 1.25rem;
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.last-updated {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-style: italic;
  margin: 0 0 2rem 0;
}

.privacy-section ul,
.privacy-section ol {
  margin: 1rem 0;
  padding-left: 1.5rem;
  color: var(--text-secondary);
}

.privacy-section ul li,
.privacy-section ol li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.quote {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
}

.quote h2 {
  border-bottom: none;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .privacy-section {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 2.5rem;
  }

  .page-subtitle {
    font-size: 1.1rem;
  }
}
</style>

