<template>
  <main>
    <h1>쓰레드 상세 페이지</h1>
    <template v-if="threadDetail === null">
      <p>로딩 중...</p>
    </template>

    <template v-else>
      <div class="container py-4">
        <!-- Book & Thread Info -->
        <div class="card mb-4" v-if="threadDetail">
          <div v-if="threadDetail.thread_cover_img" class="thread-cover-wrapper">
            <img :src="accountStore.API_URL + threadDetail.thread_cover_img" alt="Thread Cover"
              class="thread-cover-img" />
          </div>
          <div class="row g-0">
            <div class="col-md-4">
              <img :src="accountStore.API_URL + threadDetail.book.book_cover_img" class="img-fluid rounded-start"
                alt="Book Cover" style="object-fit: cover; height: 100%; width: 100%;" />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">{{ threadDetail.book.book_title }}</h5>
                <p class="card-text">
                  <small class="text-muted">출간일: {{ threadDetail.book.book_pub_date }}</small><br />
                  평균 평점: {{ threadDetail.book.avg_review_rank }} / 5.0
                </p>
                <hr />
                <div class="d-flex align-items-center mb-2">
                  <img :src="accountStore.API_URL + threadDetail.user.user_profile_img" class="rounded-circle me-2"
                    width="40" height="40" alt="작성자 이미지" />
                  <strong>{{ threadDetail.user.username }}</strong>
                </div>
                <h4 class="mb-2">{{ threadDetail.thread_title }}</h4>
                <p class="mb-2">{{ threadDetail.thread_content }}</p>
                <p class="text-muted">
                  평점: {{ threadDetail.thread_book_review_rank }} / 5.0<br />
                  작성일: {{ new Date(threadDetail.thread_updated_at).toLocaleString() }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Comments Section -->
        <div v-if="threadDetail">
          <button type="button" class="btn btn-primary" v-if="accountStore.auth.isAuthenticated" data-bs-toggle="modal"
            data-bs-target="#commentCreate">댓글 생성</button>
          <h5 class="mb-3">댓글 {{ threadDetail.comments.length }}개</h5>
          <div class="row">
            <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-3" v-for="comment in threadDetail.comments"
              :key="comment.pk">
              <div v-if="Number(comment.user.pk) === Number(accountStore.auth.userPk)" class="card h-100 comment-card"
                @click="openCommentUpdateModal(comment)" style="cursor: pointer;">
                <div class="card-body">
                  <div class="d-flex align-items-center mb-2">
                    <img :src="accountStore.API_URL + comment.user.user_profile_img" alt="프로필 이미지"
                      class="rounded-circle me-2" width="32" height="32" />
                    <strong>{{ comment.user.username }}</strong>
                  </div>
                  <p class="card-text">{{ comment.comment_content }}</p>
                  <small class="text-muted">
                    {{ new Date(comment.comment_created_at).toLocaleString() }}
                  </small>
                  <div class="mt-2 d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-danger" @click.stop="">
                      ❤️ {{ comment.num_likes }}
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="card h-100 comment-card">
                <div class="card-body">
                  <div class="d-flex align-items-center mb-2">
                    <img :src="accountStore.API_URL + comment.user.user_profile_img" alt="프로필 이미지"
                      class="rounded-circle me-2" width="32" height="32" />
                    <strong>{{ comment.user.username }}</strong>
                  </div>
                  <p class="card-text">{{ comment.comment_content }}</p>
                  <small class="text-muted">
                    {{ new Date(comment.comment_created_at).toLocaleString() }}
                  </small>
                  <div class="mt-2 d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-danger diabled" @click.stop="onCommentLike(comment.pk)">
                      ❤️ {{ comment.num_likes }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </main>

  <div class="modal fade" id="commentCreate" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5" id="exampleModalLabel">댓글 작성</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createComment">
            <div class="mb-3">
              <label for="commet-create-text" class="col-form-label">내용</label>
              <textarea class="form-control" id="commet-create-text" v-model="commentContent"></textarea>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 comment-create-button">생성</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="commentUpdate" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5" id="exampleModalLabel">댓글 수정</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateComment">
            <div class="mb-3">
              <label for="commet-update-text" class="col-form-label">내용</label>
              <textarea class="form-control" id="comment-update-text" v-model="commentUpdateContent"></textarea>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 comment-update-button">수정</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useBookStore } from '@/stores/books';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';

const route = useRoute()
const bookStore = useBookStore()
const accountStore = useAccountStore()
const threadDetail = ref(null)
let modal = null
let updateModal = null
const getThreadInfo = () => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/`,
    method: 'get',
  }).then(res => {
    console.log(res)
    threadDetail.value = res.data
  }).catch(err => {
    console.log(err)
  })
}
onMounted(() => {
  const bootstrap = window.bootstrap
  modal = new bootstrap.Modal(document.getElementById('commentCreate'))
  updateModal = new bootstrap.Modal(document.getElementById('commentUpdate'))
  getThreadInfo()
})

const commentContent = ref('')
const createComment = () => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/comments/create/`,
    method: 'post',
    data: {
      comment_content: commentContent.value,
    },
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    console.log(res)
    modal.hide()
    commentContent.value = ''
    getThreadInfo()
  }).catch(err => {
    console.log(err)
  })
}

const commentUpdateContent = ref('')
const updateTargetComment = ref(0)

const openCommentUpdateModal = (comment) => {
  commentUpdateContent.value = comment.comment_content
  updateTargetComment.value = comment.pk
  console.log(comment.comment_content)
  updateModal.show()
}

const updateComment = () => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/comments/${updateTargetComment.value}/`,
    method: 'put',
    data: {
      'comment_content': commentUpdateContent.value,
    },
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    console.log(res)
    updateModal.hide()
    getThreadInfo()
  }).catch(err => {
    console.log(err)
  })
}
</script>


<style scoped>
.comment-create-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.comment-create-button:active {
  background-color: #df0c34;
  color: white;
}

.form-control:focus {
  border-color: #ff2c54;
  box-shadow: none;
}
.thread-cover-wrapper {
  width: 100%;
  max-height: 250px;
  overflow: hidden;
  border-top-left-radius: 0.375rem;
  border-top-right-radius: 0.375rem;
}

.thread-cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}
</style>