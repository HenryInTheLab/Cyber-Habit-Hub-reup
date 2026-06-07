<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo/Brand -->
      <div class="nav-brand" @click="goToHome">
        <img src="./../assets/logo.png" alt="GuardU Logo" class="nav-logo">CyberHabit Hub
      </div>

      <!-- Desktop Navigation Links -->
      <div class="nav-links desktop-nav">
        <router-link to="/infographic" class="nav-link">Infographic</router-link>
        <div class="nav-dropdown" @click="toggleActivityDropdown">
          <span class="nav-link dropdown-trigger" :class="{ 'router-link-active': isActivityActive }">Activity</span>
          <div class="dropdown-menu" :class="{ open: isActivityDropdownOpen }">
            <router-link to="/link-check" class="dropdown-item" @click="closeActivityDropdown">Link Check</router-link>
            <router-link to="/library" class="dropdown-item" @click="closeActivityDropdown">Library</router-link>
            <router-link to="/challenge" class="dropdown-item" @click="closeActivityDropdown">Challenge</router-link>
          </div>
        </div>
        <router-link to="/community" class="nav-link">Community</router-link>
        <router-link to="/support" class="nav-link">Support</router-link>

      </div>

      <!-- Desktop Right side buttons -->
      <div class="nav-buttons desktop-nav">
        <div v-if="!isAuthenticated" class="auth-buttons">
          <button @click="goToSignIn" class="btn btn-signin" :disabled="loading">
            {{ loading ? 'Loading...' : 'Sign In' }}
          </button>
          <button @click="goToSignUp" class="btn btn-signup" :disabled="loading">
            {{ loading ? 'Loading...' : 'Sign Up' }}
          </button>
        </div>
        <div v-else class="user-menu">
          <div class="user-avatar-container" @click="toggleUserDropdown">
            <div class="user-avatar">
              {{ getUserInitial() }}
            </div>
            <div class="user-dropdown" :class="{ open: isUserDropdownOpen }">
              <div class="dropdown-item" @click="() => { goToUserCenter(); isUserDropdownOpen = false; }">
                User Center
              </div>
              <div class="dropdown-item" @click="() => { goToSettings(); isUserDropdownOpen = false; }">
                Settings
              </div>
              <div class="dropdown-item" @click="() => { signOut(); isUserDropdownOpen = false; }">
                Sign Out
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile Menu Button -->
      <button @click="toggleMobileMenu" class="mobile-menu-btn" :class="{ active: isMobileMenuOpen }">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </div>

    <!-- Mobile Menu Backdrop -->
    <div v-if="isMobileMenuOpen" class="mobile-menu-backdrop" @click="closeMobileMenu"></div>

    <!-- Mobile Menu Dropdown -->
    <div class="mobile-menu" :class="{ open: isMobileMenuOpen }">
      <div class="mobile-menu-content">
        <!-- Mobile Navigation Links -->
        <div class="mobile-nav-links">
          <div class="mobile-dropdown" @click="toggleMobileActivityDropdown">
            <span class="mobile-nav-link dropdown-trigger" :class="{ 'router-link-active': isActivityActive }">Activity</span>
            <div class="mobile-dropdown-menu" :class="{ open: isMobileActivityDropdownOpen }">
              <router-link to="/link-check" class="mobile-dropdown-item" @click="closeMobileMenu">Link Check</router-link>
              <router-link to="/library" class="mobile-dropdown-item" @click="closeMobileMenu">Library</router-link>
              <router-link to="/challenge" class="mobile-dropdown-item" @click="closeMobileMenu">Challenge</router-link>
            </div>
          </div>
          <router-link to="/infographic" class="mobile-nav-link" @click="closeMobileMenu">Infographic</router-link>
          <router-link to="/community" class="mobile-nav-link" @click="closeMobileMenu">Community</router-link>
          <router-link to="/support" class="mobile-nav-link" @click="closeMobileMenu">Support</router-link>
        </div>

        <!-- Mobile User Section -->
        <div class="mobile-user-section">
          <div v-if="!isAuthenticated" class="mobile-auth-buttons">
            <button @click="goToSignIn" class="btn btn-signin mobile-btn" :disabled="loading">
              {{ loading ? 'Loading...' : 'Sign In' }}
            </button>
            <button @click="goToSignUp" class="btn btn-signup mobile-btn" :disabled="loading">
              {{ loading ? 'Loading...' : 'Sign Up' }}
            </button>
          </div>
          <div v-else class="mobile-user-menu">
            <div class="mobile-user-info">
              <div class="mobile-user-avatar" @click="() => { goToUserCenter(); closeMobileMenu(); }">
                <div class="mobile-avatar">
                  {{ getUserInitial() }}
                </div>
                <span class="mobile-username">{{ userEmail }}</span>
              </div>
            </div>
            <button @click="signOut" class="btn btn-logout mobile-btn">Sign Out</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'NavigationBar',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isAuthenticated = ref(false)
    const loading = ref(false)
    const userEmail = ref(null)
    const isMobileMenuOpen = ref(false)
    const isUserDropdownOpen = ref(false)
    const isActivityDropdownOpen = ref(false)
    const isMobileActivityDropdownOpen = ref(false)

    // 计算属性：检查当前路由是否属于 Activity 子菜单
    const isActivityActive = computed(() => {
      const activityRoutes = ['/link-check', '/library', '/challenge']
      return activityRoutes.includes(route.path)
    })

    const signIn = async () => {
      router.push('/signin')
    }

    const signOut = async () => {
      try {
        // Clear localStorage
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_info')

        isAuthenticated.value = false
        userEmail.value = null
        router.push('/')
      } catch (error) {
        console.error('Sign out error:', error)
      }
    }

    const goToUserCenter = () => {
      router.push('/user-center')
    }

    const goToSettings = () => {
      router.push('/settings')
    }

    const goToSignUp = () => {
      router.push('/signup')
      closeMobileMenu()
    }

    const goToSignIn = () => {
      router.push('/signin')
      closeMobileMenu()
    }

    const goToHome = () => {
      router.push('/')
    }

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value
      // Prevent body scroll when menu is open
      if (isMobileMenuOpen.value) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false
      document.body.style.overflow = ''
    }

    const toggleUserDropdown = () => {
      isUserDropdownOpen.value = !isUserDropdownOpen.value
    }

    const toggleActivityDropdown = () => {
      isActivityDropdownOpen.value = !isActivityDropdownOpen.value
    }

    const closeActivityDropdown = () => {
      isActivityDropdownOpen.value = false
    }

    const toggleMobileActivityDropdown = () => {
      isMobileActivityDropdownOpen.value = !isMobileActivityDropdownOpen.value
    }

    const getUserInitial = () => {
      if (!userEmail.value) return '?'
      return userEmail.value.charAt(0).toUpperCase()
    }

    const getUserEmail = () => {
      try {
        const userInfoStr = localStorage.getItem('user_info')
        if (userInfoStr) {
          const userInfo = JSON.parse(userInfoStr)
          userEmail.value = userInfo.username || 'User'
        } else {
          userEmail.value = 'User'
        }
      } catch {
        userEmail.value = 'User'
      }
    }

    const checkAuthStatus = () => {
      try {
        const accessToken = localStorage.getItem('access_token')
        if (accessToken) {
          isAuthenticated.value = true
          getUserEmail()
        } else {
          isAuthenticated.value = false
          userEmail.value = null
        }
      } catch {
        isAuthenticated.value = false
        userEmail.value = null
      }
    }

    watch(isAuthenticated, (newValue) => {
      if (newValue && !userEmail.value) {
        getUserEmail()
      }
    })

    onMounted(() => {
      checkAuthStatus()

      // Add click outside listener for dropdown
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      // Restore body scroll when component is unmounted
      document.body.style.overflow = ''

      // Remove click outside listener
      document.removeEventListener('click', handleClickOutside)
    })

    const handleClickOutside = (event) => {
      const avatarContainer = document.querySelector('.user-avatar-container')
      const activityDropdown = document.querySelector('.nav-dropdown')

      if (avatarContainer && !avatarContainer.contains(event.target)) {
        isUserDropdownOpen.value = false
      }

      if (activityDropdown && !activityDropdown.contains(event.target)) {
        isActivityDropdownOpen.value = false
      }
    }

    return {
      isAuthenticated,
      loading,
      userEmail,
      isMobileMenuOpen,
      isUserDropdownOpen,
      isActivityDropdownOpen,
      isMobileActivityDropdownOpen,
      isActivityActive,
      signIn,
      signOut,
      goToUserCenter,
      goToSettings,
      goToSignUp,
      goToSignIn,
      goToHome,
      toggleMobileMenu,
      closeMobileMenu,
      toggleUserDropdown,
      toggleActivityDropdown,
      closeActivityDropdown,
      toggleMobileActivityDropdown,
      getUserInitial,
    }
  },
}
</script>

<style scoped>
.navbar {
  background: var(--violet-light);
  box-shadow: 0 2px 8px var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0.8rem 8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

/* Common hover effects */
.nav-link:hover,
.dropdown-item:hover {
  background: var(--violet-sage);
}

.btn-signin:hover:not(:disabled),
.btn-logout:hover,
.mobile-nav-link:hover,
.mobile-dropdown-item:hover {
  background: var(--violet-medium);
  color: var(--text-light);
}

.nav-link.router-link-active {
  background: var(--violet-dark);
  color: var(--text-light);
}

/* Activity Dropdown Styles */
.nav-dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-trigger {
  cursor: pointer;
  position: relative;
}

.dropdown-trigger::after {
  content: '▼';
  font-size: 0.7rem;
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid var(--border-light);
  min-width: 160px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
  margin-top: 0;
  overflow: hidden;
}

.dropdown-menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu .dropdown-item {
  display: block;
  text-decoration: none;
  font-weight: 500;
}

.dropdown-menu .dropdown-item:hover {
  color: var(--violet-dark);
}

.dropdown-menu .dropdown-item.router-link-active {
  background: var(--violet-dark);
  color: var(--text-light);
}

.nav-brand {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.nav-logo {
  height: 2.8rem;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.auth-buttons {
  display: flex;
  gap: 0.75rem;
}

.user-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-avatar-container {
  position: relative;
  cursor: pointer;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--violet-dark);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid var(--border-light);
  min-width: 160px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
  margin-top: 0;
}

.user-dropdown.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  color: var(--text-primary);
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--border-light);
}

.dropdown-item:last-child {
  border-bottom: none;
}

.user-email {
  color: var(--text-primary);
  font-weight: 500;
  background: var(--violet-sage);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid var(--border-light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-email.clickable {
  cursor: pointer;
}

.user-email.clickable:hover {
  background: var(--violet-medium);
  color: var(--text-light);
}

.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-signin {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--violet-medium);
}

.btn-signin:hover:not(:disabled) {
  background: var(--violet-medium);
  color: var(--text-light);
}

.btn-signup {
  background: var(--violet-dark);
  color: var(--text-light);
}

.btn-signup:hover:not(:disabled) {
  background: var(--violet-deep);
}

.btn-logout {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--violet-medium);
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 2rem;
  height: 2rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  position: relative;
}

.hamburger-line {
  width: 100%;
  height: 2px;
  background: var(--text-primary);
  transition: all 0.3s ease;
  position: absolute;
}

.hamburger-line:nth-child(1) {
  top: 6px;
}

.hamburger-line:nth-child(2) {
  top: 50%;
  transform: translateY(-50%);
}

.hamburger-line:nth-child(3) {
  bottom: 6px;
}

/* Active state - forms X */
.mobile-menu-btn.active .hamburger-line:nth-child(1) {
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
}

.mobile-menu-btn.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active .hamburger-line:nth-child(3) {
  bottom: 50%;
  transform: translateY(50%) rotate(-45deg);
}


/* Mobile Menu Backdrop */
.mobile-menu-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  backdrop-filter: blur(2px);
}

/* Mobile Menu */
.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: var(--violet-light);
  border-bottom: 1px solid var(--border-light);
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
  max-height: 100vh;
  overflow-y: auto;
  padding-top: 80px;
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.mobile-menu-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  display: block;
  text-align: center;
  background: var(--violet-sage);
  margin-bottom: 0.5rem;
}

.mobile-nav-link.router-link-active {
  background: var(--violet-dark);
  color: var(--text-light);
}

/* Mobile Activity Dropdown Styles */
.mobile-dropdown {
  position: relative;
}

.mobile-dropdown .dropdown-trigger::after {
  content: '▼';
  font-size: 0.7rem;
  margin-left: 0.5rem;
}

.mobile-dropdown-menu {
  background: var(--violet-sage);
  margin-top: 0;
  overflow: hidden;
  max-height: 0;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  border: 1px solid var(--border-light);
}

.mobile-dropdown-menu.open {
  max-height: 200px;
  opacity: 1;
  visibility: visible;
}

.mobile-dropdown-item {
  display: block;
  padding: 0.8rem 1.5rem;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  transition: all 0.3s ease;
  border-bottom: 1px solid var(--border-light);
  background: var(--violet-sage);
}

.mobile-dropdown-item:last-child {
  border-bottom: none;
}

.mobile-dropdown-item.router-link-active {
  background: var(--violet-dark);
  color: var(--text-light);
}

.mobile-user-section {
  border-top: 1px solid var(--border-light);
  padding-top: 1.5rem;
}

.mobile-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mobile-user-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-user-info {
  display: flex;
  justify-content: center;
}

.mobile-user-avatar {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
}

.mobile-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: var(--violet-dark);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.mobile-username {
  color: var(--text-primary);
  font-weight: 500;
}

.mobile-btn {
  width: 100%;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .nav-brand {
    font-size: 1.5rem;
  }

  .mobile-menu {
    padding-top: 70px;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0.8rem;
  }

  .nav-brand {
    font-size: 1.3rem;
  }

  .mobile-menu-content {
    padding: 1rem;
  }

  .mobile-nav-link {
    padding: 0.7rem 0.8rem;
  }

  .mobile-btn {
    padding: 0.7rem 1.2rem;
  }

  .mobile-menu {
    padding-top: 60px;
  }
}
</style>
