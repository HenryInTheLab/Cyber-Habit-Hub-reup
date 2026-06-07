<template>
  <div class="grouped-bar-section">


    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading financial loss data...</p>
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'GroupedBarChart',
  emits: ['insights'],
  setup(props, { emit, expose }) {
    const chartRef = ref(null)
    const chartInstance = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const chartData = ref(null)

    const insights = ref(null)

    // API base URL - using AWS API Gateway
    const API_BASE_URL = 'https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com'

    // Fetch data from API
    const fetchData = async () => {
      try {
        loading.value = true
        error.value = null

        const response = await fetch(`${API_BASE_URL}/infographics/financial-losses/`, {
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

        // 保存原始数据
        chartData.value = rawData

        // 确保DOM更新后再初始化图表
        await nextTick()

        // 添加小延迟确保DOM完全渲染
        setTimeout(() => {
          initChart()
        }, 100)

      } catch (err) {
        console.error('Error details:', err)
        error.value = err.message || 'Failed to fetch data'
      } finally {
        loading.value = false
      }
    }

    // 横向分组柱状图数据处理逻辑
    const processHorizontalGroupedData = (rawData) => {
      // 提取唯一的犯罪类型
      const crimeTypes = [...new Set(rawData.map(item => item.cybercrime))]

      // 定义损失维度
      const lossTypes = [
        'Median amount directly lost',
        'Median amount spent on consequences',
        'Median amount recovered',
        'Median amount lost after recoveries'
      ]

      // 初始化数据映射结构
      const dataMap = {}
      crimeTypes.forEach(crime => {
        dataMap[crime] = {}
        lossTypes.forEach(type => {
          dataMap[crime][type] = 0
        })
      })

      // 填充实际数据
      rawData.forEach(item => {
        if (crimeTypes.includes(item.cybercrime) && lossTypes.includes(item.median_type)) {
          dataMap[item.cybercrime][item.median_type] = item.value
        }
      })

      return { crimeTypes, lossTypes, dataMap }
    }

    // ECharts横向分组柱状图配置
    const createHorizontalGroupedBarOption = (processedData) => {
      const { crimeTypes, lossTypes, dataMap } = processedData

      // 简化标签名称
      const simplifiedLabels = {
        'Median amount directly lost': 'Direct Loss',
        'Median amount spent on consequences': 'Additional Costs',
        'Median amount recovered': 'Amount Recovered',
        'Median amount lost after recoveries': 'Net Loss'
      }

      // 颜色配置 - 现代配色方案
      const colors = {
        'Direct Loss': '#8B5A96',           // 紫色 - 直接损失
        'Additional Costs': '#E67E22',      // 橙色 - 额外成本
        'Amount Recovered': '#16A085',      // 青绿色 - 恢复金额
        'Net Loss': '#34495E'              // 深灰蓝 - 净损失
      }

      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            let result = `<div style="padding: 8px;">
              <div style="font-weight: bold; margin-bottom: 8px; color: #2c3e50;">
                ${params[0].name}
              </div>`

            params.forEach(param => {
              const value = param.value
              const color = param.color
              result += `
                <div style="margin: 4px 0; display: flex; align-items: center;">
                  <span style="display: inline-block; width: 12px; height: 12px; background: ${color}; border-radius: 2px; margin-right: 8px;"></span>
                  <span style="color: #34495e;">${param.seriesName}:</span>
                  <span style="font-weight: bold; margin-left: 8px; color: #2c3e50;">$${value.toLocaleString()}M</span>
                </div>`
            })

            result += `</div>`
            return result
          }
        },
        legend: {
          data: Object.keys(simplifiedLabels).map(key => simplifiedLabels[key]),
          bottom: 14,
          itemGap: 20,
          textStyle: {
            fontSize: 12,
            color: '#666'
          }
        },
        grid: {
          left: '16%',
          right: '10%',
          top: '10%',
          bottom: '20%',
          containLabel: false
        },
        xAxis: {
          type: 'value',
          name: 'Amount ($M)',
          nameLocation: 'middle',
          nameGap: 30,
          nameTextStyle: {
            color: '#666',
            fontSize: 12,
            align: 'center'
          },
          axisLabel: {
            formatter: function(value) {
              return '$' + value + 'M'
            },
            color: '#666'
          },
          axisLine: {
            lineStyle: {
              color: '#ddd'
            }
          },
          splitLine: {
            lineStyle: {
              color: '#f0f0f0',
              type: 'dashed'
            }
          }
        },
        yAxis: {
          type: 'category',
          data: crimeTypes,
          axisLabel: {
            fontSize: 12,
            color: '#888',
            // 如果标签太长，可以换行显示
            formatter: function(value) {
              if (value.length > 8) {
                const words = value.split(' ')
                const mid = Math.ceil(words.length / 2)
                return words.slice(0, mid).join(' ') + '\n' + words.slice(mid).join(' ')
              }
              return value
            }
          },
          axisLine: {
            lineStyle: {
              color: '#ddd'
            }
          },
          axisTick: {
            show: false
          }
        },
        series: lossTypes.map(lossType => ({
          name: simplifiedLabels[lossType],
          type: 'bar',
          data: crimeTypes.map(crime => dataMap[crime][lossType]),
          itemStyle: {
            color: colors[simplifiedLabels[lossType]],
            borderRadius: [0, 4, 4, 0] // 右侧圆角
          },
          barMaxWidth: 25, // 控制柱子最大宽度
          label: {
            show: true,
            position: 'right',
            distance: 6,
            fontSize: 10,
            color: '#7A8A9A',
            formatter: function(params) {
              return '$' + params.value.toLocaleString() + 'M'
            }
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
          }
        }))
      }
    }

    // 多维度排序功能
    const sortDataByDimension = (processedData, sortType) => {
      if (sortType === 'none') {
        return processedData
      }

      const { crimeTypes, dataMap } = processedData

      // 定义排序字段映射
      const sortFieldMap = {
        'direct_loss': 'Median amount directly lost',
        'additional_costs': 'Median amount spent on consequences',
        'amount_recovered': 'Median amount recovered',
        'net_loss': 'Median amount lost after recoveries'
      }

      const sortField = sortFieldMap[sortType]
      if (!sortField) {
        return processedData
      }

      // 创建新的数组副本进行排序，避免修改原始数组
      const sortedCrimes = [...crimeTypes].sort((a, b) => {
        const valueA = dataMap[a][sortField] || 0
        const valueB = dataMap[b][sortField] || 0
        return valueB - valueA
      })

      return {
        ...processedData,
        crimeTypes: sortedCrimes
      }
    }

    // Initialize ECharts grouped bar chart
    const initChart = () => {
      if (!chartRef.value || !chartData.value) {
        return
      }

      if (!Array.isArray(chartData.value) || chartData.value.length === 0) {
        error.value = 'No valid data available for visualization'
        return
      }

      // 创建图表实例
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }

      chartInstance.value = echarts.init(chartRef.value)

      // 初始化图表
      updateChart()

      // Handle window resize
      const handleResize = () => {
        if (chartInstance.value) {
          chartInstance.value.resize()
        }
      }
      window.addEventListener('resize', handleResize)
    }

    // Update chart with current data
    const updateChart = () => {
      if (chartInstance.value && chartData.value) {
        let processedData = processHorizontalGroupedData(chartData.value)

        // 固定按直接损失（Direct Loss）降序排序
        processedData = sortDataByDimension(processedData, 'direct_loss')

        const option = createHorizontalGroupedBarOption(processedData)
        chartInstance.value.setOption(option, true)

        // Generate insights
        insights.value = generateFinancialInsights(processedData)
        emit('insights', insights.value)
      }
    }

    // Export chart as image
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
        console.warn('Failed to export bar chart image:', e)
        return null
      }
    }

    expose({ getImageDataURL })

    // Generate insights
    const generateFinancialInsights = (processedData) => {
      const { crimeTypes, dataMap } = processedData

      if (!crimeTypes || crimeTypes.length === 0) {
        return null
      }

      const directLossValues = crimeTypes.map(crime => ({
        crime,
        value: dataMap[crime]['Median amount directly lost'] || 0
      }))
      const netLossValues = crimeTypes.map(crime => ({
        crime,
        value: dataMap[crime]['Median amount lost after recoveries'] || 0
      }))

      const highestDirect = directLossValues.reduce((a, b) => (b.value > a.value ? b : a), { crime: '', value: 0 })
      const highestNet = netLossValues.reduce((a, b) => (b.value > a.value ? b : a), { crime: '', value: 0 })
      const minDirect = directLossValues.reduce((a, b) => (b.value < a ? b.value : a), directLossValues[0]?.value || 0)
      const maxDirect = directLossValues.reduce((a, b) => (b.value > a ? b.value : a), 0)

      return {
        highestDirectLoss: highestDirect.value,
        highestDirectLossCrime: highestDirect.crime,
        highestNetLoss: highestNet.value,
        highestNetLossCrime: highestNet.crime,
        totalRecovered: crimeTypes.reduce((sum, crime) => sum + (dataMap[crime]['Median amount recovered'] || 0), 0),
        averageRecoveryRate: calculateAverageRecoveryRate(processedData),
        minDirectLoss: minDirect,
        maxDirectLoss: maxDirect
      }
    }

    // Calculate average recovery rate
    const calculateAverageRecoveryRate = (processedData) => {
      const { crimeTypes, dataMap } = processedData
      let totalRate = 0
      let validCount = 0

      crimeTypes.forEach(crime => {
        const directLoss = dataMap[crime]['Median amount directly lost'] || 0
        const recovered = dataMap[crime]['Median amount recovered'] || 0

        if (directLoss > 0) {
          totalRate += (recovered / directLoss) * 100
          validCount++
        }
      })

      return validCount > 0 ? (totalRate / validCount).toFixed(1) : '0.0'
    }


    // Lifecycle hooks
    onMounted(() => {
      fetchData()
    })

    onUnmounted(() => {
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }
      window.removeEventListener('resize', () => {})
    })

    return {
      chartRef,
      loading,
      error,
      insights,
      fetchData,
      getImageDataURL,

    }
  }
}
</script>

<style scoped>
.grouped-bar-section {
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

@media (max-width: 768px) {
  .grouped-bar-section {
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
