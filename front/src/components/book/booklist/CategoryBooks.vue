<template>
  <section>
    <h3>카테고리별 도서</h3>
    <!-- 카테고리별로 버튼... -->
  </section>
</template>


<script setup>
import { ref, watch } from 'vue'
import BookList from '../BookList.vue';

const props = defineProps({
  categories: Array,
  books: Array,
})

const selectedCategory = ref(0)           // 선택된 카테고리: id로 구분, 0은 전체 의미
const filteredBooks = ref(props.books)    // 현재 선택된 카테고리에 맞는 도서 배열

// selectedCategory 또는 props.books가 바뀔 때마다(즉, 카테고리가 바뀔 때마다) 필터링
watch (
  // 감시 대상
  () => [selectedCategory.value, props.books],
  // 필터링
  () => {
    if (selectedCategory.value === 0) {
      filteredBooks.value = props.books
    }
    else {
      filteredBooks.value = props.books.filter(
        // book => book.fields.
      )
    }
  }
)
</script>


<style scoped>

</style>