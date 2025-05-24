import { createRouter, createWebHistory } from 'vue-router'

// View 경로들 import
import MainPageView from '@/views/MainPageView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 경로 "/"의 view가 없어서 나타나는 경고 해결하기 위한 코드라고는 하는데..
    // 전용 뷰 생성해서 다시해봐야하는지 아님 필요없는건지..;
    // { 
    //   path: '/:pathMatch(.*)*',
    //   name: 'NotFound',
    //   component: () => {
    //     return import(
    //     /* webpackChunkName: "NotFoundView" */ '@/views/NotFoundView.vue'
    //     );
    //   },
    // },

    {
      path: '/book',
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
    }
  ],
})

export default router
