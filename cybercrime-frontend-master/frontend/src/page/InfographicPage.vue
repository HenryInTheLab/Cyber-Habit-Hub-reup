<template>
  <div class="infographic-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Cybercrime Infographic</h1>
        <p class="page-subtitle">Explore real-time cybercrime data through interactive visualizations and charts</p>
      </div>
    </div>

    <div class="page-content">
      <div class="container">
        <section class="infographic-section">
          <div class="section-content">
            <div class="section-header">
              <h2 class="section-title">Cybercrime Financial Impact & Victimization Overview</h2>
              <button class="download-btn" @click="openDownloadModal">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
                </svg>
                Download Chart
              </button>
            </div>
            <div class="charts-row">
              <div class="chart-col">
            <!-- Financial Impact Comparison Grouped Bar Chart -->
                <GroupedBarChart ref="barRef" @insights="financialInsights = $event" />
              </div>
              <div class="chart-col">
            <!-- Cybercrime Victimization Rate Heatmap by Age Group -->
                <HeatmapChart ref="heatmapRef" @insights="victimInsights = $event" />
              </div>
            </div>
            <div class="data-source-shared">
              <p>Sourced from: © Commonwealth of Australia, Australian Institute of Criminology (AIC)</p>
            </div>

            <!-- Insights Section -->
            <div v-if="financialInsights || victimInsights" class="insights">
              <h3 class="insights-title">Data Insights</h3>

              <!-- Financial Impact Panel -->
              <div v-if="financialInsights" class="panel">
                <h4 class="panel-title">Key Financial Figures</h4>
                <div class="stats-grid">
                  <div class="stat-card">
                    <div class="stat-value">${{ Number(financialInsights.highestDirectLoss || 0).toLocaleString() }}M</div>
                    <div class="stat-label">Highest direct loss ({{ financialInsights.highestDirectLossCrime }})</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">${{ Number(financialInsights.highestNetLoss || 0).toLocaleString() }}M</div>
                    <div class="stat-label">Highest net loss ({{ financialInsights.highestNetLossCrime }})</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">${{ Number(financialInsights.totalRecovered || 0).toLocaleString() }}M</div>
                    <div class="stat-label">Total recovered across crimes</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">${{ Number(financialInsights.minDirectLoss || 0).toLocaleString() }}M – ${{ Number(financialInsights.maxDirectLoss || 0).toLocaleString() }}M</div>
                    <div class="stat-label">Direct loss range</div>
                  </div>
                </div>

                <h4 class="panel-title">Crime Type Characteristics</h4>
                <div class="card-grid">
                  <div class="info-card">
                    <h5>High Financial Impact</h5>
                    <ul>
                      <li>Identity theft and fraud typically cause the highest direct losses</li>
                      <li>Additional costs often exceed direct losses due to recovery efforts</li>
                      <li>Low recovery rates compound the financial burden</li>
                    </ul>
                  </div>
                  <div class="info-card">
                    <h5>Medium Financial Impact</h5>
                    <ul>
                      <li>Malware and phishing attacks show moderate financial impact</li>
                      <li>Recovery efforts may be more successful for these types</li>
                    </ul>
                  </div>
                  <div class="info-card">
                    <h5>Lower Financial Impact</h5>
                    <ul>
                      <li>Some cybercrimes have lower direct financial costs</li>
                      <li>May still incur significant indirect costs</li>
                    </ul>
                  </div>
                </div>

                <h4 class="panel-title">Key Findings</h4>
                <div class="quote-list">
                  <div class="quote-item">"Financial impact varies significantly by cybercrime type, with large spread between min and max direct loss"</div>
                  <div class="quote-item">"{{ financialInsights.highestDirectLossCrime }} and {{ financialInsights.highestNetLossCrime }} show the most severe financial burdens"</div>
                  <div class="quote-item">"Average recovery rate is around {{ financialInsights.averageRecoveryRate }}%, indicating most losses are not recovered"</div>
                </div>

                <h4 class="panel-title">Financial Protection Recommendations</h4>
                <div class="quote-list">
                  <div class="quote-item">Prevention: Invest in layered security and anti-fraud controls to reduce direct losses</div>
                  <div class="quote-item">Insurance: Consider cyber insurance to offset high-impact incidents</div>
                  <div class="quote-item">Recovery: Establish incident response and evidence collection to improve recovery odds</div>
                </div>
              </div>

              <!-- Victimization Panel -->
              <div v-if="victimInsights" class="panel">
                <h4 class="panel-title">Key Figures Summary</h4>
                <div class="stats-grid">
                  <div class="stat-card">
                    <div class="stat-value">{{ victimInsights.topAverageAge ? victimInsights.topAverageAge.avg.toFixed(1) : '0.0' }}%</div>
                    <div class="stat-label">Top average by age ({{ victimInsights.topAverageAge && victimInsights.topAverageAge.age }})</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">{{ victimInsights.topAverageCrime ? victimInsights.topAverageCrime.avg.toFixed(1) : '0.0' }}%</div>
                    <div class="stat-label">Top average by crime ({{ victimInsights.topAverageCrime && victimInsights.topAverageCrime.crime }})</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">{{ victimInsights.highestRisk ? victimInsights.highestRisk.rate.toFixed(1) : '0.0' }}%</div>
                    <div class="stat-label">Highest single rate ({{ victimInsights.highestRisk && victimInsights.highestRisk.age }})</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">{{ victimInsights.lowestRisk ? victimInsights.lowestRisk.rate.toFixed(1) : '0.0' }}%</div>
                    <div class="stat-label">Lowest single rate ({{ victimInsights.lowestRisk && victimInsights.lowestRisk.age }})</div>
                  </div>
                </div>

                <!-- Age Group Characteristics -->
                <h4 class="panel-title">Age Group Characteristics</h4>
                <div class="card-grid">
                  <div class="info-card">
                    <h5>18 – 34: High-Risk Group</h5>
                    <ul>
                      <li>Highest victimization rates across all crime types</li>
                      <li>Particularly vulnerable to online harassment and identity crime</li>
                      <li>Likely causes: More frequent online activity and social media usage</li>
                    </ul>
                  </div>
                  <div class="info-card">
                    <h5>35 – 64: Medium Risk</h5>
                    <ul>
                      <li>Relatively balanced victimization patterns</li>
                      <li>Malware and identity crime are main threats</li>
                    </ul>
                  </div>
                  <div class="info-card">
                    <h5>65+: Relatively Safer</h5>
                    <ul>
                      <li>Lowest overall victimization rates</li>
                      <li>Still need attention for fraud protection</li>
                    </ul>
                  </div>
                </div>

                <h4 class="panel-title">Key Findings</h4>
                <div class="quote-list">
                  <div class="quote-item">"Age is a strong factor of cybercrime vulnerability; {{ victimInsights.topAverageAge && victimInsights.topAverageAge.age }} shows the highest average risk"</div>
                  <div class="quote-item">"{{ victimInsights.topAverageCrime && victimInsights.topAverageCrime.crime }} has the highest average victimization rate among crime types"</div>
                  <div class="quote-item">"Peaks indicate focused prevention should target young users and high-risk crime types"</div>
                </div>

                <h4 class="panel-title">Action Recommendations</h4>
                <div class="quote-list">
                  <div class="quote-item">Young: Strengthen privacy settings and avoid oversharing on social platforms</div>
                  <div class="quote-item">Adults: Update security software regularly and identify phishing/scam patterns</div>
                  <div class="quote-item">Elderly: Improve scam awareness and verify suspicious contacts</div>
                </div>
              </div>

              <router-link to="/library" class="continue-button">
                Go to Library Section
              </router-link>



            </div>

          </div>
        </section>

        <!-- Download Modal -->
        <DownloadModal
          :is-visible="showDownloadModal"
          :bar-chart-ref="$refs.barRef"
          :heatmap-ref="$refs.heatmapRef"
          @close="closeDownloadModal"
        />
      </div>
    </div>
    <FooterSection />
  </div>
</template>

<script>

// import RadarChart from '@/components/Visualization/Radarchart.vue'
import GroupedBarChart from '@/components/Visualization/GroupedBarChart.vue'
import HeatmapChart from '@/components/Visualization/Heatmap.vue'
import DownloadModal from '@/components/DownloadModal.vue'
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'InfographicSection',
  components: {
    // RadarChart,
    GroupedBarChart,
    HeatmapChart,
    DownloadModal,
    FooterSection
  },
  data() {
    return {
      // Keep loading state for child components
      loading: false,
      financialInsights: null,
      victimInsights: null,
      showDownloadModal: false
    }
  },
  methods: {
    openDownloadModal() {
      this.showDownloadModal = true
    },

    closeDownloadModal() {
      this.showDownloadModal = false
    }
  }
}
</script>

<style scoped>
.infographic-page {
  background-color: var(--violet-light);
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

.infographic-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.download-btn {
  border: 1px solid var(--border-light);
  background: var(--violet-dark);
  color: var(--text-light);
  border-radius: 999px;
  padding: 0.6rem 1.3rem 0.6rem 0.9rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.download-btn:hover {
  background: var(--violet-deep);
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
  align-items: start;
}
.insights {
  margin-top: 1rem;
  background: var(--text-light);
}

.insights-title {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.75rem;
}

.insight-card {
  background: var(--violet-light);
  border-radius: 10px;
  padding: 1rem;
  color: var(--text-primary);
}

.insight-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 700;
}

.insight-card ul {
  margin: 0;
  padding-left: 1rem;
}

.insight-card li {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: 0.35rem;
}

/* Panels for richer sections */
.panel {
  background: var(--violet-dark);
  border-radius: 12px;
  padding: 1.25rem 1.25rem 1rem 1.25rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px var(--shadow-light);
  border: 1px solid var(--border-light);
}

.panel-title {
  margin: 0.75rem 0;
  color: var(--text-light);
  font-size: 1.1rem;
  font-weight: 700;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-card {
  background: var(--violet-light);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  text-align: center;
  border: 1px solid var(--border-light);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px var(--shadow-light);
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 0.3px;
}

.stat-label {
  margin-top: 0.25rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.quote-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.quote-item {
  background: var(--text-light);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 0.8rem 1rem;
  color: var(--text-secondary);
  position: relative;
}

@media (min-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Info card grid for Characteristics sections */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.info-card {
  background: var(--text-light);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.info-card h5 {
  margin: 0 0 0.5rem 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
}

.info-card ul {
  margin: 0;
  padding-left: 1.2rem;
}

.info-card li {
  color: var(--violet-deep);
  margin-bottom: 0.5rem;
}

.chart-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.data-source-shared {
  text-align: center;
  padding: 0.75rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-style: italic;
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

  .infographic-section {
    padding: 0;
  }

  .charts-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
