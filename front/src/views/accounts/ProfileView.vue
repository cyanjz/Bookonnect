<template>
  <main>
    <template v-if="isLoading">
      <h2>로딩 중...</h2>
    </template>
    <template v-if="!isLoading">
      <ProfileCard
        :userInfo="userInfo"
        @follow="onFollow"
        @updateProfile="onUpdate"
      />
    </template>
  </main>
</template>


<script setup>
import { useAccountStore } from '@/stores/accounts';
import { ref } from 'vue';
import ProfileCard from '@/components/profile/ProfileCard.vue';
import axios from 'axios';

import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const accountStore = useAccountStore()
const userInfo = ref(null)
const isLoading = ref(true)
onMounted(async () => {
    axios({
      url: `http://127.0.0.1:8000/accounts/${route.params.userId}/`,
      method: 'get',
    }).then((res) => {
      console.log(res.data)
      userInfo.value = res.data
      isLoading.value = false
    }).catch((err) => {
      console.log(err)
    })
})

const onFollow = (data) => {
  userInfo.value.num_followers = data.numFollowers
  userInfo.value.isFollowed = !data.removed
}

const onUpdate = (data) => {
  userInfo.value = data
}

</script>


<style scoped>
main {
  padding-top: 100px;
}
</style>