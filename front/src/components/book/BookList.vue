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
            class="custom-book-card"
          />
        </div>
      </div>
    </div>

    <!-- 캐러셀 컨트롤(좌우 이동 버튼) -->
    <button class="carousel-control-prev custom-carousel-control" type="button" 
      :data-bs-target="'#'+carouselId" data-bs-slide="prev">
      <span class="carousel-control-prev-icon"></span>
      <!-- 아래는 접근성을 높이기 위한 스크린 리더용 기능 -> 텍스트가 읽혀 시각장애인도 접근 가능 -->
      <span class="visually-hidden">이전</span>
    </button>
    <button class="carousel-control-next custom-carousel-control" type="button" 
      :data-bs-target="'#'+carouselId" data-bs-slide="next">
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


<style scoped>
/* 화면이 작아져도 캐러셀 컨트롤 버튼이 도서 영역에 겹치지 않도록 */
/* 캐러셀 전체에 좌우 패딩 추가 (버튼 공간 확보) */
.custom-carousel {
  position: relative;
  padding: 0 60px; /* 버튼 공간 확보 */
}

/* 컨트롤 버튼을 캐러셀 바깥쪽에 위치시키기 */
.custom-carousel-control {
  width: 48px;
  height: 48px;
  top: 50%;
  transform: translateY(-50%);
}

.carousel-control-prev.custom-carousel-control {
  left: -24px; /* 캐러셀 바깥쪽으로 */
}

.carousel-control-next.custom-carousel-control {
  right: -24px; /* 캐러셀 바깥쪽으로 */
}

/* 반응형: 화면이 작아지면 버튼이 겹치지 않도록 위치 조정 */
@media (max-width: 768px) {
  .custom-carousel {
    padding: 0 20px;
  }
  .carousel-control-prev.custom-carousel-control,
  .carousel-control-next.custom-carousel-control {
    left: 0;
    right: 0;
  }
}


/* 북카드 크기 조정 */
.custom-book-card {
  min-width: 180px;
  max-width: 220px;
  flex: 1 1 180px;
}
</style>
