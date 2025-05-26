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
import { useBookStore } from '@/stores/books'

const bookStore = useBookStore()
bookStore.getCategories()
</script>



<style>
body, #app {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  /* 위는 흰색, 아래는 검정으로 자연스럽게 전환되는 그라데이션 */
  background: linear-gradient(to bottom, #fff 0%, #111 20%);
}
</style>