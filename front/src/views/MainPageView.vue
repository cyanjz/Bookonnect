<template>
  <main>
    <h1>📚 BooKonnect Main Page</h1>

    <section>
      <h2>🔥 Best Sellers</h2>
      <BestSellers />
    </section>
    <br>
    <section>
      <h2>✨ Recommended by Editors</h2>
      <RecommendedBooks />
    </section>
    <br>
    <section>
      <h2>📂 Books by Category</h2>
      <CategoryBooks />
    </section>
    <br>
    <p>컬렉션 썸네일 컴포넌트 넣어주기</p>
    <br>
    <section>
      <h2>📈 High Ranked Books</h2>
      <HighRankBooks />
    </section>
  </main>
</template>


<script setup>
import { onMounted } from 'vue'
import { useBookStore } from '@/stores/books';

import BestSellers from '@/components/book/booklist/BestSellers.vue';
import RecommendedBooks from '@/components/book/booklist/RecommendedBooks.vue';
import CategoryBooks from '@/components/book/booklist/CategoryBooks.vue';
import HighRankBooks from '@/components/book/booklist/HighRankBooks.vue';

const store = useBookStore()

onMounted(() => {
  store.getBooks()
  // store.getBestSellers()
  // store.getRecommendedBooks()
  // store.getHighRankBooks()
  // store.getCategories()
})
</script>


<style scoped></style>
