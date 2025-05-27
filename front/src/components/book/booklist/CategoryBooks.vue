<template>
  <section>
    <!-- <h1>#{{ categoryName }}</h1> -->
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
const carouselId = 'category'
// const categoryName = ref('')

onMounted(() => {
  const idx = bookStore.selectedCategory
  // categoryName.value = bookStore.categories.at(idx)["category_name"]
  axios({
    url: bookStore.API_URL + '/api/v1/books',
    method: 'get',
    params: {
      q: 'category',
      cId: idx+1,
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