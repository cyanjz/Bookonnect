<template>
  <div class="col">
    <RouterLink
      :to="{
        name: 'thread-detail',
        params: {
          thread_pk: thread.pk,
          book_pk: route.params.book_pk,
        },
      }"
      class="text-decoration-none text-dark"
    >
      <div class="card shadow-sm thread-card">
        <div class="card-body">
          <h5 class="card-title mb-2">{{ thread.thread_title }}</h5>
          <hr>
          <p class="card-text text-muted truncated-content">
            {{ truncateContent(thread.thread_content) }}
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center bg-white border-top-0">
          <small class="text-muted">평점 ★{{ thread.thread_book_review_rank }}</small>
          <small class="text-muted">{{ formatDate(thread.created_at) }}</small>
        </div>
      </div>
    </RouterLink>
  </div>
</template>


<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()

const props = defineProps({
  thread: {
    type: Object,
    required: true
  }
})

// 긴 텍스트 자르기
function truncateContent(content, maxLength = 70) {
  if (!content) return ''
  return content.length > maxLength ? content.slice(0, maxLength) + '...' : content
}

// 날짜 포맷
function formatDate(datetimeStr) {
  if (!datetimeStr) return ''
  return new Date(datetimeStr).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>


<style scoped>
.thread-card {
  transition: transform 0.2s ease;
  border-radius: 12px;
  overflow: hidden;
  height: 200px;
}
.thread-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

hr {
  margin-top: 10px;
}

.truncated-content {
  max-height: 3.6em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 최대 2줄 */
  -webkit-box-orient: vertical;
}
</style>
