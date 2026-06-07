<template>
  <div class="explore-challenge-section">
    <div class="section-container">
      <div class="card-content">
        <div class="section-header">
          <h2 class="card-title">Cybersecurity Challenges</h2>
          <p class="card-subtitle">Progressive learning system with three contextualized tasks</p>
        </div>

        <!-- Challenge Cards -->
        <div class="challenges-grid">
          <div class="challenge-card" v-for="(challenge, index) in challenges" :key="index">
            <div class="challenge-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                <path :d="challenge.icon" />
              </svg>
            </div>
            <div class="challenge-content">
              <h3 class="challenge-title">{{ challenge.title }}</h3>
              <p class="challenge-description">{{ challenge.description }}</p>
              <div class="challenge-level">
                <span class="level-badge level">{{ challenge.level }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="browse-section">
          <router-link to="/challenge" class="browse-button" @click="scrollToTop">
            Start Learning
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ExploreChallengeSection',
  setup() {
    const challenges = ref([
      {
        title: 'Network Newbie Protection',
        description: 'Learn basic cybersecurity protection for beginners in the digital world',
        level: 'Beginner',
        icon: 'M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z'
      },
      {
        title: 'Security Awareness Enhancement',
        description: 'Develop advanced awareness to face complex network threat scenarios',
        level: 'Intermediate',
        icon: 'M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 15C1.732 15 1 15.732 1 16.458v.542a1 1 0 001 1h20a1 1 0 001-1v-.542C23 15.732 22.268 15 21.542 15H2.458zM12 2a8 8 0 100 16 8 8 0 000-16z'
      },
      {
        title: 'Security Expert Advancement',
        description: 'Master professional-level security management and compliance knowledge',
        level: 'Advanced',
        icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'
      }
    ])

    const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    return {
      challenges,
      scrollToTop
    }
  }
}
</script>

<style scoped>
/* Main Section Container */
.explore-challenge-section {
  padding: 0 0 4rem 0; /* 上0rem，下4rem */
  background: var(--bg-primary);
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
  max-width: 1200px;
  gap: 1.5rem;
}

/* Section Header */
.section-header {
  text-align: center;
}

.card-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--violet-dark);
  margin: 0 0 1rem 0;
}

.card-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Challenge Cards Grid */
.challenges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

/* Challenge Card */
.challenge-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px var(--shadow-light);
  position: relative;
  overflow: hidden;
}

.challenge-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--violet-light), var(--violet-medium), var(--violet-dark));
}

.challenge-card:hover {
  box-shadow: 0 8px 30px var(--shadow-medium);
}

/* Challenge Card Icon */
.challenge-icon {
  width: 60px;
  height: 60px;
  background: var(--violet-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--violet-dark);
  margin-bottom: 1.5rem;
}

/* Challenge Card Content */
.challenge-content {
  flex: 1;
}

.challenge-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
  line-height: 1.3;
}

.challenge-description {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
}

/* Challenge Level Badge */
.challenge-level {
  display: flex;
  justify-content: flex-start;
}

.level-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.level {
  background: var(--violet-light);
  color: var(--violet-dark);
}

/* Browse Section */
.browse-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
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

@media (max-width: 768px) {
  .explore-challenge-section {
    padding: 0 0 2rem 0; /* 上0rem，下2rem - 移动端移除标题上方间距 */
    min-height: 50vh;
  }

  .section-container {
    padding: 0 15px;
  }

  .card-content {
    gap: 2rem;
  }

  .card-title {
    font-size: 1.6rem;
  }

  .card-subtitle {
    font-size: 1.125rem;
  }

  .challenges-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .challenge-card {
    padding: 1.5rem;
  }

  .challenge-title {
    font-size: 1.25rem;
  }

  .challenge-description {
    font-size: 0.9rem;
  }

  .challenge-stats {
    gap: 1rem;
  }

  .stat-number {
    font-size: 1.25rem;
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

  .challenge-card {
    padding: 1.25rem;
  }

  .challenge-icon {
    width: 50px;
    height: 50px;
  }

  .challenge-title {
    font-size: 1.125rem;
  }

  .challenge-description {
    font-size: 0.875rem;
  }
}
</style>
