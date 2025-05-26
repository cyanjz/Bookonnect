import { createRouter, createWebHistory } from 'vue-router'

// View 경로들 import
import MainPageView from '@/views/MainPageView.vue'

import ProfileView from '@/views/accounts/ProfileView.vue'

import BookDetailView from '@/views/books/BookDetailView.vue'
import BookSearchView from '@/views/books/BookSearchView.vue'

import ThreadListView from '@/views/threads/ThreadListView.vue'
import ThreadDetailView from '@/views/threads/ThreadDetailView.vue'
import ThreadCreateView from '@/views/threads/ThreadCreateView.vue'
import ThreadUpdateView from '@/views/threads/ThreadUpdateView.vue'
import CollectionDetailView from '@/views/collections/CollectionDetailView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. NavBar Menu (메인 페이지(홈) / 회원가입 / 로그인 / 프로필)
    {
      path: '/',
      name: 'main-page',
      component: MainPageView,
    },
    {
      path: '/profile/:userId',
      name: 'profile',
      component: ProfileView,
    },


    // 2. Book (도서 상세 / 도서 검색)
    {
      path: '/books/:book_pk',
      name: 'book-detail',
      component: BookDetailView,
    },
    // {
    //   path: '/books/search',
    //   name: 'book-search',
    //   component: BookSearchView,
    // },


    // 3. Thread (스레드 목록 / 스레드 상세 / 스레드 생성 / 스레드 수정)
    {
      path: '/books/:book_pk/threads',
      name: 'thread-list',
      component: ThreadListView,
    },
    {
      path: '/books/:book_pk/threads/:thread_pk',
      name: 'thread-detail',
      component: ThreadDetailView,
    },
    {
      path: '/books/:book_pk/threads/create',
      name: 'thread-create',
      component: ThreadCreateView,
    },
    {
      path: '/books/:book_pk/threads/:thread_pk/update',
      name: 'thread-update',
      component: ThreadUpdateView,
    },


    // 4. Collection (컬렉션 상세)
    // {
    //   path: '/collection/:collection_pk',
    //   name: 'collection-detail',
    //   component: CollectionDetailView,
    // },
  ],
})

export default router
