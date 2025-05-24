<template>
  <div>
    <BaseNavBar />
    <RouterView />
    <BaseFooter />
  </div>
</template>


<script setup>
// RouterView나 RouterLink는 이미 전역에 등록되어있으므로 추가 import 필요 x

import BaseNavBar from '@/components/BaseNavBar.vue'
import BaseFooter from '@/components/BaseFooter.vue'
</script>


<style scoped>

</style>