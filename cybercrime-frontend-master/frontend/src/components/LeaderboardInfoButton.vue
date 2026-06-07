<template>
  <div class="leaderboard-info-button-container">
    <div class="info-icon" @click="toggleModal" :title="'How to earn points and appear on leaderboard'">
      <svg width="30" height="30" viewBox="0 0 24 24">
        <!-- Outer circle as stroke only -->
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
        <!-- Inner 'i' icon -->
        <path d="M11 17h2v-6h-2v6zm0-8h2V7h-2v2z" fill="currentColor"/>
      </svg>
    </div>

    <!-- Toast Notification -->
    <div v-if="showModal" class="toast-overlay" @click="closeModal">
      <div class="toast-content" @click.stop>
        <div class="toast-message">
          <div class="toast-title">How to Get on the Leaderboard</div>
          <div class="toast-description">
            <p>Earn points by reading articles and watching videos in our Library, or completing challenges.</p>
            <strong>The more points you earn, the higher your rank!</strong>
          </div>
        </div>
        <button @click="closeModal" class="modal-close">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showModal = ref(false)

const toggleModal = () => {
  showModal.value = !showModal.value
}

const closeModal = () => {
  showModal.value = false
}
</script>

<style scoped>
.leaderboard-info-button-container {
  position: relative;
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

/* Toast Styles */
.toast-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
}

.toast-content {
  background: var(--violet-light);
  display: flex;
  align-items: flex-start;
  text-align: left;
  padding: 32px;
  gap: 12px;
  border-radius: 12px;
}

.toast-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.toast-description {
  color: var(--text-secondary);
  font-size: 1.2rem;
}

.toast-description strong {
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.modal-close:hover {
  background: var(--violet-sage);
}

@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .toast-content {
    width: 95%;
    margin: 0.5rem;
  }

  .toast-header {
    padding: 0.8rem 1rem;
  }

  .toast-title {
    font-size: 1rem;
  }

  .toast-body {
    padding: 1rem;
  }

  .toast-body p {
    font-size: 0.9rem;
  }
}
</style>
