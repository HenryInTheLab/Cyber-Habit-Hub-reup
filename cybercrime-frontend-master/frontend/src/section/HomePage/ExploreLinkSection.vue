<template>
  <div id="link-check-section" class="link-check-section">
    <div class="section-container">
      <div class="content-wrapper">
        <div class="text-content">
          <div class="title-section">
            <h2 class="card-title">Link Security Check</h2>
            <p class="description">
              Check the security of suspicious links to avoid phishing attacks and protect yourself from malicious websites, identity theft, and financial fraud. Our advanced scanning technology analyzes URLs in real-time to detect potential threats before you click.
            </p>
          </div>
        </div>

        <div class="features-section">
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon-wrapper">
                <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="13,2 3,14 12,14 11,22 21,10 12,10"></polygon>
                </svg>
              </div>
              <div class="feature-content">
                <h3 class="feature-title">Real-time Detection</h3>
                <p class="feature-desc">Instant analysis of suspicious URLs</p>
              </div>
            </div>

            <div class="feature-card">
              <div class="feature-icon-wrapper">
                <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <circle cx="12" cy="16" r="1"></circle>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <div class="feature-content">
                <h3 class="feature-title">Multiple Security Checks</h3>
                <p class="feature-desc">Comprehensive threat analysis</p>
              </div>
            </div>

            <div class="feature-card">
              <div class="feature-icon-wrapper">
                <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <div class="feature-content">
                <h3 class="feature-title">Privacy Protection</h3>
                <p class="feature-desc">Your data stays secure and private</p>
              </div>
            </div>
          </div>

          <div class="cta-section">
            <router-link to="/link-check" class="browse-button" @click="scrollToTop">
              Check Now
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExploreLinkSection',
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}
</script>

<style scoped>
.link-check-section {
  padding: 4rem 0;
  background: var(--bg-primary);
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
}

.title-section {
  margin-bottom: 2rem;
}

.card-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--violet-dark);
  margin: 0 0 1rem 0;
}

.description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.features-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 550px;
  margin: 0 auto;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}

.feature-icon-wrapper {
  width: 48px;
  height: 48px;
  background: var(--violet-deep);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--violet-dark);
  margin: 0 0 0.5rem 0;
}

.feature-desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

.cta-section {
  display: flex;
  justify-content: center;
}

.browse-button {
  display: inline-block;
  background: var(--violet-dark);
  color: var(--text-light);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
}

.browse-button:hover {
  background: var(--violet-deep);
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .text-content {
    padding-right: 0;
    text-align: center;
  }

  .card-title {
    font-size: 2rem;
  }

  .browse-button {
    padding: 10px 20px;
  }
}
</style>
