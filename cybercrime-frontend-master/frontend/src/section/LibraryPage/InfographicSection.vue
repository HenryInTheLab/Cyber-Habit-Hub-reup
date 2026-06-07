<template>
  <section class="infographic-section">
    <!-- 修改header结构 -->
    <div class="section-header">
      <h2 class="section-title">Cybercrime Infographic</h2>
      <!-- <p class="section-description">
        Here's what happened in the past 28 days - Real-time data insights and threat analysis
      </p> -->
    </div>

    <div class="section-content">
      <!-- Financial Loss Comparison Radar Chart -->
      <!-- <RadarChart /> -->


      <!-- Financial Impact Comparison Grouped Bar Chart -->
      <GroupedBarChart />

      <!-- Cybercrime Victimization Rate Heatmap by Age Group -->
      <HeatmapChart />
    </div>
  </section>
</template>

<script>

// import RadarChart from '@/components/Visualization/Radarchart.vue'
import GroupedBarChart from '@/components/Visualization/GroupedBarChart.vue'
import HeatmapChart from '@/components/Visualization/Heatmap.vue'

export default {
  name: 'InfographicSection',
  components: {
    // RadarChart,
    GroupedBarChart,
    HeatmapChart
  },
  data() {
    return {
      // Keep loading state for child components
      loading: false
    }
  }
}
</script>

<style scoped>
.section-header {
  text-align: center;
  position: relative;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  /* margin-bottom: 0.25rem; */
}

.section-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto 2rem;
}

@media (max-width: 768px) {
  .infographic-section {
    padding: 2rem 1.5rem;
  }

  .section-title {
    font-size: 2rem;
  }
}
</style>
