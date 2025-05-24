import { createRouter, createWebHistory } from 'vue-router'

// View 경로들 import
import MainPageView from '@/views/MainPageView.vue'

import SignUpView from '@/views/accounts/SignUpView.vue'
import LogInView from '@/views/accounts/LogInView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. NavBar Menu (메인 페이지(홈) / 회원가입 / 로그인 / 프로필)
    {
      path: '/books',
      name: 'main-page',
      component: MainPageView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },


    // 2. Book (도서 상세 / 도서 검색)
    {
      // path: '/books/:book_pk',
      // name: 'book-detail',
      // component:
    },
  ],
})

export default router
