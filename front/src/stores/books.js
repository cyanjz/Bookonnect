import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


// #1. MainPageView 내의 도서 store
export const useBookStore = defineStore('book', () => {
  // 1. 상태 정의
  const books = ref([])
  const categories = ref([])

  const bestSellers = ref([])
  const recommendedBooks = ref([])
  const highRankBooks = ref([])

  const isLoading = ref(false)
  const error = ref(null)


  // 2. API URL
  const API_URL = 'http://127.0.0.1:8000'


  // 3. books 데이터 가져오기
  // 3-1 .백엔드 API에서 전체 책 목록 데이터를 가져와(응답받아) store의 book.value에 저장
  const getBooks = async () => {
    isLoading.value = true
    error.value = null

    // 비동기적으로 처리
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books`
    })
      .then(res => {
        books.value = res.data
      })
      .catch(err => {
        console.log(err)
        error.value = err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  // 3-2. 프론트엔드 store에 이미 저장된 책 목록(books.value)에서 특정 id(pk)에 해당하는 책 한 권을 찾아 반환
  const findBook = bookId => {
    const intId = Number(bookId)
    return books.value.find((book) => book.pk === intId)
  }

  // 3-3. 프론트엔드 store에 이미 저장된 책 목록(books.value)에서 특정 카테고리의 책들만 필터링해서 반환(추출)
  const filterBooks = categoryId => {
    const intId = Number(categoryId)
    // 전체 카테고리를 선택한 경우
    if (intId === 0) {
      return books.value    // 모든 책 배열 그대로 반환
    }
    // books.value에서 각 book의 카테고리 id(fields.category)가 intId와 같은 책들만 골라 새로운 배열로 반환
    return books.value.filter((book) => book.fields.category === intId)
  }


  // **아래는 백엔드에 경로를 따로 추가해주던가 해야함!!
  // 4. Best Sellers
  const getBestSellers = async () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/bestsellers`
    })
      .then(res => {
        bestSellers.value = res.data
      })
      .catch(err => {
        console.log(err)
        error.value = err
      })
  }


  // 5. Recommended Books
  const getRecommendedBooks = async () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/recommend`
    })
      .then(res => {
        recommendedBooks.value = res.data
      })
      .catch(err => {
        console.log(err)
        error.value = err
      })
  }


  // 6. Categories 
  // => 카테고리(장르?)별로 다양하므로 버튼으로 카테고리를 고르도록 할 예정
  const getCategories = async () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/categories`
    })
      .then(res => {
        categories.value = res.data
      })
      .catch(err => {
        console.log(err)
        error.value = err
      })
  }


  // 7. High Rank Books
  const getHighRankBooks = async () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/highrank`
    })
      .then(res => {
        highRankBooks.value = res.data
      })
      .catch(err => {
        console.log(err)
        error.value = err
      })
  }



  return {
    books,
    categories,
    bestSellers,
    recommendedBooks,
    highRankBooks,
    isLoading,
    error,

    API_URL,

    getBooks,
    findBook,
    filterBooks,

    getBestSellers,
    getRecommendedBooks,
    getCategories,
    getHighRankBooks,
  }
}, { persist: true })



// #2. BookDetailView 내의 도서 정보
export const useBookDetailStore = defineStore('bookDetail', () => {
  const book = ref(null)
  const author = ref(null)
  const threads = ref([])
  const error = ref(null)

  const API_URL = 'http://127.0.0.1:8000'

  // 1. BookInfo: 단일 책 상세 정보
  const getBookInfo = (bookId) => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/${bookId}/`
    })
      .then(res => {
        book.value = res.data; 
        return res.data
      })
      .catch(err => {
        error.value = err
      })
  }


  // 2. AuthorInfo: 작가 정보
  const getAuthorInfo = (authorId) => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/authors/${authorId}/`
    })
      .then(res => { 
        author.value = res.data; 
        return res.data 
      })
      .catch(err => { 
        error.value = err 
      })
  }


  // 3. ThreadThumbnail: 쓰레드 목록
  const getThreads = (bookId) => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/${bookId}/threads/`
    })
      .then(res => { 
        threads.value = res.data; 
        return res.data 
      })
      .catch(err => { 
        error.value = err 
      })
  }

  return {
    book,
    author,
    threads,
    error,

    getBookInfo,
    getAuthorInfo,
    getThreads,
  }
}, { persist: true })