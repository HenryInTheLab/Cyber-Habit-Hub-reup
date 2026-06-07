<template>
  <div class="library-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Educational Library</h1>
        <p class="page-subtitle">
          Access cybersecurity videos, articles, and infographics to enhance your digital safety knowledge
        </p>
      </div>
    </div>

    <div class="page-content">
      <div class="container">
        <ResourceSection />

        <!-- Continue Button -->
        <router-link to="/challenge" class="continue-button">
          Continue to Challenge Section
        </router-link>
      </div>
    </div>

    <FooterSection />
  </div>
</template>


<script>
import ResourceSection from '../section/LibraryPage/ResourceSection.vue'
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'LibraryPage',
  components: {
    ResourceSection,
    FooterSection
  }
}
</script>

<style scoped>
.library-page {
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
  padding: 0 8rem;
}

.continue-button {
  display: block;
  width: fit-content;
  margin: 2rem auto 3rem auto; /* ensure it's visible and balanced */
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
