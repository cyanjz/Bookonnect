<template>
  <section>
    <h3>별점 랭킹 상위 도서</h3>
    <BookList
      :books="books"
    />
  </section>
</template>


<script setup>
import BookList from '@/components/book/BookList.vue'

defineProps({
  books: Array
})
</script>


<style scoped>

</style>