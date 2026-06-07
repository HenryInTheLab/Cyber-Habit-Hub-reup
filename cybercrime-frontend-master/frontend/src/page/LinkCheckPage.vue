<template>
  <div class="link-check-page">
    <div class="page-content">
      <div class="container">
        <LinkSafetySection />

        <!-- Continue Button -->
        <router-link to="/library" class="continue-button">
          Continue to Library Page
        </router-link>
      </div>
    </div>
    <FooterSection />
  </div>
</template>

<script>
import LinkSafetySection from '../section/LinkCheckPage/LinkSafetySection.vue'
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'LinkCheckPage',
  components: {
    LinkSafetySection,
    FooterSection
  }
}
</script>

<style scoped>
.page-content {
  padding: 0;
}

.continue-button {
  display: block;
  width: fit-content;
  margin: 2rem auto;
  padding: 1rem 2rem;
  background: var(--violet-deep);
  color: var(--violet-light);
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 12px var(--shadow-dark);
}

.continue-button:hover {
  background: var(--violet-dark);
}

.container {
  max-width: 2000px;
  margin: 0 auto;
  padding: 0 2rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
}
</style>

