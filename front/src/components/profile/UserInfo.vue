<template>
  <div class="card">

    <h1>프로필 내 사용자 정보 영역</h1>
    <div class="card-body">
      <header>
        <img :src="accountStore.userInfo.user_banner_img" alt="배너 없음">
        <img :src="accountStore.userInfo.user_profile_img" alt="프로필 없음">
      </header>
    </div>
    <p>사용자 이름</p>
    <p>사용자 설명</p>
    <p>사용자 프로필 사진</p>
    <p>프로필 배너 사진</p>
  </div>
</template>


<script setup>
import { useAccountStore } from '@/stores/accounts';
import { onMounted } from 'vue';
const accountStore = useAccountStore()
onMounted(() => {
  console.log(accountStore.userInfo)
})
</script>


<style scoped>

</style>