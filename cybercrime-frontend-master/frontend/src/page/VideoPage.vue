<template>
  <div class="video-page">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading video...</p>
    </div>

    <div v-else-if="video" class="video-content">
      <div class="back-button-container">
        <button class="back-button" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back to Library
        </button>
      </div>

      <div class="title-info-container">
        <h1 class="video-page-title">{{ video.title }}</h1>

        <div class="video-info-section">
          <div class="video-meta">
            <span class="video-type">Video</span>
            <span class="video-duration">{{ video.suggested_reading_time }} min</span>
          </div>
          <div class="video-description">
            <span>Video by: {{ video.author }}</span>
            <span>Published date: {{ video.publish_date }}</span>
          </div>
        </div>
      </div>

      <div class="video-page-content">
        <div class="video-player-container">
          <YoutubePlayer
            :key="video.id"
            :videoId="extractYouTubeId(video.link)"
            :videoKey="video.id"
            :initialProgress="getVideoProgress(video.id)"
            @save-progress="handleSaveProgress"
            @video-ended="handleVideoEnded"
          />
        </div>

        <!-- Related Suggestions -->
        <div v-if="showRecommendations" class="related-content">
          <h2 class="related-content__heading">Recommended for You</h2>

          <div v-if="relatedVideos.length" class="related-content__videos">
            <h3 class="related-content__section-title">Related Videos</h3>
            <div class="related-videos-grid">
              <div v-for="relatedVideo in relatedVideos" :key="relatedVideo.id" class="related-video-card" @click="loadRelatedVideo(relatedVideo)">
                <div class="video-thumbnail">
                    <img
                      :src="'https://img.youtube.com/vi/' + extractYouTubeId(relatedVideo.link) + '/0.jpg'"
                      alt="Thumbnail"
                      class="thumbnail-img"
                    />
                  <div class="play-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M8 5v14l11-7z"/>
                    </svg>
                  </div>
                  <div class="duration-badge">{{ relatedVideo.suggested_reading_time }} min</div>
                </div>
                <div class="video-info">
                  <h4 class="video-title">{{ relatedVideo.title }}</h4>
                  <p class="video-author">Video by: {{ relatedVideo.author }}</p>
                  <p class="video-date">Published date: {{ relatedVideo.publish_date }}</p>
                </div>
                <div class="video-type-badge">
                  <span class="type-label">Video</span>
                  <span class="duration-label">{{ relatedVideo.suggested_reading_time }} min</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="relatedQuiz" class="related-content__quiz">
            <h3 class="related-content__section-title">Quick Quiz: {{ relatedQuiz.question_text }}</h3>
            <ul class="related-content__quiz-options">
              <li
                v-for="option in relatedQuiz.options"
                :key="option.identifier"
                class="related-content__quiz-option"
                :class="{
                  'correct-option': option.is_answer,
                  'incorrect-option': selectedAnswer === option.identifier && !option.is_answer,
                  'selected-option': selectedAnswer === option.identifier
                }"
              >
                <label class="related-content__quiz-label">
                  <input
                    type="radio"
                    :name="relatedQuiz.id"
                    :value="option.identifier"
                    class="related-content__quiz-input"
                    :checked="selectedAnswer === option.identifier"
                    @change="checkAnswer(option)"
                    :disabled="selectedAnswer !== null"
                  />
                  {{ option.identifier }}. {{ option.text }}

                  <!-- Feedback next to selected option -->
                  <span v-if="selectedAnswer === option.identifier">
                    <span v-if="option.is_answer" style="color: green; font-weight: bold;">✔ Correct</span>
                    <span v-else style="color: red; font-weight: bold;">✘ Incorrect</span>
                  </span>

                  <!-- Show ✔ on correct answer, even if not selected -->
                  <span
                    v-if="selectedAnswer && option.is_answer && selectedAnswer !== option.identifier"
                    style="color: green; font-weight: bold; margin-left: 10px;"
                  >
                    ✔ Correct Answer
                  </span>
                </label>
              </li>

            </ul>
            <details
              v-if="selectedAnswer"
              class="related-content__explanation"
              open
            >
              <summary class="related-content__explanation-toggle">Explanation</summary>
              <p class="related-content__explanation-text">{{ relatedQuiz.explanation }}</p>
            </details>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import YoutubePlayer from '@/components/YoutubePlayer.vue'

const route = useRoute()
const router = useRouter()

const video = ref(null)
const loading = ref(true)
const relatedVideos = ref([])
const relatedQuiz = ref(null)
const showRecommendations = ref(false)
const videoProgress = ref({})
const selectedAnswer = ref(null)
const isAnswerCorrect = ref(null)
// const viewedVideoIds = ref(new Set())


const fetchVideo = async () => {
  const token = localStorage.getItem('access_token')

  try {
    loading.value = true

    // 构建请求头
    const headers = {}
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/', {
      headers
    })

    if (!response.ok) {
      console.error('Failed to fetch videos')
      return
    }

    const videosData = await response.json()
    const currentId = route.params.id
    const foundVideo = videosData.find(v => v.id === currentId || v.id === currentId.toString())

    if (!foundVideo) {
      console.error('Video not found')
      return
    }

    video.value = foundVideo
    relatedQuiz.value = null
    relatedVideos.value = []
    showRecommendations.value = false
    selectedAnswer.value = null
    isAnswerCorrect.value = null

  } catch (err) {
    console.error('Error fetching video:', err)
  } finally {
    loading.value = false
  }
}

const checkAnswer = (option) => {
  selectedAnswer.value = option.identifier
  isAnswerCorrect.value = option.is_answer === true
}



const extractYouTubeId = (url) => {
  const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/
  const match = url.match(regex)
  return match ? match[1] : null
}

const handleSaveProgress = async (progressData) => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  const { videoId, currentTime, duration } = progressData
  const actualVideoId = videoId || video.value?.id
  if (!actualVideoId) return

  videoProgress.value[actualVideoId] = {
    currentTime,
    duration,
    lastWatched: new Date().toISOString()
  }

  try {
    await fetch(`https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/${actualVideoId}/progress/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        current_time: currentTime,
        duration: duration
      })
    })
  } catch (error) {
    console.error('Error saving video progress:', error)
  }

}

const fetchRelatedVideos = async (id) => {
  const token = localStorage.getItem('access_token')

  try {
    // 构建请求头
    const headers = {}
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    const response = await fetch(
      `https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/${id}/related/`,
      {
        headers
      }
    )

    if (!response.ok) {
      console.error('Failed to fetch related videos')
      return
    }

    const data = await response.json()
    relatedVideos.value = data.related_videos || []
    relatedQuiz.value = data.related_quiz || null

  } catch (err) {
    console.error('Error fetching related videos:', err)
  }
}


const handleVideoEnded = () => {
  showRecommendations.value = true

  // Show toast after video completion
  setTimeout(() => {
    window.showActivityToast()
  }, 1000)
}


const loadRelatedVideo = (relatedVideo) => {
  if (!relatedVideo?.id) return
  router.push(`/video/${relatedVideo.id}`)
  fetchRelatedVideos(relatedVideo.id)
}

const getVideoProgress = (videoId) => {
  return videoProgress.value[videoId] || null
}

const fetchUserProgress = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/progress/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      const progressData = await response.json()
      videoProgress.value = {}
      progressData.forEach(progress => {
        videoProgress.value[progress.video_id] = {
          currentTime: progress.current_time,
          duration: progress.duration,
          lastWatched: progress.last_watched
        }
      })
    }
  } catch (error) {
    console.error('Error fetching user progress:', error)
  }
}

const goBack = () => {
  router.push('/library')
}

onMounted(async () => {
  await fetchVideo()
  await fetchUserProgress()
  await fetchVideo()
  if (video.value?.id) {
    await fetchRelatedVideos(video.value.id)
  }
})

watch(() => route.params.id, async (newId) => {
  loading.value = true
  await fetchVideo()
  await fetchRelatedVideos(newId)
  loading.value = false
})
</script>

<style scoped>
.video-page {
  min-height: 100vh;
  background: var(--bg-primary);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--violet-sage);
  border-top: 4px solid var(--violet-dark);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.video-content {
  padding: 2rem;
}

/* Video page back button */
.back-button-container {
  margin-bottom: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background: var(--violet-sage);
  color: var(--violet-dark);
}

.title-info-container {
  max-width: 1000px;
  margin: 0 auto 1rem auto;
}

.video-page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
}

.video-page-content {
  max-width: 1000px;
  margin: 0 auto;
}

.video-player-container {
  aspect-ratio: 16 / 9;
  margin-bottom: 2rem;
  border-radius: 12px;
  overflow: hidden;
}

.video-info-section {
  padding: 0;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.video-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.video-type {
  background: var(--violet-deep);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.video-duration {
  color: var(--text-secondary);
  font-weight: 500;
}

.video-description {
  color: var(--text-secondary);
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Related Content Styles */
.related-content {
  margin-top: 2rem;
  padding: 1.5rem;
  background: var(--bg-light);
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

.related-content__heading {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.related-content__section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.related-videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.related-video-card {
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  box-shadow: 0 2px 8px var(--shadow-light);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px var(--shadow-medium);
}

.video-thumbnail {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--bg-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.play-button {
  z-index: 2;
  width: 60px;
  height: 60px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.duration-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.video-info {
  padding: 1rem;
}

.video-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.video-author, .video-date {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 0.25rem 0;
}

.video-type-badge {
  padding: 0.75rem 1rem;
  background: var(--bg-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.type-label {
  background: var(--violet-deep);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.duration-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

.related-content__quiz {
  margin-top: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.related-content__quiz-options {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.related-content__quiz-option {
  margin-bottom: 0.75rem;
}

.related-content__quiz-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.75rem;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.related-content__quiz-label:hover {
  background: var(--bg-light);
}

.related-content__quiz-input {
  margin: 0;
  margin-top: 0.2rem;
}

.related-content__explanation {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-light);
  border-radius: 6px;
}

.related-content__explanation-toggle {
  cursor: pointer;
  font-weight: 600;
  color: var(--violet-dark);
}

.related-content__explanation-text {
  margin-top: 0.75rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Responsive Design */
@media (max-width: 768px) {
  .video-page-title {
    font-size: 1.4rem;
  }

  .video-page-content {
    padding: 1rem;
  }

  .video-player-container {
    margin-bottom: 1.5rem;
  }

  .video-info-section {
    margin-bottom: 1.5rem;
  }

  .related-content {
    padding: 1rem;
    margin-top: 1.5rem;
  }

  .related-content__heading {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }


  .related-content__quiz {
    padding: 0.75rem;
    margin-top: 1rem;
  }

  .related-videos-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .related-video-card {
    margin-bottom: 0;
  }

  .video-info {
    padding: 0.75rem;
  }

  .video-title {
    font-size: 0.9rem;
  }

  .video-author, .video-date {
    font-size: 0.8rem;
  }
}
</style>
