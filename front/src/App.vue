<template>
  <div>
    <NavBar />
    <RouterView />
    <Footer />
  </div>
</template>


<script setup>
// RouterView나 RouterLink는 이미 전역에 등록되어있으므로 추가 import 필요 x

import NavBar from '@/components/layout/NavBar.vue'
import Footer from '@/components/layout/Footer.vue'
</script>


<style scoped>

</style>