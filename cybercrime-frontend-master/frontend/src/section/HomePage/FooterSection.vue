<template>
  <footer class="footer-section">
    <div class="container">
      <div class="footer-content">
        <!-- 左侧列 - 公司信息 -->
        <div class="footer-column">
          <div class="company-info">
            <h3 class="company-name">Prism Sync</h3>
            <p class="company-tagline">FOSTER DIGITAL CITIZENSHIP</p>
            <div class="social-icons">
              <div class="social-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </div>

              <div class="social-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- 中间列 - 快速链接 -->
        <div class="footer-column">
          <div class="quick-links">
            <h3 class="section-title">Quick Links</h3>
            <ul class="links-list">
              <li class="link-item">
                <router-link to="/" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Home
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/link-check" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Link Check
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/library" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Library
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/challenge" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Challenge
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/community" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Community
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <!-- 右侧列 - About -->
        <div class="footer-column">
          <div class="about-section">
            <h3 class="section-title">About</h3>
            <ul class="links-list">
              <li class="link-item">
                <router-link to="/support" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Support
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/about" class="link-text">
                  <span class="arrow-icon">▶</span>
                  About Us
                </router-link>
              </li>
              <li class="link-item">
                <router-link to="/privacy-policy" class="link-text">
                  <span class="arrow-icon">▶</span>
                  Privacy Policy
                </router-link>
              </li>
            </ul>
          </div>
        </div>

      </div>

      <!-- 版权信息 -->
      <div class="footer-divider"></div>
      <div class="copyright">
        <p>COPYRIGHT @Prism Sync</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterSection'
}
</script>

<style scoped>
.footer-section {
  background-color: var(--violet-ultra-dark);
  color: white;
  padding: 3rem 0 1rem 0;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-column {
  display: flex;
  flex-direction: column;
}

/* 公司信息样式 */
.company-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: white;
  font-family: 'Inter', sans-serif;
}

.company-tagline {
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  margin-bottom: 1.5rem;
  color: var(--violet-sage);
  text-transform: uppercase;
}

.social-icons {
  display: flex;
  gap: 1rem;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: var(--violet-deep);
  border-radius: 50%;
  color: white;
  transition: all 0.3s ease;
}

.social-icon:hover {
  background-color: var(--forest-accent);
  transform: translateY(-2px);
}

/* 快速链接样式 */
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: white;
  font-family: 'Georgia', serif;
}

.links-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.links-list li {
  margin-bottom: 0.75rem;
}

.link-item {
  margin-bottom: 0.75rem;
}

.link-text {
  display: flex;
  align-items: center;
  color: var(--violet-sage);
  font-size: 0.95rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.link-text:hover {
  color: white;
}

.arrow-icon {
  font-size: 0.75rem;
  margin-right: 0.5rem;
  color: var(--forest-accent);
}



/* 分隔线和版权 */
.footer-divider {
  height: 1px;
  background-color: var(--violet-deep);
  margin: 2rem 0 1rem 0;
}

.copyright {
  text-align: center;
}

.copyright p {
  color: var(--violet-sage);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer-column {
    text-align: center;
  }

  .social-icons {
    justify-content: center;
  }


}

@media (max-width: 480px) {
  .footer-section {
    padding: 2rem 0 1rem 0;
  }

  .company-name {
    font-size: 1.75rem;
  }

  .section-title {
    font-size: 1.125rem;
  }
}
</style>
