<template>
  <div class="explore-library-section">
    <div class="section-container">
      <div class="card-content">
        <div class="section-header">
          <h2 class="card-title">Cybersecurity Library</h2>
        </div>

        <!-- Featured Video Carousel -->
        <div class="featured-video" v-if="videos.length">
          <div class="video-content">
            <div class="content-info">
              <h3 class="video-title">{{ videos[currentIndex].title }}</h3>
              <div class="video-description">
                <span>Video by: {{ videos[currentIndex].author }}</span><br />
                <span>Published date: {{ videos[currentIndex].publish_date }}</span>
              </div>
              <div class="video-meta">
                <span class="video-type">Video</span>
                <span class="video-duration">{{ videos[currentIndex].suggested_reading_time }} min</span>
              </div>
            </div>

            <div class="video-preview" @click="loadVideo(videos[currentIndex].id)">
              <div class="video-thumbnail">
                <img
                  :src="getYouTubeThumbnail(videos[currentIndex].link)"
                  :alt="videos[currentIndex].title"
                  class="thumbnail-image"
                  @error="handleImageError"
                />
                <div class="play-overlay">
                  <svg width="60" height="60" viewBox="0 0 24 24" fill="none">
                    <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
                  </svg>
                </div>
                <div class="duration-badge">{{ videos[currentIndex].suggested_reading_time }} min</div>
              </div>
            </div>
          </div>

          <!-- Navigation Arrows -->
          <button class="nav-arrow nav-prev" @click="prevVideo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
          <button class="nav-arrow nav-next" @click="nextVideo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
        </div>

        <div class="browse-section">
          <router-link to="/library" class="browse-button" @click="scrollToTop">
            Browse Content
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ExploreLibrarySection',
  setup() {
    const router = useRouter()
    const videos = ref([])
    const currentIndex = ref(0)

    const fetchVideos = async () => {
      try {
        const res = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/videos/')
        const data = await res.json()
        videos.value = data.slice(0, 3) // 只取前3个视频用于轮播
        console.log('Fetched videos:', videos.value)
      } catch (err) {
        console.error('Error fetching videos:', err)
      }
    }

    const extractYouTubeId = (url) => {
      if (!url) {
        console.log('No URL provided')
        return null
      }
      const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/
      const match = url.match(regex)
      const videoId = match ? match[1] : null
      console.log('Extracting YouTube ID from:', url, 'Result:', videoId)
      return videoId
    }

    const handleSaveProgress = () => {
      // Handle save progress functionality
    }

    const handleVideoEnded = () => {
      // Handle video ended event
    }

    const loadVideo = (videoId) => {
      router.push(`/video/${videoId}`)
    }

    const getYouTubeThumbnail = (url) => {
      const videoId = extractYouTubeId(url)
      console.log('Getting thumbnail for URL:', url, 'Video ID:', videoId)
      if (videoId) {
        // 尝试多个缩略图尺寸
        return `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`
      }
      return ''
    }

    const handleImageError = (event) => {
      console.log('Image failed to load, using fallback')
      // 设置一个默认的视频图标
      event.target.style.display = 'none'
      const thumbnail = event.target.parentElement
      thumbnail.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      thumbnail.style.display = 'flex'
      thumbnail.style.alignItems = 'center'
      thumbnail.style.justifyContent = 'center'
    }

    const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const nextVideo = () => {
      currentIndex.value = (currentIndex.value + 1) % videos.value.length
    }

    const prevVideo = () => {
      currentIndex.value = (currentIndex.value - 1 + videos.value.length) % videos.value.length
    }

    onMounted(fetchVideos)

    return {
      videos,
      currentIndex,
      extractYouTubeId,
      loadVideo,
      getYouTubeThumbnail,
      handleImageError,
      handleSaveProgress,
      handleVideoEnded,
      nextVideo,
      prevVideo,
      scrollToTop,
    }
  },
}
</script>

<style scoped>
.explore-library-section {
  padding: 0 0 4rem 0;
  background: var(--violet-light);
  min-height: 40vh;
  display: flex;
  align-items: center;
}

.section-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
}

.card-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1000px;
  gap: 30px;
}

.section-header {
  text-align: center;
}

.browse-section {
  display: flex;
  justify-content: center;
}

.card-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--violet-dark);
  margin: 0 0 1rem 0;

}

.browse-button {
  display: inline-block;
  background: var(--violet-dark);
  color: var(--text-light);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  transition: background 0.3s ease;
}

.browse-button:hover {
  background: var(--violet-deep);
}

/* Featured Video Carousel */
.featured-video {
  position: relative;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto 0.4rem auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px var(--shadow-light);
  overflow: visible;
}

.video-content {
  display: flex;
  height: 420px;
  overflow: hidden;
}

.content-info {
  flex: 0.4;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.video-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.video-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.video-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
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
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.video-preview {
  flex: 0.6;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: transparent;
  border-radius: 0;
  overflow: visible;
  width: 100%;
  height: 100%;
  position: relative;
  cursor: pointer;
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
}

.video-preview:hover .play-overlay {
  background: rgba(0, 0, 0, 0.9);
  transform: translate(-50%, -50%) scale(1.1);
}

.duration-badge {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--violet-light);
  border-radius: 8px;
  color: var(--violet-medium);
  font-size: 1rem;
}

/* YouTube Player Styles */
.iframe-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
}

.youtube-embed-wrapper {
  width: 100%;
  height: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* Navigation Arrows - Updated Modern Style */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: white;
  border: 2px solid var(--violet-dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--violet-dark);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.nav-arrow:hover {
  background: var(--violet-dark);
  color: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.nav-arrow svg {
  width: 24px;
  height: 24px;
}

.nav-prev {
  left: -25px;
}

.nav-next {
  right: -25px;
}

@media (max-width: 768px) {
  .explore-library-section {
    padding: 1rem 0;
    min-height: 40vh;
  }

  .section-container {
    padding: 0 15px;
  }

  .card-content {
    gap: 20px;
  }

  .card-title {
    font-size: 1.6rem;
  }


  .video-content {
    display: flex;
    flex-direction: column;
    height: auto;
    overflow: visible;
  }

  .content-info {
    padding: 1rem;
    font-size: 0.9rem;
  }

  .video-preview {
    height: 200px;
    margin-top: 1rem;
  }

  .video-meta,
  .video-description {
    font-size: 0.85rem;
    line-height: 1.2;
  }

  .video-title {
    font-size: 1.1rem;
    line-height: 1.3;
    word-break: break-word;
    hyphens: auto;
  }

  .iframe-container {
    height: 100%;
  }

  .video-placeholder {
    height: 100%;
  }

  /* Mobile arrows positioning */
  .nav-arrow {
    width: 40px;
    height: 40px;
    border-width: 1px;
  }

  .nav-arrow svg {
    width: 20px;
    height: 20px;
  }

  .nav-prev {
    left: -20px;
  }

  .nav-next {
    right: -20px;
  }

  .browse-button {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .section-container {
    padding: 0 10px;
  }

  .card-title {
    font-size: 1.4rem;
  }

}
</style>
