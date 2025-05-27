<template>
  <div>
  </div>
</template>


<script setup>
import { onMounted } from 'vue';
import { useBookStore } from '@/stores/books';

const bookStore = useBookStore()
const props = defineProps({
  book_pk: {
    type: int,
    required: true,
  }
})

onMounted(() => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${props.book_pk}/threads/`,
    method: 'get'
  }).then(res => {
    console.log(res)
  }).catch(err => {
    console.log(err)
  })
})
</script>


<style scoped>

</style>