<template>
  <div class="container py-3">
    <div class="thread-card-header">
      <h2 class="mb-0">Threads List</h2>
      <!-- 쓰레드 작성 버튼 -->
      <div v-if="accountStore.auth.isAuthenticated">
        <button type="button" class="btn thread-write-button" data-bs-toggle="modal" data-bs-target="#threadCreateModal">
          쓰레드 작성
        </button>
      </div>
    </div>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary mb-3" role="status"></div>
      <h2 class="text-muted">로딩 중...</h2>
    </div>

    <!-- 쓰레드 목록 -->
    <div v-else>
      <h3 v-if="threads.length === 0" class="no-thread-txt">쓰레드가 없어요...</h3>
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
          <img src="@/assets/LOGO.png" alt="로고" class="mb-3" style="max-height: 60px;" />
          <h1 class="modal-title fs-4">쓰레드 작성</h1>
          <button type="button" class="btn-close position-absolute top-0 end-0 m-3" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>

        <!-- 모달 바디 -->
        <div class="modal-body">
          <hr class="mt-0">
          <form @submit.prevent="onSubmit">
            <div class="mb-3">
              <label for="thread-title" class="form-label">쓰레드 제목</label>
              <input type="text" class="form-control" id="thread-title" v-model="title" required>
            </div>

            <div class="mb-3">
              <label for="thread-text" class="form-label">쓰레드 내용</label>
              <textarea class="form-control fixed-textarea" id="thread-text" v-model="content" rows="4"
                required></textarea>
            </div>

            <div class="mb-3">
              <label for="thread-score" class="form-label">쓰레드 점수 (0 ~ 5)</label>
              <input type="number" class="form-control" id="thread-score" v-model="score" min="0" max="5" step="0.5"
                required />
            </div>

            <button type="button" class="btn ai-button d-inline" @click="AIFeedBack">AI 피드백</button>
            <div v-if="aiVisible" class="container rounded p-2 bg-info">
              <h3>AI 피드백</h3>
              <div class="bg-white rounded mt-2">
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
                <button class="btn btn-outline-success" @click.stop="onAiApply">반영하기</button>
              </div>
            </div>
            <button type="submit" class="btn my-3 create-finish-button">쓰레드 생성</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, onBeforeRouteLeave } from 'vue-router';
import { useBookStore } from '@/stores/books';
import { useAccountStore } from '@/stores/accounts';
import { diffChars } from 'diff'
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

// 99. AI
const aiResponse = ref('')
const aiVisible = ref(false)
const diffs = ref(null)
const updatedDiffs = ref(null)
const diffReason = ref(null)
const apiKey = import.meta.env.VITE_API_KEY

const AIFeedBack = async () => {
  if (content.value === '') {
    window.alert('Thread를 작성해주세요!')
    return
  }

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
          { role: 'user', content: content.value }
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
    diffs.value = diffChars(content.value, aiResponse.value)
    updatedDiffs.value = updateDiff()
    AIFeedBackListup()
  } catch (err) {
    console.error('API 호출 오류:', err)
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
  } catch (err) {
    console.error('API 호출 오류:', err)
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
  content.value = result
  aiResponse.value = ''
  aiVisible.value = false
  diffs.value = null
  updatedDiffs.value = null
  diffReason.value = null
}

onBeforeRouteLeave((to, from) => {
  aiVisible.value = false
})
</script>


<style scoped>
.thread-card-header {
  color: #f0f0f0;
  margin-bottom: 10px;
  padding-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
}
.no-thread-txt {
  color: #ccc;
  padding-top: 30px;
}

.modal-title.fs-4 {
  font-size: 1.5em !important;
}
.modal-content {
  width: 1000px;
}

.thread-write-button {
  background-color: transparent;
  border-color: #ccc;
  color: #ccc;
}
.thread-write-button:hover {
  background-color: #df0c34;
  border: #df0c34;
  box-shadow: 0 2px 12px 0 #ccc;;
}

.ai-button {
  border-color: #ff2c54;
  color: #ff2c54;
  width: 100%;
}

.create-finish-button {
  background-color: #ff2c54;
  border: none;
  color: white;
  width: 100%;
}

.create-finish-button:active {
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