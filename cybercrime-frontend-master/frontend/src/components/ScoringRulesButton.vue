<template>
  <div class="scoring-rules-container">
    <div class="info-icon" @click="toggleModal" :title="'View scoring rules'">
      <svg width="30" height="30" viewBox="0 0 24 24">
        <!-- Outer circle as stroke only -->
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
        <!-- Inner 'i' icon -->
        <path d="M11 17h2v-6h-2v6zm0-8h2V7h-2v2z" fill="currentColor"/>
      </svg>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="toggleModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Scoring Rules</h2>
          <button class="close-button" @click="toggleModal">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <div class="rules-table">
          <div class="table-header">
            <div class="header-item">Activity</div>
            <div class="header-item">Points</div>
            <div class="header-item">Description</div>
          </div>
          <div v-for="(rule, index) in rules" :key="index" class="table-row">
            <div class="row-item">{{ rule.activity }}</div>
            <div class="row-item points">{{ rule.points }}</div>
            <div class="row-item">{{ rule.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScoringRulesButton',
  data() {
    return {
      showModal: false,
      rules: [
        {
          activity: 'Reading Articles',
          points: '3 points',
          description: 'After reading an article you automatically gain 3 points.'
        },
        {
          activity: 'Watching Videos',
          points: '5 points',
          description: 'After watching a video, you automatically gain 5 points.'
        },
        {
          activity: 'Tests accuracy 80%',
          points: '4 points',
          description: 'After finishing the test above 80% accuracy, you automatically gain 4 points.'
        },
        {
          activity: 'Tests accuracy 100%',
          points: '5 points',
          description: 'After finishing the test with 100% accuracy, you automatically gain 5 points.'
        },
        {
          activity: 'Friend Invitation',
          points: '5 points',
          description: 'After the invitation code is used, you automatically gain 5 points.'
        }
      ]
    }
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal
    }
  }
}
</script>

<style scoped>
.scoring-rules-container {
  display: inline-flex;
  align-items: center;
  margin-left: 12px;
}

.info-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: transparent;
  color: var(--violet-deep);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.info-icon:hover {
  color: var(--violet-dark);
  transform: scale(1.05);
}

.info-icon:active {
  transform: scale(0.95);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px 12px 24px;
  border-bottom: 1px solid var(--border-light);
}

.modal-header h2 {
  margin: 0;
  color: var(--violet-dark);
  font-size: 1.5rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: var(--violet-light);
  color: var(--violet-dark);
}

.rules-table {
  padding: 0;
  display: grid;
  grid-template-columns: 2fr 1fr 3fr;
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.table-header, .table-row {
  display: contents;
}

.header-item, .row-item {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
}

.header-item {
  background: var(--violet-light);
  font-weight: 600;
  color: var(--violet-dark);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.row-item {
  color: var(--text-primary);
  font-size: 0.95rem;
  line-height: 1.5;
}

.row-item.points {
  font-weight: 600;
  color: var(--violet-deep);
  justify-content: center;
}

.table-row:last-child .row-item {
  border-bottom: none;
}

.header-item:not(:last-child), .row-item:not(:last-child) {
  border-right: 1px solid var(--border-light);
}

/* Responsive design */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }

  .modal-header {
    padding: 20px 20px 0 20px;
  }

  .rules-table {
    padding: 0 20px 20px 20px;
    grid-template-columns: 1fr;
    gap: 0;
  }

  .header-item, .row-item {
    padding: 12px 16px;
    border-right: none !important;
  }

  .header-item {
    display: none;
  }

  .table-row {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border-light);
    border-radius: 8px;
    margin-bottom: 12px;
    padding: 16px;
    background: var(--bg-primary);
  }

  .row-item {
    border-bottom: none !important;
    padding: 4px 0;
  }

  .row-item:first-child {
    font-weight: 600;
    color: var(--violet-dark);
    margin-bottom: 8px;
  }

  .row-item.points {
    color: var(--violet-deep);
    font-weight: 600;
    margin-bottom: 8px;
  }
}
</style>
