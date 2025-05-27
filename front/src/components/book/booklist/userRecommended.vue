<template>
  <section>
    <h1 v-if="success">좋아할만한 책들입니다!</h1>
    <h1 v-else>아래 책들은 어떠세요?</h1>
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
import { useAccountStore } from '@/stores/accounts';
import axios from 'axios';

let books = ref(null)
const success = ref(false)
const bookStore = useBookStore()
const accountStore = useAccountStore()
const carouselId = 'userRecommended'
onMounted(() => {
  axios({
    url: bookStore.API_URL + '/api/v1/books',
    method: 'get',
    params: {
      q: 'userRecommended',
    },
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    books.value = res.data.data
    success.value = res.data.success
  }).catch(err => {
    console.log(err)
  })
})

</script>


<style scoped>

</style>