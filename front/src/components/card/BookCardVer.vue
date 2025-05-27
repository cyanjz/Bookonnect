<template>
  <div class="book-card d-flex flex-column align-items-center">
    <RouterLink
    :to="{name: 'book-detail', params: {book_pk: book.pk}}"
    >
    <img class="book-cover" 
      :src="store.API_URL+book.book_cover_img || placeholder"
      alt="책 표지" 
    />
    </RouterLink>
    <div class="book-info mt-2 text-center">
      <div class="book-title" :title="book.book_title || '책 제목'">
        {{ cutTitle(book.book_title, 25) }}
      </div>
      <div class="book-rating fw-bold">
        평균 ★{{ book.book_customer_review_rank }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { useBookStore } from '@/stores/books.js'

const store = useBookStore()


defineProps({
  book: Object
})

// 제목을 자르는 함수
function cutTitle(title, len = 25) {
  if (!title) return '책 제목'
  return title.length > len ? title.slice(0, len - 3) + '...' : title
}
</script>

<style scoped>
.book-card {
  width: 200px;
  margin: 20px 10px;
  padding: 20px 10px 14px 10px; /* 위, 좌우, 아래 패딩(아래는 약간 줄임) */
  transition: box-shadow 0.2s;
}
.book-card:hover {
  box-shadow: 0 0 10px #ccc;
  /* box-shadow: 0 8px 24px rgba(0,0,0,0.13); */
}

.book-cover {
  width: 160px;
  height: 240px;
  background: #adb5bd;
  border-radius: 4px;
}

.book-info {
  font-size: 0.95em;
}

.book-title {
  color: whitesmoke;
  margin-bottom: 2px;
  word-break: keep-all;
}

.book-rating {
  color: #ccc;
  font-size: 1em;
}
</style>
