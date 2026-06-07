<template>
  <div class="heatmap-section">


    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading data...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h4>Data Loading Failed</h4>
      <p>Unable to fetch data, please try again later</p>
      <button @click="fetchData" class="retry-btn">Retry</button>
    </div>

    <div v-else class="content">
      <!-- Main ECharts Visualization -->
      <div class="chart-container">
        <div ref="chartRef" class="main-chart"></div>
      </div>


    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'HeatmapChart',
  emits: ['insights'],
  props: {
    data: {
      type: Array,
      default: () => []
    },
    autoFetch: {
      type: Boolean,
      default: true
    }
  },
  setup(props, { emit, expose }) {
    const chartRef = ref(null)
    const chartInstance = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const chartData = ref(null)
    const insights = ref(null)

    // 数据处理函数
    const processHeatmapData = (rawData) => {
      if (!rawData || !Array.isArray(rawData) || rawData.length === 0) {
        return { ageGroups: [], crimeTypes: [], dataMatrix: [], maxValue: 0 }
      }

      const ageGroups = ['18 – 34', '35 – 64', '65+', 'All ages']
      const crimeTypes = [
        'Malware',
        'Identity crime and misuse',
        'Fraud and scams',
        'Online abuse and harassment',
        'Any cybercrime (all)'
      ]

      const dataMatrix = []

      ageGroups.forEach((age, ageIndex) => {
        crimeTypes.forEach((crime, crimeIndex) => {
          const dataPoint = rawData.find(item =>
            item &&
            item.age === age &&
            item.main_type === crime &&
            item.prevalence_2024 !== undefined &&
            item.prevalence_2024 !== null
          )

          const value = dataPoint ? parseFloat(dataPoint.prevalence_2024) : 0
          const validValue = isNaN(value) ? 0 : Math.max(0, value)

          dataMatrix.push([crimeIndex, ageIndex, validValue])
        })
      })

      const maxValue = Math.max(...dataMatrix.map(item => item[2]), 0)
      return { ageGroups, crimeTypes, dataMatrix, maxValue }
    }

    // ECharts配置生成
    const createHeatmapOption = (processedData) => {
      const { ageGroups, crimeTypes, dataMatrix, maxValue } = processedData

      return {
        tooltip: {
          show: false
        },

        grid: {
          left: '5%',
          right: '10%',
          top: '15%',
          bottom: '10%',
          containLabel: true
        },

        xAxis: {
          type: 'category',
          data: crimeTypes.slice(),
          axisLabel: {
            fontSize: 11,
            color: '#34495e',
            interval: 0,
            rotate: 0,
            formatter: function(value) {
              if (!value) return ''
              if (value.length > 12) {
                const words = value.split(' ')
                if (words.length > 1) {
                  const mid = Math.ceil(words.length / 2)
                  return words.slice(0, mid).join(' ') + '\n' + words.slice(mid).join(' ')
                }
              }
              return value
            }
          },
          splitArea: { show: true },
          axisLine: { lineStyle: { color: '#bdc3c7' } },
          axisTick: { lineStyle: { color: '#bdc3c7' } }
        },

        yAxis: {
          type: 'category',
          data: ageGroups.slice(),
          axisLabel: {
            fontSize: 12,
            color: '#34495e',
            fontWeight: 'bold'
          },
          splitArea: { show: true },
          axisLine: { lineStyle: { color: '#bdc3c7' } },
          axisTick: { lineStyle: { color: '#bdc3c7' } }
        },

        visualMap: {
          min: 0,
          max: Math.max(maxValue, 1),
          calculable: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          itemWidth: 20,
          itemHeight: 140,
          textStyle: { color: '#34495e', fontSize: 11 },
          inRange: {
            color: [
              '#ffffff', '#f0f4ff', '#e1ecff', '#c7d9ff',
              '#a8c8ff', '#7db3ff', '#5299ff', '#2d66cc', '#1a3d99'
            ]
          }
        },

        series: [{
          name: 'Victimization Rate',
          type: 'heatmap',
          data: dataMatrix,
          label: {
            show: true,
            fontSize: 10,
            fontWeight: 'bold',
            color: '#000000',
            formatter: function(params) {
              if (!params || !params.value || !Array.isArray(params.value) || params.value.length < 3) {
                return '0%'
              }
              const value = params.value[2]
              return value > 0 ? `${value.toFixed(1)}%` : '0%'
            }
          },
          itemStyle: {
            borderColor: 'transparent',
            borderWidth: 0
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0,0,0,0.3)',
              borderColor: 'transparent'
            }
          }
        }]
      }
    }

    // 图表初始化
    const initHeatmapChart = async (rawData) => {
      if (!chartRef.value || !rawData) {
        return
      }

      try {
        const processedData = processHeatmapData(rawData)

        if (!processedData || !processedData.dataMatrix || !processedData.dataMatrix.length) {
          return
        }

        const container = chartRef.value
        if (container.offsetWidth === 0 || container.offsetHeight === 0) {
          setTimeout(() => initHeatmapChart(rawData), 100)
          return
        }

        if (chartInstance.value) {
          chartInstance.value.dispose()
          chartInstance.value = null
        }

        await nextTick()

        chartInstance.value = echarts.init(container, null, {
          renderer: 'canvas',
          useDirtyRect: false,
          width: container.offsetWidth,
          height: container.offsetHeight
        })

        const option = createHeatmapOption(processedData)
        chartInstance.value.setOption(option, {
          notMerge: true,
          replaceMerge: ['series'],
          silent: true
        })

        insights.value = generateHeatmapInsights(processedData)
        emit('insights', insights.value)

      } catch (error) {
        console.error('Error initializing chart:', error)
        error.value = 'Chart initialization failed: ' + error.message
      }
    }

    // 导出图表为图片
    const getImageDataURL = (opts = {}) => {
      if (!chartInstance.value) return null
      try {
        return chartInstance.value.getDataURL({
          type: 'png',
          pixelRatio: 2,
          backgroundColor: getComputedStyle(document.body).getPropertyValue('--text-light') || '#ffffff',
          ...opts
        })
      } catch (e) {
        console.warn('Failed to export heatmap image:', e)
        return null
      }
    }

    expose({ getImageDataURL })

    // 生成洞察
    const generateHeatmapInsights = (processedData) => {
      const { ageGroups, crimeTypes, dataMatrix } = processedData

      if (dataMatrix.length === 0) {
        return null
      }

      const maxRiskPoint = dataMatrix.reduce((max, current) =>
        current[2] > max[2] ? current : max
      )

      const minRiskPoint = dataMatrix.reduce((min, current) =>
        current[2] < min[2] ? current : min
      )

      // 计算各年龄段的平均受害率
      const ageAverages = ageGroups.map((age, idx) => {
        const values = dataMatrix.filter(d => d[1] === idx).map(d => d[2])
        const avg = values.length ? values.reduce((s, v) => s + v, 0) / values.length : 0
        return { age, avg }
      })

      // 计算各犯罪类型的平均受害率
      const crimeAverages = crimeTypes.map((crime, idx) => {
        const values = dataMatrix.filter(d => d[0] === idx).map(d => d[2])
        const avg = values.length ? values.reduce((s, v) => s + v, 0) / values.length : 0
        return { crime, avg }
      })

      const topCrime = crimeAverages.reduce((a, b) => (b.avg > a.avg ? b : a), { crime: '', avg: 0 })
      const topAge = ageAverages.reduce((a, b) => (b.avg > a.avg ? b : a), { age: '', avg: 0 })

      return {
        highestRisk: { crime: crimeTypes[maxRiskPoint[0]], age: ageGroups[maxRiskPoint[1]], rate: maxRiskPoint[2] },
        lowestRisk: { crime: crimeTypes[minRiskPoint[0]], age: ageGroups[minRiskPoint[1]], rate: minRiskPoint[2] },
        topAverageCrime: topCrime,
        topAverageAge: topAge
      }
    }

    // API数据获取
    const API_BASE_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com'

    const fetchData = async () => {
      try {
        loading.value = true
        error.value = null

        const response = await fetch(`${API_BASE_URL}/infographics/victimisation/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`HTTP ${response.status}: ${errorText}`)
        }

        const rawData = await response.json()

        if (!Array.isArray(rawData) || rawData.length === 0) {
          throw new Error('No data received from API')
        }

        chartData.value = rawData

        await nextTick()

        setTimeout(() => {
          initHeatmapChart(rawData)
        }, 100)

      } catch (err) {
        console.error('Error details:', err)
        error.value = err.message || 'Failed to fetch data'
      } finally {
        loading.value = false
      }
    }





    // 数据监听
    watch(() => props.data, (newData) => {
      if (newData && newData.length > 0) {
        chartData.value = newData
        nextTick(() => {
          setTimeout(() => {
            initHeatmapChart(newData)
          }, 50)
        })
      }
    }, { immediate: true })

    // 窗口大小调整处理
    const handleResize = () => {
      if (!chartInstance.value || loading.value || error.value || !chartRef.value || !chartData.value) {
        return
      }

      try {
        if (chartInstance.value.isDisposed && chartInstance.value.isDisposed()) {
          return
        }

        const container = chartRef.value
        if (!container || container.offsetWidth === 0 || container.offsetHeight === 0) {
          return
        }

        chartInstance.value.resize({
          width: container.offsetWidth,
          height: container.offsetHeight,
          silent: true
        })

      } catch (error) {
        console.error('Chart resize error:', error)
        if (chartData.value && chartData.value.length > 0) {
          setTimeout(() => {
            try {
              initHeatmapChart(chartData.value)
            } catch (reinitError) {
              console.error('Failed to reinitialize chart:', reinitError)
            }
          }, 100)
        }
      }
    }

    let resizeTimer = null

    const debouncedResize = () => {
      if (resizeTimer) {
        clearTimeout(resizeTimer)
      }

      resizeTimer = setTimeout(() => {
        handleResize()
      }, 200)
    }

    // 组件生命周期
    onMounted(async () => {
      if (props.autoFetch) {
        await fetchData()
      }
      window.addEventListener('resize', debouncedResize)
    })

    onUnmounted(() => {
      if (resizeTimer) {
        clearTimeout(resizeTimer)
        resizeTimer = null
      }

      if (chartInstance.value) {
        try {
          chartInstance.value.off()
          chartInstance.value.dispose()
        } catch (e) {
          console.warn('Error disposing chart on unmount:', e)
        }
        chartInstance.value = null
      }

      window.removeEventListener('resize', debouncedResize)
    })

    return {
      chartRef,
      loading,
      error,
      insights,
      fetchData,
      getImageDataURL
    }
  }
}
</script>

<style scoped>
.heatmap-section {
  background: var(--bg-primary);
  border-radius: 12px;
  font-family: inherit;
}

/* header removed */

.loading, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 3rem;
  color: var(--text-secondary);
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-light);
  border-top: 3px solid var(--violet-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h4 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--violet-ultra-dark);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px var(--shadow-light);
}

.retry-btn:hover {
  background: var(--violet-dark);
}

.content {
  display: flex;
  flex-direction: column;
}

.chart-container {
  background: var(--text-light);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 4px 12px var(--shadow-light);
  border: 1px solid var(--border-light);
}

.main-chart {
  width: 100%;
  height: 500px;
  min-height: 400px;
  position: relative;
  overflow: hidden;
}

.data-source {
  text-align: center;
  padding: 0.75rem 0;
  border-top: 1px solid var(--border-light);
  margin-top: 0.5rem;
}

.data-source p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-style: italic;
}

@media (max-width: 768px) {
  .heatmap-section {
    padding: 1rem;
  }

  .main-chart {
    height: 400px;
    min-height: 350px;
  }
}

@media (max-width: 480px) {
  .main-chart {
    height: 350px;
    min-height: 300px;
  }

  .chart-container {
    padding: 1rem;
  }
}
</style>
