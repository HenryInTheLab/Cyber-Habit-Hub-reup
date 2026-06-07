import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../page/HomePage.vue'
import LinkCheckPage from '../page/LinkCheckPage.vue'
import LibraryPage from '../page/LibraryPage.vue'
import ChallengePage from '../page/ChallengePage.vue'
import CommunityPage from '../page/CommunityPage.vue'
import UserCenterPage from '../page/UserCenterPage.vue'
import SignUpPage from '../page/SignUpPage.vue'
import SignInPage from '../page/SignInPage.vue'
import VideoPage from '../page/VideoPage.vue'
import PrivacyPolicyPage from '../page/PrivacyPolicyPage.vue'
import SupportPage from '../page/SupportPage.vue'
import InfographicPage from '../page/InfographicPage.vue'
import SettingPage from '../page/SettingPage.vue'
import AboutUsPage from '../page/AboutUsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/link-check',
    name: 'LinkCheck',
    component: LinkCheckPage,
  },
  {
    path: '/library',
    name: 'Library',
    component: LibraryPage,
  },
  {
    path: '/challenge',
    name: 'Challenge',
    component: ChallengePage,
  },
  {
    path: '/community',
    name: 'Community',
    component: CommunityPage,
  },
  {
    path: '/user-center',
    name: 'UserCenter',
    component: UserCenterPage,
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUpPage,
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: SignInPage,
  },
  {
    path: '/video/:id',
    name: 'Video',
    component: VideoPage,
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicyPage,
  },
  {
    path: '/about',
    name: 'AboutUs',
    component: AboutUsPage,
  },
  {
    path: '/support',
    name: 'Support',
    component: SupportPage,
  },
  {
    path: '/infographic',
    name: 'Infographic',
    component: InfographicPage,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的位置（浏览器前进/后退），使用保存的位置
    if (savedPosition) {
      return savedPosition
    }
    // 否则滚动到页面顶部
    return { top: 0 }
  }
})

export default router
