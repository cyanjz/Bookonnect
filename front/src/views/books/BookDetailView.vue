<template>
  <main>
    <h1>도서 상세 페이지</h1>
    <template v-if="!isLoading">
      <p>책 정보</p>
      <div v-if="book">
        <div class="book-info d-flex align-items-start">
          <div class="book-cover flex-shrink-0">
            <img :src="store.API_URL + book.book_cover_img" alt="책 표지" class="cover-img" />
          </div>
          <div class="ms-4 flex-grow-1">
            <div class="fw-bold fs-5 mb-2">
              {{ book.book_title }}
              <span class="ms-2 fs-6 text-dark">평균★ {{ book.book_customer_review_rank }}</span>
            </div>
            <div class="mb-3" style="min-height: 48px;">
              {{ book.book_description }}
            </div>
            <div class="mt-4">
              <div class="fw-bold">출판사명</div>
              <div>{{ book.book_pub_date }}</div>
              <div>{{ book.book_ISBN13 }}</div>
            </div>
          </div>
        </div>
      </div>

      <p>작가 정보</p>
      <div class="author-info d-flex align-items-center">
        <div class="author-img-wrap flex-shrink-0">
          <img :src="store.API_URL + book.author.author_profile_img" alt="작가 이미지" class="author-img" />
        </div>
        <div class="ms-4">
          <div class="fw-bold mb-1">{{ book.author.author_name }}</div>
          <div>{{ book.author.author_info }}</div>
          <div>{{ book.author.author_info_mp3 }}</div>
          <div class="mt-2"><i class="bi bi-volume-up"></i></div>
        </div>
      </div>

      <p>쓰레드 썸네일</p>
      <div>
        <h1>쓰레드 목록 썸네일</h1>
        <p>BookDetailView에만 들어감.</p>
        <p>하위 컴포넌트: ThreadThumbCard</p>
      </div>
    </template>

    <template v-if="isLoading">
      로딩중...
    </template>
  </main>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import axios from 'axios';

import BookInfo from '@/components/book/BookInfo.vue';
import AuthorInfo from '@/components/book/AuthorInfo.vue';
import ThreadThumbnail from '@/components/thread/ThreadThumbnail.vue';

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
    console.log(res.data)
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