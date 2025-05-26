<template>
  <main class="container py-4">
    <h1 class="mb-4">도서 상세 페이지</h1>

    <template v-if="!isLoading">
      <!-- 책 정보 -->
      <div class="card mb-4 shadow-sm">
        <div class="card-body d-flex">
          <div class="book-cover me-4">
            <img :src="store.API_URL + book.book_cover_img" alt="책 표지" class="cover-img" />
          </div>
          <div class="flex-grow-1">
            <h2 class="h5 fw-bold">{{ book.book_title }}</h2>
            <p class="mb-1 text-muted">평균 ★ {{ book.book_customer_review_rank }}</p>
            <p class="mb-3">{{ book.book_description }}</p>
            <div>
              <div><strong>출판일:</strong> {{ book.book_pub_date }}</div>
              <div><strong>ISBN:</strong> {{ book.book_ISBN13 }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 작가 정보 -->
      <div class="card mb-4 shadow-sm">
        <div class="card-body d-flex align-items-center">
          <div class="author-img-wrap me-4">
            <img :src="store.API_URL + book.author.author_profile_img" alt="작가 이미지" class="author-img" />
          </div>
          <div>
            <h2 class="h6 fw-bold mb-1">{{ book.author.author_name }}</h2>
            <p class="mb-2">{{ book.author.author_info }}</p>
            <audio controls :src="store.API_URL + book.author.author_info_mp3" class="w-100 mb-1"></audio>
            <div class="text-muted small"><i class="bi bi-volume-up"></i> 작가 음성 정보</div>
          </div>
        </div>
      </div>

      <!-- 쓰레드 썸네일 -->
      <div class="card shadow-sm">
        <div class="card-body">
          <h2 class="h6 fw-bold mb-3">관련 쓰레드 목록</h2>
          <ThreadThumbnail :book_pk="route.params.book_pk" />
        </div>
      </div>
    </template>

    <template v-else>
      <div class="text-center py-5">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted">도서 정보를 불러오는 중입니다...</p>
      </div>
    </template>
  </main>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import axios from 'axios';

import ThreadThumbnail from '@/components/thread/ThreadThumbnail.vue';

import BookInfo from '@/components/book/BookInfo.vue';
import AuthorInfo from '@/components/book/AuthorInfo.vue';

const route = useRoute()
const store = useBookStore()
const isLoading = ref(true)
const book = ref(null)

onMounted(() => {
  const bookId = route.params.book_pk
  console.log(store.API_URL + '/books/' + bookId)
  axios({
    url: store.API_URL + '/api/v1/books/' + bookId,
    method: 'get'
  }).then(res => {
    book.value = res.data
    isLoading.value = false
  }).catch(err => {
    console.log(err)
  })
})

</script>


<style scoped>
.book-info {
  min-height: 280px;
}
.cover-img {
  width: 200px;
  height: 280px;
  object-fit: cover;
  background: #adb5bd;
  border-radius: 4px;
}

.author-img-wrap {
  width: 120px;
  height: 120px;
}
.author-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  background: #adb5bd;
}
.author-info {
  min-height: 120px;
}
</style>