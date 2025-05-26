<template>
  <main>
    <h1>📚 BooKonnect Main Page</h1>

    <BookList />

    <section>
      <h2>🔥 Best Sellers</h2>
      <BestSellers 
        :carouselId="bestSellersCarousel"
      />
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
    <h2>CollectionThumbnail 컴포넌트 넣어주기</h2>
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

import BookList from '@/components/book/BookList.vue'

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


<style scoped>
main {
  margin: 50px;
}

h1,
section {
  margin-bottom: 50px;
}
</style>
