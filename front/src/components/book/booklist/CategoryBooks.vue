<template>
  <section>
    <h3>카테고리별 도서</h3>
    <div class="categories">
      <!-- 카테고리별로 선택할 수 있는 버튼 생성 -->
      <button
        v-for="category in categories"
        :key="category.pk"
        @click="selectCategory(category.pk)"
      >
        {{ category.fields.name }}
      </button>
      <BookList 
        :books="filteredBooks"
      />
    </div>
  </section>
</template>


<script setup>
import { ref, watch } from 'vue'
import BookList from '@/components/book/BookList.vue'

const props = defineProps({
  categories: Array,
  books: Array,
  carouselId: String
})

const selectedCategory = ref(0)           // 선택된 카테고리: id로 구분, 0은 전체 의미
const filteredBooks = ref(props.books)    // 현재 선택된 카테고리에 맞는 도서 배열

// selectedCategory 또는 props.books(전체 도서 목록 배열)가 바뀔 때마다(즉, 카테고리가 바뀔 때마다) 필터링
watch (
  // 1) 감시 대상: 두 값 중 하나라도 바뀌면 watch의 콜백 함수실행
  () => [selectedCategory.value, props.books],
  // 2) 콜백 함수
  () => {
    // 2-1) selectedCategory가 0이면(= "전체" 카테고리 선택 시) 
    // -> 모든 책을 filteredBooks에 할당
    if (selectedCategory.value === 0) {
      filteredBooks.value = props.books
    }
    // 2-2) 그렇지 않으면(= 특정 카테고리 선택 시) 
    // -> books 배열에서 각 book의 category가 선택된 카테고리와 같은 책들만 골라 filteredBooks에 할당
    else {
      filteredBooks.value = props.books.filter(
        // book은 props.books 배열의 각 요소(책 한권)
        book => book.fields.category === selectedCategory.value
      )
    }
  },
  // watch가 등록되자마자(컴포넌트 마운트 시) 콜백 함수 한 번 바로 실행 -> 초기 렌더링 시에도 filteredBooks가 올바르게 세팅됨.
  { immediate: true }
)

// "selected"Category 반응형 변수랑 다른 이름!!! 함수는 "select"
function selectCategory(categoryId) {
  selectedCategory.value = categoryId
}
</script>


<style scoped>

</style>