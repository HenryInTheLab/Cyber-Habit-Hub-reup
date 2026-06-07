<template>
  <div class="privacy-section">
    <div class="section-header">
      <h2 class="section-title">Privacy Settings</h2>
    </div>

    <div class="privacy-container">
      <!-- Privacy Card -->
      <div class="privacy-card card-base">
        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading privacy settings...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="error-state">
          <div class="alert alert-danger">
            <h6 class="alert-heading">Error loading privacy settings:</h6>
            <p>{{ error }}</p>
            <button @click="fetchPrivacySettings" class="btn btn-retry">Retry</button>
          </div>
        </div>

        <!-- Settings List -->
        <div v-else class="privacy-options">
          <div
            v-for="option in privacyOptions"
            :key="option.key"
            class="privacy-option"
          >
            <label class="privacy-label">
                <input
                type="checkbox"
                class="privacy-checkbox"
                :checked="privacy[option.key]"
                @change="toggleSetting(option.key)"
                />
              {{ option.label }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue"
import { getValidAccessToken } from '@/utils/auth.js'

const API_BASE_URL = "https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com"

export default {
  name: "PrivacySettingSection",
  setup() {
    const loading = ref(true)
    const error = ref(null)
    const privacy = ref({})

    const privacyOptions = [
      { key: "allow_public_ranking", label: "Appear in Leaderboards" },
      { key: "show_score", label: "Show My Points" },
      { key: "show_level", label: "Show My Level" },
      { key: "show_badges", label: "Show My Badges" }
    ]

    const getAccessToken = () => {
      try {
        const token = getValidAccessToken()
        if (!token) throw new Error("No valid access token found")
        return token
      } catch (error) {
        console.error("Error getting access token:", error)
        throw error
      }
    }

    const fetchPrivacySettings = async () => {
      try {
        loading.value = true
        error.value = null
        const res = await fetch(`${API_BASE_URL}/leaderboard/privacy/`, {
          method: "GET",
          headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${getAccessToken()}`
          }
        })
        if (!res.ok) throw new Error("Failed to load privacy settings")
        privacy.value = await res.json()
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const toggleSetting = async (key) => {
    try {
        // 1. Flip the value
        const updatedValue = !privacy.value[key]

        // 2. Send PATCH to backend
        const res = await fetch(`${API_BASE_URL}/leaderboard/privacy/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({ [key]: updatedValue })
        })

        // 3. If backend accepts, reload page
        if (!res.ok) throw new Error("Failed to update setting")

        // Option A: reload the whole page
        window.location.reload()

        // Option B (lighter): re-fetch only privacy settings without full reload
        // await fetchPrivacySettings()
    } catch (err) {
        error.value = err.message
    }
    }



    onMounted(fetchPrivacySettings)

    return { loading, error, privacy, privacyOptions, fetchPrivacySettings, toggleSetting }
  }
}
</script>

<style scoped>
.privacy-section {
  padding: 0 0 2rem 0;
}

/* Header */
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.privacy-container {
  max-width: 1200px;
  margin: 0 auto;
}

.card-base {
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  box-shadow: 0 4px 15px var(--shadow-light);
  padding: 2rem;
  margin-top: 1rem;
}

/* Privacy Options */
.privacy-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.privacy-option {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--violet-light);
  transition: background 0.2s ease;
}

.privacy-option:hover {
  background: var(--violet-sage);
}

.privacy-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: var(--violet-ultra-dark);
  cursor: pointer;
}

.privacy-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 2rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--violet-sage);
  border-top: 4px solid var(--violet-ultra-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error */
.error-state {
  padding: 1rem;
}
</style>
