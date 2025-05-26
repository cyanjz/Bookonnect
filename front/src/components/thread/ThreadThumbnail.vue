<template>
  <div class="container py-3">
    <!-- 쓰레드 작성 버튼 -->
    <div class="mb-4 text-end" v-if="accountStore.auth.isAuthenticated">
      <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#threadCreateModal">
        쓰레드 작성
      </button>
    </div>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary mb-3" role="status"></div>
      <h2 class="text-muted">로딩 중...</h2>
    </div>

    <!-- 쓰레드 목록 -->
    <div v-else>
      <p v-if="threads.length === 0" class="text-muted">아직 아무도 쓰레드를 작성하지 않았습니다!</p>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" v-else>
        <ThreadThumbCard v-for="thread in threads" :key="thread.id" :thread="thread" />
      </div>
    </div>
  </div>

  <!-- 쓰레드 작성 모달 -->
  <div class="modal fade modal-xl" id="threadCreateModal" tabindex="-1" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content p-2">
        <!-- 모달 헤더 -->
        <div class="modal-header d-flex flex-column align-items-center border-0">
          <img src="@/assets/LOGO.png" alt="로고" class="mb-2" style="max-height: 60px;" />
          <h1 class="modal-title fs-4">Thread 작성</h1>
          <button type="button" class="btn-close position-absolute top-0 end-0 m-3" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>

        <!-- 모달 바디 -->
        <div class="modal-body">
          <form @submit.prevent="onSubmit">
            <div class="mb-3">
              <label for="thread-title" class="form-label">쓰레드 제목</label>
              <input type="text" class="form-control" id="thread-title" v-model="title" required>
            </div>

            <div class="mb-3">
              <label for="thread-text" class="form-label">쓰레드 내용</label>
              <textarea class="form-control fixed-textarea" id="thread-text" v-model="content" rows="4" required></textarea>
            </div>

            <div class="mb-3">
              <label for="thread-score" class="form-label">쓰레드 점수 (0 ~ 5)</label>
              <input type="number" class="form-control" id="thread-score" v-model="score" min="0" max="5" step="0.5" required />
            </div>

            <div class="modal-footer border-0">
              <button type="submit" class="btn btn-primary w-100">쓰레드 생성</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useBookStore } from '@/stores/books';
import { useAccountStore } from '@/stores/accounts';
import axios from 'axios';
import ThreadThumbCard from '../card/ThreadThumbCard.vue';

const bookStore = useBookStore()
const accountStore = useAccountStore()
const props = defineProps({
  book_pk: {
    type: String,
    required: true,
  }
})

const threads = ref(null)
const isLoading = ref(true)
const getThread = () => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${props.book_pk}/threads/`,
    method: 'get'
  }).then(res => {
    console.log(res)
    threads.value = res.data
    isLoading.value = false
  }).catch(err => {
    console.log(err)
  })
}

let modal = null
onMounted(() => {
  getThread()
  const bootstrap = window.bootstrap
  modal = new bootstrap.Modal(document.getElementById('threadCreateModal'))
})

// 2. thread creation
const route = useRoute()
const title = ref('')
const content = ref('')
const score = ref(0)

const onSubmit = () => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/create/`,
    method: 'post',
    data: {
      thread_title: title.value,
      thread_content: content.value,
      thread_book_review_rank: score.value,
    },
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    getThread()
    document.activeElement.blur()
    modal.hide()
  }).catch(err => {
    console.log(err)
  })
}

const onAIReview = () => {

}

</script>


<style scoped>
.thread-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.thread-button:active {
  background-color: #df0c34;
  color: white;
}

.form-control:focus {
  border-color: #ff2c54;
  box-shadow: none;
}

.fixed-textarea {
  width: 100%;
  height: 200px;
  resize: none;
}
</style>