<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Download Charts</h3>
        <button @click="closeModal" class="close-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="download-options">
          <div class="option-group">
            <h4>Select Charts to Download:</h4>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input
                  type="checkbox"
                  v-model="selectedCharts.barChart"
                  :disabled="!barChartAvailable"
                  @change="handleIndividualChartChange('barChart')"
                >
                <span class="checkmark"></span>
                <span class="label-text">Financial Impact Chart</span>
              </label>

              <label class="checkbox-item">
                <input
                  type="checkbox"
                  v-model="selectedCharts.heatmap"
                  :disabled="!heatmapAvailable"
                  @change="handleIndividualChartChange('heatmap')"
                >
                <span class="checkmark"></span>
                <span class="label-text">Victimization Rate Heatmap</span>
              </label>

              <label class="checkbox-item">
                <input
                  type="checkbox"
                  v-model="selectedCharts.both"
                  @change="handleBothChartsChange"
                >
                <span class="checkmark"></span>
                <span class="label-text">Both Charts</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button @click="closeModal" class="cancel-btn">Cancel</button>
        <button
          @click="handleDownload"
          class="download-btn"
          :disabled="!hasSelection"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
          </svg>
          Download Selected
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'DownloadModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    barChartRef: {
      type: Object,
      default: null
    },
    heatmapRef: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const selectedCharts = ref({
      barChart: false,
      heatmap: false,
      both: false
    })

    const barChartAvailable = computed(() => {
      return props.barChartRef && props.barChartRef.getImageDataURL
    })

    const heatmapAvailable = computed(() => {
      return props.heatmapRef && props.heatmapRef.getImageDataURL
    })

    const hasSelection = computed(() => {
      return selectedCharts.value.barChart ||
             selectedCharts.value.heatmap ||
             selectedCharts.value.both
    })

    const handleBothChartsChange = () => {
      if (selectedCharts.value.both) {
        selectedCharts.value.barChart = true
        selectedCharts.value.heatmap = true
      } else {
        selectedCharts.value.barChart = false
        selectedCharts.value.heatmap = false
      }
    }

    const handleIndividualChartChange = (chartType) => {
      // If user unchecks one chart while "both" is selected, uncheck "both"
      if (selectedCharts.value.both && !selectedCharts.value[chartType]) {
        selectedCharts.value.both = false
      }
    }

    const handleDownload = async () => {
      try {
        const downloads = []

        if (selectedCharts.value.both || selectedCharts.value.barChart) {
          if (barChartAvailable.value) {
            const barChartDataURL = props.barChartRef.getImageDataURL({
              type: 'png'
            })
            if (barChartDataURL) {
              downloads.push({
                dataURL: barChartDataURL,
                filename: 'financial-impact-chart.png'
              })
            }
          }
        }

        if (selectedCharts.value.both || selectedCharts.value.heatmap) {
          if (heatmapAvailable.value) {
            const heatmapDataURL = props.heatmapRef.getImageDataURL({
              type: 'png'
            })
            if (heatmapDataURL) {
              downloads.push({
                dataURL: heatmapDataURL,
                filename: 'victimization-heatmap.png'
              })
            }
          }
        }

        // Download files
        for (const download of downloads) {
          const link = document.createElement('a')
          link.download = download.filename
          link.href = download.dataURL
          link.click()
        }

        // Close modal after successful download
        closeModal()

      } catch (error) {
        console.error('Download failed:', error)
        alert('Download failed. Please try again.')
      }
    }

    const closeModal = () => {
      // Reset selections
      selectedCharts.value = {
        barChart: false,
        heatmap: false,
        both: false
      }
      emit('close')
    }

    // Watch for individual chart selections to update "both" checkbox
    watch([() => selectedCharts.value.barChart, () => selectedCharts.value.heatmap],
      ([barChart, heatmap]) => {
        // Only auto-check "both" if both individual charts are selected
        if (barChart && heatmap) {
          selectedCharts.value.both = true
        }
      }
    )

    return {
      selectedCharts,
      barChartAvailable,
      heatmapAvailable,
      hasSelection,
      handleBothChartsChange,
      handleIndividualChartChange,
      handleDownload,
      closeModal
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--text-light);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.download-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-group h4 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.checkbox-item:hover {
  background: var(--violet-light);
}

.checkbox-item input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-light);
  border-radius: 3px;
  position: relative;
  transition: all 0.2s ease;
}

.checkbox-item input[type="checkbox"]:checked + .checkmark {
  background: var(--violet-dark);
  border-color: var(--violet-dark);
}

.checkbox-item input[type="checkbox"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.label-text {
  font-size: 0.95rem;
  color: var(--text-primary);
  font-weight: 500;
}

.checkbox-item:has(input:disabled) .label-text {
  color: var(--text-secondary);
  opacity: 0.6;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-light);
}

.cancel-btn,
.download-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: var(--text-light);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.cancel-btn:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

.download-btn {
  background: var(--violet-dark);
  color: white;
  border: none;
  box-shadow: 0 2px 8px var(--shadow-light);
}

.download-btn:hover:not(:disabled) {
  background: var(--violet-ultra-dark);
}

.download-btn:disabled {
  background: var(--violet-sage);
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 768px) {
  .modal-content {
    margin: 1rem;
    max-width: none;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
}
</style>
