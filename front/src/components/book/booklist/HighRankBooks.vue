<template>
  <section>
    <template v-if="books">
      <div v-if="books">
        <BookList
          :books="books"
          :carouselId="carouselId"
        />
      </div>
    </template>
  </section>
</template>


<script setup>
import { onMounted, ref } from 'vue';
import BookList from '@/components/book/BookList.vue'
import { useBookStore } from '@/stores/books';
import axios from 'axios';

let books = ref(null)
const bookStore = useBookStore()
const carouselId = 'highranked'
onMounted(() => {
  axios({
    url: bookStore.API_URL + '/api/v1/books',
    method: 'get',
    params: {
      q: 'highranked',
    }
  }).then(res => {
    books.value = res.data
  }).catch(err => {
    console.log(err)
  })
})

</script>


<style scoped>

</style>