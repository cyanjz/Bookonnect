<template>
  <div class="author-info d-flex align-items-center">
    <div class="author-img-wrap flex-shrink-0">
      <img :src="author.author_profile_img || placeholder" alt="작가 이미지" class="author-img" />
    </div>
    <div class="ms-4">
      <div class="fw-bold mb-1">{{ author.author_name }}</div>
      <div>{{ author.author_info }}</div>
      <div>{{ author.author_info_mp3 }}</div>
      <div class="mt-2"><i class="bi bi-volume-up"></i></div>
    </div>
  </div>
</template>

<script setup>
const placeholder = 'https://via.placeholder.com/120x120/adb5bd/ffffff?text=Author'
defineProps({
  author: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.author-img-wrap {
  width: 120px;
  height: 120px;
}
.author-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  background: #adb5bd;
}
.author-info {
  min-height: 120px;
}
</style>
