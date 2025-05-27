<template>
  <main class="container py-4 bg-white">
    <!-- 헤더: 제목 + 보기 방식 버튼 -->
    <header class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="fw-bold fs-4">검색 결과</h1>
      <div>
        <button class="btn btn-outline-secondary me-2" :class="{ active: viewType === 'grid' }"
          @click="viewType = 'grid'">
          <i class="bi bi-grid"></i>
        </button>
        <button class="btn btn-outline-secondary" :class="{ active: viewType === 'list' }" @click="viewType = 'list'">
          <i class="bi bi-list"></i>
        </button>
      </div>
    </header>

    <div class="row">
      <!-- 필터 영역 -->
      <aside class="col-md-2 mb-4">
        <div class="fw-bold mb-2">필터</div>
        <div class="form-check" v-for="i in selected.length" :key="i">
          <input class="form-check-input" type="checkbox" :id="'filter' + i" v-model="selected[i-1]">
          <label class="form-check-label" :for="'filter' + i">
            {{ filterOptions[i-1].category_name }}
          </label>
        </div>
      </aside>

      <!-- 도서 리스트 -->
      <section class="col-md-10" v-if="filteredBooks">
        <div v-if="filteredBooks.length === 0" class="text-muted py-5 text-center">
          검색 결과가 없습니다.
        </div>
        <div v-else>
          <!-- 리스트형 보기 -->
          <div v-if="viewType === 'list'">
            <div v-for="book in filteredBooks" :key="book.book_ISBN13"
              class="d-flex align-items-start mb-4 pb-3 border-bottom book-elem" @click="onClickCard(book.pk)">
              <div style="width: 90px; height: 130px; background: #d1d5db;" class="me-4 flex-shrink-0 rounded">
                <img :src="bookStore.API_URL + book.book_cover_img" alt="cover" class="img-fluid h-100 w-100 object-fit-cover rounded"
                  v-if="book.book_cover_img" />
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold">{{ book.book_title }}</div>
                <div class="text-muted small mb-1">{{ book.book_publisher }}</div>
                <div class="text-muted small mb-1">{{ book.book_pub_date }}</div>
                <div class="text-muted small mb-2">{{ book.book_description.slice(0, 40) }}...</div>
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-bookmark-heart" title="북마크"></i>
                  <!-- <i class="bi bi-chat" title="리뷰"></i> -->
                </div>
              </div>
            </div>
          </div>
          <!-- (참고) 그리드형 보기 예시: viewType === 'grid'일 때 카드형으로 배치 -->
          <div v-else class="row row-cols-1 row-cols-md-3 g-4">
            <div v-for="book in filteredBooks" :key="book.book_ISBN13" class="col book-elem" @click="onClickCard(book.pk)">
              <div class="card h-100">
                <img :src="bookStore.API_URL + book.book_cover_img" class="card-img-top" alt="cover"
                  style="height: 180px; object-fit: cover;">
                <div class="card-body">
                  <h5 class="card-title">{{ book.book_title }}</h5>
                  <h6 class="card-subtitle text-muted mb-2">{{ book.book_publisher }}</h6>
                  <p class="card-text small">{{ book.book_description.slice(0, 40) }}...</p>
                </div>
                <div class="card-footer d-flex gap-2">
                  <i class="bi bi-bookmark-heart"></i>
                  <!-- <i class="bi bi-chat"></i> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>


<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import axios from 'axios'


const bookStore = useBookStore()
const route = useRoute()
const router = useRouter()
const bookList = ref(null)
const viewType = ref('grid')

const filterOptions = ref(bookStore.categories)
const selected = ref(new Array(filterOptions.value.length).fill(true))

const filteredBooks = computed(() => {
  if (bookList.value && filterOptions.value) {
    const selectedCategories = filterOptions.value.filter((obj, index) => selected.value[index] === true).map(obj => obj.id)
    return bookList.value.filter(obj => selectedCategories.includes(obj.category))
  }
  else {
    return null
  }
})

onMounted(() => {
  axios({
    url: bookStore.API_URL + `/api/v1/books/search/`,
    method: 'get',
    params: {
      q: route.query.q
    }
  }).then(res => {
    bookList.value = res.data
  }).catch(err => {
    console.log(err)
  })
})

const onClickCard = (bookPk) => {
  router.push({
    name: 'book-detail',
    params: {
      'book_pk': bookPk
    }
  })
}
</script>


<style scoped>
.book-elem {
  cursor: pointer
}


main {
  margin-top: 100px;
}
</style>