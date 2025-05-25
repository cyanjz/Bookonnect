<template>
  <div>
    <h5>북 리스트 템플릿</h5>
    이걸로 통일하는게 맞나...api를 받아와야 하니까 따로 만드는게 맞으려나
    <BookCardVer 
      v-for="book in books"
      :key="book.pk"
      :book="book"
      @click-card="goToBookDetail(book.pk)"
    />
  </div>
</template>


<script setup>
import { useRouter } from 'vue-router'
import BookCardVer from '../card/BookCardVer.vue';

const props = defineProps({
  books: Array,
})

const router = useRouter()
function goToBookDetail(pk) {
  router.push({ name: 'book-detail', params: { book_pk: pk }})
}
</script>


<style scoped>

</style>