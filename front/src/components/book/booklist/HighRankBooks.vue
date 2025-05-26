<template>
  <section>
    <h3>별점 랭킹 상위 도서</h3>
    <div v-if="books">
    <BookList
      :books="books"
      :carouselId="carouselId"
    />
    </div>
  </section>
</template>


<script setup>
import BookList from '@/components/book/BookList.vue'

const props = defineProps({
  books: Array,
  carouselId: String
})

</script>


<style scoped>

</style>