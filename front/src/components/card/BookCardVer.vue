<template>
  <div class="card book-card mb-3" style="width: 18rem; cursor: pointer;" @click="$emit('click-card')">
    <<img 
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
          <i class="bi bi-star-fill" v-for="n in Math.round(book.book_customer_review_rank)" :key="n"></i>
        </span>
        <span class="text-muted">
          ★{{ book.book_customer_review_rank }} / 5
        </span>
      </div>


      <!-- **아래는 추가로 다른 디테일 쪽에 넣을만한거 미리 써둠! -->
      <!-- 책 설명 -->
        <!-- <p class="card-text" v-if="book.fields.description">
          {{ book.fields.description.length > 60
            ? book.fields.description.slice(0, 60) + '...'
            : book.fields.description
        }}
        </p> -->
      <!-- 책 카테고리 -->
        <!-- <span class="badge bg-primary" v-if="book.fields.category_name">
          {{ book.fields.category_name }}
        </span> -->
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

