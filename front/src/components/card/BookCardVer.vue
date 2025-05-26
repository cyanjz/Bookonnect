<template>
  <div class="book-card d-flex flex-column align-items-center">
    <img class="book-cover" 
      :src="store.API_URL+book.book_cover_img || placeholder"
      alt="책 표지" 
    />
    <div class="book-info mt-2 text-center">
      <div class="book-title">{{ book.book_title || '책 제목' }}</div>
      <div class="book-rating fw-bold">
        평균 ★ {{ book.book_customer_review_rank == null ? 0 : book.book_customer_review_rank }}
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


</script>

<style scoped>
.book-card {
  width: 150px;
  margin: 0 8px;
}

.book-cover {
  width: 120px;
  height: 180px;
  background: #adb5bd;
  border-radius: 4px;
}

.book-info {
  font-size: 0.95em;
}

.book-title {
  margin-bottom: 2px;
  word-break: keep-all;
}

.book-rating {
  font-size: 1em;
}
</style>




<!-- <template>
  <div class="card book-card mb-3" style="width: 18rem; cursor: pointer;" @click="$emit('click-card')">
    <img 
      v-if="book.book_cover_img" 
      class="card-img-top" 
      :src="book.book_cover_img" 
      alt="책 표지"
      style="height: 250px; object-fit: cover;"
    >
  
    <div class="card-body">
      <h5 class="card-title">{{ book.book_title }}</h5>
      <div v-if="book.book_customer_review_rank !== undefined" class="mb-2">
        <span class="text-warning">
          <i class="bi bi-star-fill" v-for="n in Math.round(book.book_customer_review_rank)" :key="n"></i>
        </span>
        <span class="text-muted">
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
.book-card {
  transition: box-shadow 0.2s;
}
.book-card:hover {
  box-shadow: 0 0 10px #aaa;
}
</style> -->
