<template>
  <main>
    <h1>Welcome to BooKonnect</h1>

    <!-- 왜 얘는 안될까... -->
    <!-- <BookList :books="store.books" :carouselId="carouselId"/> -->

    <section>
      <h2>Best Sellers</h2>
      <BestSellers />
    </section>
    <br>
    <section>
      <h2>Recommended by Editors</h2>
      <RecommendedBooks />
    </section>
    <br>
    <section>
      <h2>Books by Category</h2>
      <h4>: {{ store.categories[store.selectedCategory].category_name }}</h4>
      <CategoryBooks
        v-if="store.categories"
      />
    </section>
    <br>
    <!-- <h2>CollectionThumbnail 컴포넌트 넣어주기</h2> -->
    <!-- <br> -->
    <section>
      <h2>High Ranked Books</h2>
      <HighRankBooks />
    </section>
    <br>
    <section v-if="accountStore.auth.isAuthenticated">
      <h2>User Recommend</h2>
      <userRecommended />
    </section>
  </main>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books';
import { useAccountStore } from '@/stores/accounts'

import BookList from '@/components/book/BookList.vue'

import BestSellers from '@/components/book/booklist/BestSellers.vue';
import RecommendedBooks from '@/components/book/booklist/RecommendedBooks.vue';
import CategoryBooks from '@/components/book/booklist/CategoryBooks.vue';
import HighRankBooks from '@/components/book/booklist/HighRankBooks.vue';
import userRecommended from '@/components/book/booklist/userRecommended.vue';

const store = useBookStore()
const accountStore = useAccountStore()

const bestSellersCarousel = ref('bestSellersCarousel')
const recommendedCarousel = ref('recommendedCarousel')
const categoriesCarousel = ref('categoriesCarousel')
const highRankCarousel = ref('highRankCarousel')


onMounted(() => {
  store.getBooks()
  // store.getBestSellers()
  // store.getRecommendedBooks()
  // store.getHighRankBooks()
  // store.getCategories()
})
</script>


<style scoped>
body {
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

main {
  margin: 50px 100px;
  /* max-width: 100%; */
  padding: 20px;
}

section {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  /* 패딩: 상우하좌 */
  padding: 20px 0 0 0;
  margin: 50px;
}

/* 그라데이션 위에서 잘 보이도록 밝은색 */
section * {
  color: #ccc;
}

h1 {
  color: #0e2148;
  margin: 50px;
  font-family: Antic;
  font-weight: 600;
  text-align: center;
}


h2 {
  color: white;
  font-family: Antic;
  padding-left: 150px;
}

h4 {
  padding-left: 150px;
  padding-top: 10px;
}
</style>
