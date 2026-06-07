<template>
  <div class="iframe-container">
    <iframe
      ref="youtubeIframe"
      :src="computedSrc"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
      class="youtube-embed-wrapper"
    ></iframe>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'


const getAccessToken = () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('No access token found')
  }
  return token
}


const props = defineProps({
  videoId: String,
  videoKey: [String, Number],
  initialProgress: Object
})

const emit = defineEmits([
  'save-progress',
  'video-ended',
  'show-related-videos'
])

const youtubeIframe = ref(null)
let player = null
let interval = null

const backendStartTime = ref(0)

const computedSrc = computed(() => {
  return `https://www.youtube.com/embed/${props.videoId}?enablejsapi=1&start=${backendStartTime.value}&rel=0`
})

const handleVideoEnd = async () => {
  try {
    const token = getAccessToken()
    const res = await fetch(
      `https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/${props.videoKey}/related/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!res.ok) throw new Error(`Failed to fetch related content: ${res.status}`)
    const data = await res.json()

    emit('video-ended', {
      relatedVideos: data.related_videos || [],
      relatedQuiz: data.related_quiz || null
    })
  } catch (err) {
    console.error('Error fetching related content:', err)
  }
}



const setupPlayerPolling = () => {
  interval = setInterval(() => {
    (async () => {
      if (player && typeof player.getCurrentTime === 'function') {
        const time = player.getCurrentTime()
        localStorage.setItem(`video-progress-${props.videoKey}`, Math.floor(time))

        try {
          const token = getAccessToken()
          await fetch(
            `https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/${props.videoKey}/progress/`,
            {
              method: 'PATCH',
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ progress: Math.floor(time) })
            }
          )
        } catch (e) {
          console.error('Error saving progress:', e)
        }

        emit('save-progress', { id: props.videoId, time })
      }
    })()
  }, 5000)
}

const initYouTubeAPI = () => {
  if (!window.YT || !window.YT.Player) {
    const tag = document.createElement('script')
    tag.src = 'https://www.youtube.com/iframe_api'
    const firstScriptTag = document.getElementsByTagName('script')[0]
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)
    window.onYouTubeIframeAPIReady = createPlayer
  } else {
    createPlayer()
  }
}


const createPlayer = () => {
  player = new window.YT.Player(youtubeIframe.value, {
    events: {
      onReady: () => {
        setupPlayerPolling()
      },
      onStateChange: (event) => {
        if (event.data === window.YT.PlayerState.ENDED) {
          handleVideoEnd()
        }
      }
    }
  })
}

const fetchBackendProgress = async () => {
  try {
    const token = getAccessToken()
    const res = await fetch(
      `https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/${props.videoKey}/progress/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (res.ok) {
      const data = await res.json()
      backendStartTime.value = data.progress || 0
    }
  } catch (e) {
    console.error('Failed to fetch video progress:', e)
  }
}

onMounted(() => {
  // 如果有初始进度，使用它；否则从后端获取
  if (props.initialProgress && props.initialProgress.currentTime) {
    backendStartTime.value = Math.floor(props.initialProgress.currentTime)
    initYouTubeAPI()
  } else {
    fetchBackendProgress().then(() => {
      initYouTubeAPI()
    })
  }
})

onBeforeUnmount(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>

.iframe-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.youtube-embed-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

@media (max-width: 480px) {
  .iframe-container {
    padding-top: 65%;
  }
}
</style>
