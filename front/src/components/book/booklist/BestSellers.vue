<template>
  <section>
    <h3>베스트셀러</h3>
    <template v-if="books">
      <BookList
        :books="books"
        :carouselId="carouselId"
      />
    </template>
  </section>
</template>


<script setup>
import BookList from '@/components/book/BookList.vue'

const props = defineProps({
  books: Array,
  carouselId: String
})


// 베스트셀러 섹션에서만 캐러셀이 작동하도록 아이디 변경하여 부여
// const carouselId = bestSellersCarousel
</script>


<style scoped>

</style>