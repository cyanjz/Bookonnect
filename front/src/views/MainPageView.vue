<template>
  <main>
    <h1>📚 BooKonnect Main Page</h1>

    <!-- 왜 얘는 안될까... -->
    <!-- <BookList :books="store.books" :carouselId="carouselId"/> -->

    <section>
      <h2>🔥 Best Sellers</h2>
      <BestSellers/>
    </section>
    <br>
    <section>
      <h2>✨ Recommended by Editors</h2>
      <RecommendedBooks/>
    </section>
    <br>
    <section>
      <h2>📂 Books by Category</h2>
      <CategoryBooks/>
    </section>
    <br>
    <h2>CollectionThumbnail 컴포넌트 넣어주기</h2>
    <br>
    <section>
      <h2>📈 High Ranked Books</h2>
      <HighRankBooks/>
    </section>
  </main>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books';

import BookList from '@/components/book/BookList.vue'

import BestSellers from '@/components/book/booklist/BestSellers.vue';
import RecommendedBooks from '@/components/book/booklist/RecommendedBooks.vue';
import CategoryBooks from '@/components/book/booklist/CategoryBooks.vue';
import HighRankBooks from '@/components/book/booklist/HighRankBooks.vue';

const store = useBookStore()

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
/*  1. 스타일 1번 */
/* main {
  margin: 50px auto;
  max-width: 1200px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 40px;
  text-align: center;
}

section {
  margin-bottom: 60px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

section h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #34495e;
  margin-bottom: 25px;
  border-bottom: 2px solid #FF0000;
  padding-bottom: 8px;
}

section br {
  margin-bottom: 30px;
} */

/* 반응형 조정 */
/* @media (max-width: 768px) {
  main {
    margin: 20px;
    padding: 10px;
  }
  h1 {
    font-size: 2rem;
  }
  section {
    margin-bottom: 40px;
    padding: 15px;
  }
  section h2 {
    font-size: 1.5rem;
  }
} */


/* 2. 스타일 2번 */
body {
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

main {
  margin: 50px auto;
  max-width: 1200px;
  padding: 20px;
}

section {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 0 40px 0;
}

/* 그라데이션 위에서 잘 보이도록 밝은색 */
section * {
  color: #ccc;
}

h1, h2 {
  color: white
}

h3 {
  color: #ccc; 
}

</style>
