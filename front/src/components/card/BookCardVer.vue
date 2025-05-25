<template>
  <div class="card book-card mb-3" style="width: 18rem; cursor: pointer;" @click="$emit('click-card')">
    <img 
      v-if="book.book_cover_img" 
      class="card-img-top" 
      :src="book.book_cover_img" 
      alt="책 표지"
      style="height: 250px; object-fit: cover;"
    >
  
    <div class="card-body">
      <!-- 책 제목 -->
      <h5 class="card-title">{{ book.book_title }}</h5>
      <!-- 평균 별점 -->
      <div v-if="book.book_customer_review_rank !== undefined" class="mb-2">
        <span class="text-warning">
          <!-- 점수만큼 별 반복 -->
          <i class="bi bi-star-fill" v-for="n in Math.round(book.book_customer_review_rank)" :key="n"></i>
        </span>
        <span class="text-muted">
          <!-- 점수 표시 -->
          {{ book.book_customer_review_rank }} / 5
        </span>
      </div> 
    </div>
  </div>
</template>


<script setup>
defineProps({
  book: {
    type: Object,
    required: true
  }
})
</script>


<style scoped>
/* .book-card {
  transition: box-shadow 0.2s;
} */
.book-card:hover {
  box-shadow: 0 0 10px #aaa;
}
</style>

