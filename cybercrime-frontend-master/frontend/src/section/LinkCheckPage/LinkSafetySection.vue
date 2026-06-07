<template>
  <section class="link-safety-section">
    <div class="main-container">
      <div class="background-pattern"></div>

      <div class="main-card">
        <div v-if="!results && !error" class="card-content">
          <p class="top-text">Stay safe from suspicious links</p>
          <h1 class="main-title">Is This Link Really Safe?</h1>
          <p class="description">Instantly analyze any link for malware, phishing attempts, and suspicious content.</p>

          <div class="input-button-row">
            <div class="input-container">
              <input
                v-model="inputUrl"
                type="url"
                placeholder="https://example-url.com"
                class="url-input"
                @keyup.enter="checkUrlSafety"
                :disabled="isLoading"
              />
            </div>
            <button
              class="check-button"
              @click="checkUrlSafety"
              :disabled="isLoading || !inputUrl.trim()"
            >
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ isLoading ? 'Checking...' : 'Check URL' }}
            </button>
          </div>

          <p class="footer-text">
            Add your link or paste it from the device's clipboard. Your data is processed by our
            <router-link to="/privacy-policy" class="privacy-link">privacy policy.</router-link>
          </p>
        </div>

        <div v-if="error" class="error-content">
          <div class="error-message">
            <span class="error-icon">⚠️</span>
            {{ error }}
          </div>
          <button @click="resetForm" class="check-button">Check Another URL</button>
        </div>

        <div v-if="results && !error" class="results-content">
          <!-- 输入的URL显示 -->
          <div class="url-display">
            <p>{{ inputUrl }}</p>
          </div>



          <!-- 居中的结果标题与风险徽章（Hero 区域） -->
          <div class="result-hero">
            <h2 class="hero-title">{{ results.is_safe ? 'Safe' : 'Unsafe' }}</h2>

          </div>

          <!-- 分析说明横幅 -->
          <div class="analysis-banner" :class="results.is_safe ? 'safe' : 'unsafe'">
            <p class="analysis-text">{{ results.analysis || getAnalysisText() }}</p>
            <!-- 将可疑模式嵌入横幅内部，仅在不安全时显示 -->
            <div v-if="!results.is_safe && results.suspicious_patterns?.length" class="threats-list">
              <h4 class="threats-title">Suspicious Patterns Detected</h4>
              <div class="threat-items">
                <div v-for="pattern in results.suspicious_patterns" :key="pattern" class="threat-item">
                  {{ pattern }}
                </div>
              </div>
            </div>
          </div>

          <!-- 域名详情卡片：Domain / Registrar / Name Servers -->
          <div class="domain-card">
            <div class="details-grid">
              <div v-if="results.details?.domain_name" class="details-item">
                <span class="details-label">Domain</span>
                <span class="details-value">{{ results.details.domain_name }}</span>
              </div>
              <div v-if="results.details?.registrar" class="details-item">
                <span class="details-label">Registrar</span>
                <span class="details-value">{{ results.details.registrar }}</span>
              </div>
            </div>

            <div v-if="results.details?.name_servers?.length" class="nameservers">
              <span class="details-label">Name Servers</span>
              <div class="ns-list">
                <span v-for="ns in results.details.name_servers" :key="ns" class="ns-pill">{{ ns }}</span>
              </div>
            </div>

            <div v-if="results.blacklisted !== undefined" class="blk-row">
              <span class="details-label">Blacklisted</span>
              <span :class="results.blacklisted ? 'text-danger' : 'text-success'">
                {{ results.blacklisted ? 'Yes' : 'No' }}
              </span>
            </div>
          </div>



          <!-- 简化的威胁列表 -->
          <div v-if="results.matches?.length" class="threats-list">
            <h4 class="threats-title">Security Threats</h4>
            <div class="threat-items">
              <div v-for="match in results.matches" :key="match.threatType" class="threat-item">
                {{ match.threatType }}
              </div>
            </div>
          </div>
          <div class="actions-row">
            <button @click="resetForm" class="check-button">Check Another URL</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'LinkSafetySection',
  data() {
    return {
      inputUrl: '',
      results: null,
      isLoading: false,
      error: null
    }
  },
  methods: {
    async checkUrlSafety() {
      if (!this.inputUrl.trim()) {
        this.error = 'Please enter a valid URL format (e.g., https://example.com)';
        return;
      }

      try {
        new URL(this.inputUrl.trim());
      } catch {
        this.error = 'Please enter a valid URL format (e.g., https://example.com)';
        return;
      }

      this.isLoading = true;
      this.error = null;
      this.results = null;

      try {
        const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/validate/', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': 'DBAoITRog95H98YQPPDR93kkNCX1ZCfwB8nTPSBX2H16EY3osrdZ6lUoH2dxQniA'
          },
          body: JSON.stringify({ url: this.inputUrl.trim() })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        this.results = await response.json();
      } catch {
        this.error = 'Please enter a valid URL format (e.g., https://example.com)';
      } finally {
        this.isLoading = false;
      }
    },

    getRiskLevel() {
      if (!this.results) return 'Unknown';
      // 优先使用后端返回的risk_level
      if (this.results.risk_level) return this.results.risk_level;
      // 降级到原有的逻辑
      if (this.results.blacklisted) return 'High';
      if (!this.results.is_safe) return 'Medium';
      if (this.results.matches?.length) return 'Low-Medium';
      return 'Low';
    },

    getAnalysisText() {
      if (!this.results) return 'No analysis available';
      // 优先使用后端返回的analysis
      if (this.results.analysis) return this.results.analysis;
      // 降级到原有的逻辑
      if (this.results.blacklisted) return 'This URL is blacklisted and should be avoided.';
      if (!this.results.is_safe) return 'This URL has been flagged as potentially unsafe. Exercise caution when visiting.';
      if (this.results.matches?.length) return `URL matched security database entries. Review carefully before proceeding.`;
      return 'This URL appears to be safe based on our analysis.';
    },

    resetForm() {
      this.results = null;
      this.error = null;
      this.inputUrl = '';
    }
  }
}
</script>

<style scoped>
.link-safety-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 2rem 1rem 2rem;
  min-height: 0vh;
}

.main-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin: 6vh auto 2rem auto;
  min-height: 50vh;
}

.background-pattern {
  height: 50vh;
  background: var(--violet-dark);
  border-radius: 24px;
  width: 100%;
}

.main-card {
  position: relative;
  z-index: 2;
  background: var(--violet-light);
  border-radius: 24px;
  padding: 2rem;
  max-width: 900px;
  width: calc(100% - 4rem);
  box-shadow: 0 12px 40px var(--shadow-dark);
  text-align: center;
  margin: -40vh auto 2rem auto;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.top-text {
  font-size: 1.125rem;
  color: var(--violet-medium);
  margin: 0;
  font-weight: 500;
}

.main-title {
  font-size: 2.75rem;
  font-weight: 700;
  color: var(--violet-deep);
  margin: 0;
  line-height: 1.2;
}

.description {
  font-size: 1.25rem;
  color: var(--violet-dark);
  margin: 0 auto;
  max-width: 1000px;
  line-height: 1.5;
}

.input-button-row {
  display: flex;
  gap: 1rem;
  align-items: stretch;
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
}

.input-container {
  position: relative;
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
}

.url-input {
  width: 100%;
  min-width: 0;
  padding: 1rem 1.25rem;
  border: 2px solid var(--violet-sage);
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.3s ease;
}

.url-input:focus {
  outline: none;
  border-color: var(--violet-deep);
}

.url-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}



.check-button {
  padding: 1rem 2rem;
  background: var(--violet-deep);
  color: var(--violet-light);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 140px;
  max-width: 200px;
  justify-content: center;
}

.check-button:hover:not(:disabled) {
  background: var(--violet-dark);
}

.check-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Center the action button within results/error sections */
.results-content .check-button,
.error-content .check-button {
  margin-left: auto;
  margin-right: auto;
}

.footer-text {
  font-size: 0.875rem;
  color: var(--violet-medium);
  margin: 0;
  line-height: 1.4;
}

.privacy-link {
  color: var(--violet-deep);
  text-decoration: none;
  font-weight: 500;
}

.privacy-link:hover {
  text-decoration: underline;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-content, .results-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 结果区域 - 参考图2的布局 */
.result-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.hero-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--violet-deep);
  margin: 0;
}

.analysis-banner {
  background: #eef9f1;
  border-radius: 12px;
  padding: 1.5rem 2rem;
}

.analysis-banner.safe {
  background: #ecfdf5; /* green-50 */ /* green-500 */
}

.analysis-banner.unsafe {
  background: #fef2f2; /* red-50 */ /* red-500 */
}

.analysis-text {
  margin: 0;
  font-weight: 600;
}

.analysis-banner.safe .analysis-text { color: #065f46; }
.analysis-banner.unsafe .analysis-text { color: #7f1d1d; }

.actions-row {
  display: flex;
  justify-content: center;
}

.error-message {
  background: var(--violet-light);
  color: var(--violet-deep);
  padding: 1rem 1.25rem;
  border-radius: 12px;
  border: 2px solid var(--violet-sage);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 20px var(--shadow-medium);
}

.error-icon {
  font-size: 1.2rem;
}


/* 新的results样式 - 保留 */
.url-display {
  text-align: center;
}

.url-display p {
  color: var(--violet-dark);
  word-break: break-all;
  font-size: 1.2rem;
  font-weight: 700;
  display: inline-block;
  border-bottom: 2px solid var(--violet-sage);
}

/* Domain details card */
.domain-card {
  background: transparent;
  border-radius: 12px;
  padding: 0;
  box-shadow: none;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.details-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.9rem 1.1rem;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid var(--violet-sage);
  min-height: 56px;
}

.details-label {
  font-weight: 600;
  color: var(--violet-medium);
}

.details-value {
  color: var(--violet-deep);
  font-weight: 700;
  letter-spacing: 0.2px;
}

.nameservers {
  margin-top: 1rem;
}

.ns-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
  justify-content: center;
  align-items: center;
}

.nameservers .details-label {
  display: block;
  text-align: center;
  margin-bottom: 0.5rem;
}

.ns-pill {
  background: rgba(16, 24, 40, 0.06);
  color: var(--violet-deep);
  padding: 0.35rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  border: 1px solid var(--violet-sage);
}

.blk-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid var(--violet-sage);
}

.info-list {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: var(--violet-dark);
}

.info-value {
  color: var(--text-primary);
}

.text-danger {
  color: #dc2626;
  font-weight: 600;
}

.text-success {
  color: var(--violet-ultra-dark);
  font-weight: 600;
}

.threats-list {
  background: #fee2e2; /* slightly deeper red */
  border: 1px solid #fca5a5; /* slightly deeper border */
  box-shadow: none;
  margin: 1rem 0 0 0;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

.threats-title {
  font-size: 1rem;
  font-weight: 700;
  color: #7f1d1d;
  margin: 0;
  text-align: left;
  white-space: nowrap;
}

.threat-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.threat-item {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
  padding: 0.4rem 0.9rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .link-safety-section {
    padding: 1rem;
  }

  .main-card {
    padding: 2rem 1.5rem;
  }

  .main-title {
    font-size: 2rem;
  }

  .description {
    font-size: 1.125rem;
  }

  .input-button-row {
    flex-direction: column;
    width: 100%;
  }

  .input-container {
    width: 100%;
  }

  .check-button {
    min-width: auto;
    width: 100%;
    max-width: none;
  }

  .background-pattern {
    height: 75vh;
  }

  .result-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .background-pattern {
    height: 80vh;
  }

  .main-card {
    padding: 1.5rem 1rem;
    margin-top: -1rem;
  }

  .main-title {
    font-size: 1.75rem;
  }
}
</style>
