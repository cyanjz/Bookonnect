<template>
  <main>
    <template v-if="threadList">
      <p>{{ threadList }}</p>
      <h1>{{ threadList.username }}님의 쓰레드 목록</h1>
      <template v-for="thread in threadList.threadData" :key="thread.pk">
        <ThreadListCard
          :thread="thread"
        />
      </template>
    </template>
    <template v-else>
      <h1>로딩중...</h1>
    </template>
  </main>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import axios from 'axios'
import ThreadListCard from '@/components/card/ThreadListCard.vue'

const threadList = ref(null)
const route = useRoute()
const accountStore = useAccountStore()
onMounted(() => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.user_pk}/threads/`,
    method: 'get',
  }).then(res => {
    console.log(res)
    threadList.value = res.data
  }).catch(err => {
    console.log(err)
  })
})
</script>


<style scoped></style>