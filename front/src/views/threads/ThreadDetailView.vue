<template>
  <main>
    <!-- <Spinner v-if="ui.loading" /> -->
    <div v-if="threadDetail === null">
      <p>로딩 중...</p>
    </div>

    <div v-else>
      <div class="thread-container">
        <h1 class="page-title">쓰레드 상세 페이지</h1>
        <!-- #1. Book & Thread Info -->
        <div class="card thread-card mb-4" v-if="threadDetail">
          <!-- 1. 쓰레드 커버 이미지 -->
          <div v-if="threadDetail.thread_cover_img" class="thread-cover-wrapper">
            <img :src="accountStore.API_URL + threadDetail.thread_cover_img" alt="Thread Cover"
              class="thread-cover-img" />
          </div>

          <div class="row g-0">
            <!-- 2. 책 표지 -->
            <div class="col-md-4">
              <img :src="accountStore.API_URL + threadDetail.book.book_cover_img" class="img-fluid rounded-start"
                alt="Book Cover" style="object-fit: cover; height: 100%; width: 100%;" />
            </div>

            <!-- 3. 쓰레드 카드 내부 -->
            <div class="col-md-8">
              <div class="card-body">
                <!--3-1. 책 정보 -->
                <h5 class="card-title">{{ threadDetail.book.book_title }}</h5>
                <p class="card-text">
                  <small class="text-muted">출간일: {{ threadDetail.book.book_pub_date }}</small><br />
                  평균 평점: {{ Number(threadDetail.book.avg_review_rank).toFixed(1) }} / 5.0
                </p>
                <hr>
                <!-- 3-2. 쓰레드 작성자 프로필 -->
                <div class="d-flex align-items-center mb-2">
                  <!-- 3-2-1. 이미지or이름 클릭 시 해당 프로필로 이동 -->
                  <div @click="onProfileClick(threadDetail.user.pk)" class="user-info">
                    <img :src="accountStore.API_URL + threadDetail.user.user_profile_img" class="rounded-circle me-2"
                      width="40" height="40" alt="작성자 이미지" />
                    <strong>{{ threadDetail.user.username }}</strong>
                  </div>
                  <!-- 3-2-2. 쓰레드 수정/삭제 -->
                  <div class="ms-auto" v-if="Number(threadDetail.user.pk) === Number(accountStore.auth.userPk)">
                    <button class="btn btn-sm btn-outline-secondary mx-1" @click="onEditThread" data-bs-toggle="modal"
                      data-bs-target="#thread-update-modal">수정</button>
                    <button class="btn btn-sm btn-outline-danger mx-1" @click="onDeleteThread">삭제</button>
                  </div>
                </div>
                <!-- 3-3. 쓰레드 제목 -->
                <div class="d-flex align-items-center mb-2">
                  <h4 class="mb-0">{{ threadDetail.thread_title }}</h4>
                  <!-- 3-3-1. 쓰레드 좋아요 버튼 -->
                  <button class="btn btn-sm ms-3 like-button"
                    :class="{ disabled: !accountStore.auth.isAuthenticated || accountStore.auth.userPk === threadDetail.user.pk }"
                    @click="toggleThreadLike" style="font-size: 1.2rem; line-height: 1;">
                    ❤︎ {{ threadDetail.thread_likes }}
                  </button>
                </div>
                <!-- 3-4. 쓰레드 내용 -->
                <p class="mb-2">{{ threadDetail.thread_content }}</p>
                <p class="text-muted">
                  평점: {{ threadDetail.thread_book_review_rank }} / 5.0<br />
                  <small class="text-muted">작성일: {{ new Date(threadDetail.thread_updated_at).toLocaleString() }}</small>
                </p>
              </div>
            </div>
          </div>
        </div>


        <!-- #2. Comments Section -->
        <div v-if="threadDetail">
          <!-- 1. 댓글 생성 버튼 / 댓글 개수 -->
          <button type="button" class="btn comment-create-button" v-if="accountStore.auth.isAuthenticated"
            data-bs-toggle="modal" data-bs-target="#commentCreate">댓글 생성</button>
          <h5 class="comment-count">댓글 {{ threadDetail.comments.length }}개</h5>

          <div class="row">
            <!-- 2. 댓글 리스트 반복 => 내 댓글인지, 남의 댓글인지 구분 -->
            <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-3" v-for="comment in threadDetail.comments"
              :key="comment.pk">
              <!-- 2-1. 내 댓글인 경우 -->
              <div v-if="Number(comment.user.pk) === Number(accountStore.auth.userPk)" class="card h-100 comment-card"
                @click="openCommentUpdateModal(comment)" style="cursor: pointer;">
                <div class="card-body">
                  <div class="d-flex align-items-center mb-2">
                    <img :src="accountStore.API_URL + comment.user.user_profile_img" alt="프로필 이미지"
                      class="rounded-circle me-2" width="32" height="32" />
                    <strong>{{ comment.user.username }}</strong>
                    <!-- 2-1-1. 댓글 삭제 -->
                    <div class="ms-auto">
                      <button class="btn btn-outline-danger btn-sm"
                        @click.stop="onCommentDelete(comment.pk)">삭제</button>
                    </div>
                  </div>
                  <p class="card-text">{{ comment.comment_content }}</p>
                  <small class="text-muted">
                    {{ new Date(comment.comment_created_at).toLocaleString() }}
                  </small>
                  <!-- 2-1-2. 내 댓글이므로 좋아요 비활성화 / 좋아요 수 표시 -->
                  <div class="mt-2 d-flex align-items-center">
                    <button class="btn btn-sm me-1 disabled like-button" @click.stop="">
                      ❤︎
                    </button>
                    {{ comment.num_likes }}
                  </div>
                </div>
              </div>
              <!-- 2-2. 남의 댓글인 경우 -->
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

                  <!-- 2-2-1. 남의 댓글이므로 좋아요 활성화 / 좋아요 수 표시(공통) -->
                  <div class="mt-2 d-flex align-items-center">
                    <button class="btn btn-sm me-1 like-button" @click.stop="onCommentLike(comment.pk)">
                      ❤︎
                    </button>
                    {{ comment.num_likes }}
                  </div>
                </div>

              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>


  <!-- #3. Comment Create (modal form) -->
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
              <button type="submit" class="btn w-100 create-finish-button">생성</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>


  <!-- #4. Comment Update (modal form) -->
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


  <!-- #5. Thread Update (modal form + AI) -->
  <div class="modal fade modal-xl" id="thread-update-modal" tabindex="-1" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content p-2">
        <!-- 1. 모달 헤더 -->
        <div class="modal-header d-flex flex-column align-items-center border-0">
          <img src="@/assets/LOGO.png" alt="로고" class="mb-2" style="max-height: 60px;" />
          <h1 class="modal-title fs-4">Thread 수정</h1>
          <button type="button" class="btn-close position-absolute top-0 end-0 m-3" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>

        <!-- 2. 모달 바디 -->
        <div class="modal-body">
          <form @submit.prevent="onThreadUpdate">
            <div class="mb-3">
              <label for="thread-title" class="form-label">쓰레드 제목</label>
              <input type="text" class="form-control" id="thread-title" v-model="threadTitle" required>
            </div>
            <div class="mb-3">
              <label for="thread-text" class="form-label">쓰레드 내용</label>
              <textarea class="form-control fixed-textarea" id="thread-text" v-model="threadContent" rows="4"
                required></textarea>
            </div>
            <div class="mb-3">
              <label for="thread-score" class="form-label">쓰레드 점수 (0 ~ 5)</label>
              <input type="number" class="form-control" id="thread-score" v-model="threadScore" min="0" max="5"
                step="0.5" required />
            </div>
            <!-- 2-1. AI 피드백 -->
            <button type="button" class="btn d-inline ai-button" @click="AIFeedBack">AI 피드백</button>

            <!-- 오버레이 + Bootstrap Spinner -->
            <div v-if="loading" class="bootstrap-spinner-overlay">
              <div class="spinner-border text-danger" style="width: 4rem; height: 4rem;" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-if="aiVisible" class="container ai-feedback-container rounded mt-3 mb-1 p-3">
              <h3 class="ai-feedback-title">AI 피드백</h3>
              <div class="ai-result rounded mt-2">
                <span v-for="diff in updatedDiffs"
                  :class="[{ removed: diff.removed, added: diff.added, edited: diff.edited }, 'd-inline']">
                  {{ (diff.selected) ? diff.selectedValue : diff.unselectedValue }}
                </span>
              </div>
              <div class="bg-white rounded mt-2 container flex-column">
                <template v-for="diff in updatedDiffs" :key="diff.idx">
                  <div class="width-100" v-if="diff.added || diff.removed || diff.edited">
                    <input type="checkbox" v-model="diff.selected">
                    <p>{{ diffReason.at(diff.idx) }}</p>
                  </div>
                </template>
              </div>
              <div>
                <button class="btn apply-button" @click.stop="onAiApply">반영하기</button>
              </div>
            </div>

            <button type="submit" class="btn thread-update-button my-3">쓰레드 수정 완료</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, onBeforeRouteLeave, useRouter } from 'vue-router';
import { useBookStore } from '@/stores/books';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';
import { diffChars } from 'diff'


const router = useRouter()
const route = useRoute()
const bookStore = useBookStore()
const accountStore = useAccountStore()
const threadDetail = ref(null)
const threadTitle = ref(null)
const threadContent = ref(null)
const threadScore = ref(null)
const loading = ref(false)

let modal = null
let updateModal = null
let threadUpdateModal = null
const getThreadInfo = () => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/`,
    method: 'get',
  }).then(res => {
    threadDetail.value = res.data
    threadTitle.value = res.data.thread_title
    threadContent.value = res.data.thread_content
    threadScore.value = res.data.thread_book_review_rank
  }).catch(err => {
    console.log(err)
  })
}
onMounted(() => {
  const bootstrap = window.bootstrap
  modal = new bootstrap.Modal(document.getElementById('commentCreate'))
  updateModal = new bootstrap.Modal(document.getElementById('commentUpdate'))
  threadUpdateModal = new bootstrap.Modal(document.getElementById('thread-update-modal'))
  getThreadInfo()
})


// 1. comment section
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
    updateModal.hide()
    getThreadInfo()
  }).catch(err => {
    console.log(err)
  })
}


const onCommentLike = (comment_pk) => {
  if (!accountStore.auth.isAuthenticated) {
    alert('로그인 해주세요!')
    return
  }
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/comments/${comment_pk}/likes/`,
    method: 'post',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    getThreadInfo()
  }).catch(err => {
    console.log(err)
  })
}


// 2. thread update
const onThreadUpdate = () => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/update/`,
    method: 'put',
    data: {
      thread_title: threadTitle.value,
      thread_content: threadContent.value,
      thread_book_review_rank: threadScore.value
    }
  }).then(res => {
    getThreadInfo()
    threadUpdateModal.hide()
  }).catch(err => {
    console.log(err)
  })
}

const toggleThreadLike = () => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/likes/`,
    method: 'post',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    threadDetail.value.thread_likes = res.data.num_likes
  }).catch(err => {
    console.log(err)
  })
}

// 3. thread delete
const onDeleteThread = () => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/update/`,
    method: 'DELETE',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    router.push({ name: 'book-detail', params: { book_pk: route.paramsbook_pk } })
    console.log(res)
  }).catch(err => {
    console.log(err)
  })
}

//4. comment delete
const onCommentDelete = (comment_pk) => {
  axios({
    url: accountStore.API_URL + `/api/v1/books/${route.params.book_pk}/threads/${route.params.thread_pk}/comments/${comment_pk}/`,
    method: 'DELETE',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    console.log(res)
    getThreadInfo()
  }).catch(err => {
    console.log(err)
  })
}

// 5. router push to profile
const onProfileClick = (userPk) => {
  router.push({
    name: 'profile',
    params: {
      userId: userPk
    }
  })
}


// 99. AI feature
const aiResponse = ref('')
const aiVisible = ref(false)
const diffs = ref(null)
const updatedDiffs = ref(null)
const diffReason = ref(null)
const apiKey = import.meta.env.VITE_API_KEY

const AIFeedBack = async () => {
  if (threadContent.value === '') {
    window.alert('Thread를 작성해주세요!')
    return
  }
  loading.value = true
  const systemRole = `
  당신은 작성된 글의 문법적 오류 및 잘못된 표현을 수정하는 AI입니다.
  입력받은 text를 기반으로 수정된 글을 반환해주세요.
  수정된 글 외의 응답을 해서는 안됩니다.
  만약에 입력된 내용이 없다면, 0을을 응답해주시면 됩니다.
  `
  try {
    const res = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4o-mini', // 또는 gpt-4
        messages: [
          { role: 'system', content: systemRole },
          { role: 'user', content: threadContent.value }
        ],
        temperature: 0.7
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`, // 여기에 본인 키 입력
          'Content-Type': 'application/json'
        }
      }
    )

    aiResponse.value = res.data.choices[0].message.content.trim()
    diffs.value = diffChars(threadContent.value, aiResponse.value)
    updatedDiffs.value = updateDiff()
    AIFeedBackListup()
  } catch (err) {
    console.error('API 호출 오류:', err)
    loading.value = false
  }
}

const AIFeedBackListup = async () => {
  const systemRole = `
  당신은 json 배열을 입력으로 받아 각 객체의 원인을 앞 뒤의 json과 현재의 json을 바탕으로 원인을 분석해야 합니다.
  다음은 예시입니다.
  입력
[
  {
    "edited": false,
    "added": false,
    "removed": false,
    "value": "『데미안』은 자아를 찾아가는 청년의 성장 여정을 담은 철학적 소설입니다. 주인공 싱클레어는 선과 악, 빛과 어둠의 경계를 넘나들며 "
  },
  {
    "edited": true,
    "added": true,
    "removed": false,
    "value": "스스",
    "prevValue": "쓰쓰"
  },
  {
    "edited": false,
    "added": false,
    "removed": false,
    "value": "로의 "
  },
  {
    "edited": true,
    "added": true,
    "removed": false,
    "value": "내",
    "prevValue": "냬"
  },
  {
    "edited": false,
    "added": false,
    "removed": false,
    "value": "면을 "
  },
  {
    "edited": false,
    "added": false,
    "removed": true,
    "value": "ㅈ"
  },
  {
    "edited": false,
    "added": false,
    "removed": false,
    "value": "직면하고 성장해 갑니다. 현실의 질서에 안주하지 않고 ‘나"
  },
  {
    "edited": false,
    "added": false,
    "removed": true,
    "value": "ㅏ"
  },
  {
    "edited": false,
    "added": false,
    "removed": false,
    "value": "만의 길’을 찾으려는 그의 모습은 현대 독자에게도 깊은 울림을 줍니다. 특히 데미안과의 만남은 싱클레어가 기존 가치관에서 벗어나 진정한 자아로 나아가는 계기가 됩니다. 인간 내면의 이중성과 삶의 본질을 진지하게 성찰하게 만드는 작품으로, 한 번쯤 삶의 의미를 고민해본 이들에게 강력히 추천하고 싶습니다. 정말로요."
  }
]
  응답
  [
  "",
  "문법 오류를 수정하였습니다.",
  "",
  "타이핑 오류를 수정하였습니다.",
  "",
  "타이핑 오류를 수정하였습니다.",
  "",
  "타이핑 오류를 수정하였습니다"'
  "",
  "타이핑 오류를 수정하였습니다.",
  "",
  ]
  edited가 true인 value와 prevValue의 값을 비교하여 원인을 작성하면 되고,
  added 혹은 removed가 true인 경우에는 value값을 기반으로 왜 삭제 / 추가되었는지를 작성하면 됩니다.
  마지막으로 edited, added, removed 세개가 모두 false인 경우에는 빈 문자열을 작성하면 됩니다.
  `
  try {
    const res = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4o-mini', // 또는 gpt-4
        messages: [
          { role: 'system', content: systemRole },
          { role: 'user', content: JSON.stringify(updatedDiffs.value) }
        ],
        temperature: 0.7
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`, // 여기에 본인 키 입력
          'Content-Type': 'application/json'
        }
      }
    )

    const temp = res.data.choices[0].message.content.trim()
    diffReason.value = JSON.parse(temp)
    console.log(diffReason.value)
    aiVisible.value = true
    console.log(diffReason.value)
    console.log(updatedDiffs.value)
    loading.value=false
  } catch (err) {
    console.error('API 호출 오류:', err)
    loading.value=false
  }
}

const updateDiff = () => {
  const result = []
  let idx = 0
  let i = 0
  while (idx < diffs.value.length) {
    const obj = diffs.value.at(idx)
    // 0. 마지막 요소 -> 판단 필요 x
    if (idx === diffs.value.length - 1) {
      let temp = null
      if (!obj.added && !obj.removed) {
        temp = {
          "idx": i,
          "edited": false,
          "added": obj.added,
          "removed": obj.removed,
          "value": obj.value,
          "selected": true,
          "selectedValue": obj.value,
          "unselectedValue": obj.value,
        }
      }
      else {
        temp = {
          "idx": i,
          "edited": false,
          "added": obj.added,
          "removed": obj.removed,
          "value": obj.value,
          "selected": true,
          "selectedValue": obj.added ? obj.value : "",
          "unselectedValue": obj.added ? "" : obj.value
        }
      }
      result.push(temp)
    }
    // 1. 수정 안됨
    else if (obj.removed === false && obj.added === false) {
      const temp = {
        "idx": i,
        "edited": false,
        "added": obj.added,
        "removed": obj.removed,
        "value": obj.value,
        "selected": true,
        "selectedValue": obj.value,
        "unselectedValue": obj.value,
      }
      result.push(temp)
    }
    // 2. 추가된 경우 -> 그냥 바로 push
    else if (obj.added === true) {
      const temp = {
        "idx": i,
        "edited": false,
        "added": obj.added,
        "removed": obj.removed,
        "value": obj.value,
        "selected": true,
        "selectedValue": obj.added ? obj.value : "",
        "unselectedValue": obj.added ? "" : obj.value
      }
      result.push(temp)
    }
    // 3. 삭제된 경우 -> 다음 요소 보고 추가된 거면 묶어서 push
    else {
      const nextObj = diffs.value.at(idx + 1)
      if (nextObj.added === true) {
        idx += 1
        const temp = {
          "idx": i,
          "edited": true,
          "added": false,
          "removed": false,
          "value": nextObj.value,
          "prevValue": obj.value,
          "selected": true,
          "selectedValue": nextObj.value,
          "unselectedValue": obj.value,
        }
        result.push(temp)
      }
      else {
        const temp = {
          "idx": i,
          "edited": false,
          "added": obj.added,
          "removed": obj.removed,
          "value": obj.value,
          "selected": true,
          "selectedValue": obj.added ? obj.value : "",
          "unselectedValue": obj.added ? "" : obj.value,
        }
        result.push(temp)
      }
    }
    idx += 1
    i += 1
  }
  return result
}

const onAiApply = () => {
  let result = ""
  for (const obj of updatedDiffs.value) {
    result += (obj.selected) ? obj.selectedValue : obj.unselectedValue
  }
  threadContent.value = result
  aiResponse.value = ''
  aiVisible.value = false
  diffs.value = null
  updatedDiffs.value = null
  diffReason.value = null
}

onBeforeRouteLeave((to, from) => {
  aiVisible.value = false
})


// 00. AI 피드백 버튼 클릭 시 로딩
// import { useUiStore } from '@/stores/ui.js'
// import Spinner from '@/components/layout/Spinner.vue'

// const ui = useUiStore()

// async function runAIFeedback() {
//   await new Promise(res => setTimeout(res, 2000))
// }

// async function AIFeedBackLoad() {
//   ui.setLoading(true)
//   try {
//     await runAIFeedback()
//   } finally {
//     ui.setLoading(false)
//   }
// }
</script>


<style scoped>
main {
  margin: 100px 200px 70px;
  padding-top: 100px 50px;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -1px;
  color: white;
  text-align: left;
}

.thread-container {
  width: 1000px;
  min-width: 1000px;
  max-width: 1000px;
  margin: 40px auto 0 auto;
  padding: 0;
}

.thread-card {
  background: rgba(255, 255, 255, 0.5);
}

/* .card-text {
  출간일, 평균 평점 있는 쪽!
} */
hr {
  margin: 8px 0px 16px;
}


.like-button {
  background-color: transparent;
  border-color: #ff2c54;
  color: #ff2c54;
}


.comment-create-button {
  background-color: transparent;
  border-color: #ff2c54;
  color: #ff2c54;
}

.comment-create-button:hover {
  background-color: #ff2c54;
  border: #ff2c54;
  color: white;
  box-shadow: 0 2px 12px 0 #ccc;
  ;
}

.comment-count {
  color: whitesmoke;
  margin: 10px 2px;
  font-size: medium;
}


.create-finish-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.create-finish-button:active {
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

.ai-button {
  border-color: #ff2c54;
  color: #ff2c54;
  width: 100%;
}

.thread-update-button {
  background-color: #ff2c54;
  border: none;
  color: white;
  width: 100%;
}

.thread-update-button:active {
  background-color: #df0c34;
  color: white;
}

.added {
  color: green;
}

.removed {
  color: red;
  text-decoration: line-through;
}

.edited {
  background-color: pink;
}

.thread-submit {
  background-color: lightgrey;
}

.user-info {
  cursor: pointer;
}

.ai-feedback-container {
  border: 1px solid #ff2c54;
}

.ai-feedback-title {
  color: #ff2c54;
}

.ai-result {
  background-color: blanchedalmond;
  /* border-bottom: 1px solid #ff2c54; */
  padding: 5px 10px 5px 15px;
}

.apply-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.bootstrap-spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.comment-update-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.comment-update-button:active {
  background-color: #df0c34;
  color: white;
}
</style>