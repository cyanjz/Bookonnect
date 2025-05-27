<template>
  <main class="container">
    <template v-if="!isLoading">
      <h1 class="mb-4 page-title">{{ book.book_title }}</h1>
      
      <!-- 책 정보 -->
      <section class="book-card mb-5">
        <div class="book-card-img">
          <img :src="store.API_URL + book.book_cover_img" alt="책 표지" />
        </div>

        <div class="book-card-info">
          <h2 class="book-title">{{ book.book_title }}</h2>

          <div class="book-rating mb-2">
            <i class="bi bi-star-fill text-warning"></i>
            <span>평균 ★ {{ book.book_customer_review_rank }}</span>
          </div>
          
          <div class="book-meta">
            <div><i class="bi bi-calendar2"></i> 출판일: <span>{{ book.book_pub_date }}</span></div>
            <div><i class="bi bi-upc-scan"></i> ISBN: <span>{{ book.book_ISBN13 }}</span></div>
          </div>
        </div>
        <p class="book-description mb-3">{{ book.book_description }}</p>
      </section>

      <!-- 작가 정보 -->
      <section class="author-card mb-5">
        <div class="author-card-img">
          <img :src="store.API_URL + book.author.author_profile_img" alt="작가 이미지" />
        </div>

        <div class="author-card-info">
          <h3 class="author-name">{{ book.author.author_name }}</h3>

          <p class="author-bio mb-2">{{ book.author.author_info }}</p>

          <div class="author-audio mb-3 ms-1"><i class="bi bi-volume-up"></i>작가 음성 정보</div>
          <audio controls :src="store.API_URL + book.author.author_info_mp3" class="w-100 mb-2"></audio>
        </div>
      </section>

      <!-- 쓰레드 썸네일 -->
      <section class="thread-card">
        <div class="thread-card-header">
          <h2 class="mb-0">Threads List</h2>
        </div>
        <ThreadThumbnail :book_pk="route.params.book_pk" />
      </section>
    </template>

    <template v-else>
      <div class="loading-wrap py-5">
        <div class="spinner-border text-primary mb-3" role="status"></div>
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
.container {
  padding-top: 100px;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -1px;
  color: white;
  text-align: left;
}

/* 카드 스타일 */
.book-card, .author-card {
  display: flex;
  flex-wrap: wrap;
  /* background: #fff; */
  background: rgba(255, 255, 255, 0);
  border: 1.5px solid white; 
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(60, 60, 100, 0.12);
  padding: 2rem;
  gap: 2rem;
  align-items: flex-start;
  transition: box-shadow 0.2s;
}
.book-card:hover, .author-card:hover, .thread-card:hover {
  box-shadow: 0 8px 32px 0 #a1a1a1;
}

/* 책 이미지 */
.book-card-img img {
  width: 180px;
  height: 260px;
  object-fit: cover;
  border-radius: 12px;
  background: #e9ecef;
  box-shadow: 0 2px 8px rgba(90, 90, 120, 0.08);
}

/* 책 정보 */
.book-card-info {
  flex: 1 1 240px;
}
.book-title {
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #3a3a54;
}
.book-rating {
  font-size: 1.1rem;
  color: #c42441;
  /* color: #ff2c54; */
  font-weight: 500;
  display: flex;
  align-items: center;
  margin-left: 2px;
}
.book-description {
  font-size: 1.06rem;
  color: #ccc;
  margin-bottom: 1.2rem;
}
.book-meta {
  font-size: 0.97rem;
  color: #bbb;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.book-meta i {
  margin-right: 0.4em;
  color: #6c63ff;
}


/* 작가 카드 */
.author-card-img img {
  width: 110px;
  height: 110px;
  object-fit: cover;
  border-radius: 50%;
  background: #e9ecef;
}
.author-card-info {
  flex: 1 1 200px;
}
.author-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #f0f0f0;
  margin-bottom: 0.5rem;
}
.author-bio {
  font-size: 1rem;
  color: #ccc;
  min-height: 48px;
}
.author-audio {
  color: #aaa;
}


/* 쓰레드 카드 */
.thread-card-header {
  color: white;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 1rem;
  padding-bottom: 0.6rem;
}
.thread-card {
  background: transparent;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(90, 90, 120, 0.04);
  padding: 1.5rem;
}


/* 로딩 */
.loading-wrap {
  text-align: center;
}


/* 반응형 */
@media (max-width: 768px) {
  .book-card, .author-card {
    flex-direction: column;
    align-items: stretch;
    padding: 1.2rem;
    gap: 1.2rem;
  }
  .book-card-img img, .author-card-img img {
    margin: 0 auto;
  }
}
</style>