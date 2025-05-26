<template>
  <!-- 책 데이터가 있을 때만 캐러셀 렌더링 / id는 캐러셀 컨트롤과 연결 -->
  <div v-if="books && books.length" :id="carouselId" class="carousel slide">
    <!-- 캐러셀 내부 영역 -->
    <div class="carousel-inner">
      <!-- 첫번째 슬라이드 덩어리(idx===0)에만 active를 붙여서 기본으로 첫 덩어리만 보이도록 함. -->
      <div 
        v-for="(chunk, idx) in chunkedBooks" 
        :key="idx" 
        :class="['carousel-item', { active: idx === 0 }]"
      >
        <div class="d-flex justify-content-center gap-3 py-3">
          <BookCardVer 
            v-for="book in chunk" 
            :key="book.pk" 
            :book="book" 
          />
        </div>
      </div>
    </div>

    <!-- 캐러셀 컨트롤(좌우 이동 버튼) -->
    <button class="carousel-control-prev" type="button" :data-bs-target="'#'+carouselId" data-bs-slide="prev">
      <span class="carousel-control-prev-icon"></span>
      <!-- 아래는 접근성을 높이기 위한 스크린 리더용 기능 -> 텍스트가 읽혀 시각장애인도 접근 가능 -->
      <span class="visually-hidden">이전</span>
    </button>
    <button class="carousel-control-next" type="button" :data-bs-target="'#'+carouselId" data-bs-slide="next">
      <span class="carousel-control-next-icon"></span>
      <span class="visually-hidden">다음</span>
    </button>
  </div>

  <!-- 책 데이터가 없을 때(로딩 전 or 비어있을 때) 표시될 안내 문구 -->
  <div v-else class="text-center py-5 text-muted">도서가 없습니다.</div>
</template>


<script setup>
import { computed, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import BookCardVer from '@/components/card/BookCardVer.vue'

const store = useBookStore()

const props = defineProps({
  books: {
    type: Array,
    default: () => []
  },
  carouselId: {
    type: String,
    required: true
  }
})

// 한 슬라이드에 5개씩 보이도록 books 배열 분할
const chunkedBooks = computed(() => {
  const size = 5
  const arr = []
  for (let i = 0; i < props.books.length; i += size) {
    arr.push(props.books.slice(i, i + size))
  }
  return arr
})
</script>


<style scoped></style>




<!-- <template>
  <div>
    <h5>북 리스트 템플릿</h5>
    <BookCardVer 
      v-for="book in books"
      :key="book.pk"
      :book="book"
      @click-card="goToBookDetail(book.pk)"
    />
  </div>
</template>


<script setup>
import { useRouter } from 'vue-router'
import BookCardVer from '../card/BookCardVer.vue';

const props = defineProps({
  books: Array,
})

const router = useRouter()
function goToBookDetail(pk) {
  router.push({ name: 'book-detail', params: { book_pk: pk }})
}
</script>


<style scoped>

</style> -->