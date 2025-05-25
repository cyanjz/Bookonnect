<template>
  <div v-if="book">    
    <div class="book-info d-flex align-items-start">
      <div class="book-cover flex-shrink-0">
        <img :src="book.book_cover_img || placeholder" alt="책 표지" class="cover-img" />
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
</template>

<script setup>
// 레이아웃이 깨지지 않도록 넣을 (책 표지 이미지가 없을 경우) 대체 이미지
const placeholder = 'https://via.placeholder.com/200x280/adb5bd/ffffff?text=Book+Cover'
defineProps({
  book: {
    type: Object,
    required: true
  }
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
</style>
