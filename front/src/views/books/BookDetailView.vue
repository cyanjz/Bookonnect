<template>
  <main>
    <h1>도서 상세 페이지</h1>
    <p>책 정보</p>
    <BookInfo />

    <p>작가 정보</p>
    <AuthorInfo />

    <p>쓰레드 썸네일</p>
    <ThreadThumbnail />
  </main>
</template>


<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookDetailStore } from '@/stores/books'

import BookInfo from '@/components/book/BookInfo.vue';
import AuthorInfo from '@/components/book/AuthorInfo.vue';
import ThreadThumbnail from '@/components/thread/ThreadThumbnail.vue';

const route = useRoute()
const store = useBookDetailStore()

onMounted(() => {
  const bookId = route.params.id
  store.getBookInfo(bookId).then(book =>  {
    // 책 정보가 있고 그 안에 작가 아이디가 있다면 -> 작가 정보 받아오기
    // 아니근데 작가 아이디가 존재하나..?
    if (book && book.author_id) {
      store.getAuthorInfo(book.author_id)
    }
  })
  store.getThreads(bookId)
})

</script>


<style scoped>

</style>