<template>
  <nav :class="['navbar', 'navbar-expand-lg', { dark: isDark }]">
    <div class="container-fluid">
      <!-- 왼쪽: 로고(메인 페이지) -->
      <RouterLink :to="{ name: 'main-page' }" class="nav-link" active-class="active">
        <img :src="isDark ? '/src/assets/LOGO_white.png' : '/src/assets/LOGO.png'" alt="logo_img.png" id="logo">
      </RouterLink>

      <!-- 토글 버튼(작은 화면용) -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#toggleContent"
        aria-controls="toggleContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 오른쪽: [로그인X] 회원가입, 로그인, 검색 / [로그인O] 프로필, 로그아웃, 검색 -->
      <!-- **v-if 써서 로그인 여부에 따라 navbar 메뉴를 다르게 구현해야함!! -->
      <div class="collapse navbar-collapse" id="toggleContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex align-items-center">
          <template v-if="!accountStore.auth.isAuthenticated">
            <li class="nav-item">
              <button type="button" class="nav-link" data-bs-toggle="modal" data-bs-target="#signUpModal"
                data-bs-whatever="@mdo">회원가입</button>
            </li>
            <li class="nav-item">
              <button type="button" class="nav-link" data-bs-toggle="modal" data-bs-target="#logInModal"
                data-bs-whatever="@mdo">로그인</button>
            </li>
          </template>
          <template v-if="accountStore.auth.isAuthenticated">
            <li class="nav-item">
              <RouterLink :to="{ name: 'profile', params: { userId: accountStore.auth.userPk } }" class="nav-link"
                active-class="active">
                내 프로필
              </RouterLink>
            </li>
            <li class="nav-item">
              <button type="button" class="nav-link" @click="onLogOut">
                로그아웃
              </button>
            </li>
          </template>

          <!-- 검색 폼 -->
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
            <button class="search-btn" type="submit">
              <img 
                :src="btnSrc" alt="Search" class="search-icon"
                :class="{ 'fade': isFading }"
                @mouseover="handleSearchMouseOver"
                @mouseout="handleSearchMouseOut"
              >
            </button>
          </form>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Login form -->
  <LogInForm />
  <SignUpForm />
</template>


<script setup>
// 별도 스크립트 없이 router만 사용 중!
import LogInForm from '@/components/form/LogInForm.vue'
import SignUpForm from '@/components/form/SignUpForm.vue';
import { useAccountStore } from '@/stores/accounts';
const accountStore = useAccountStore()

const onLogOut = () => {
  accountStore.logOut()
}

import { ref, onMounted, onUnmounted, watch } from 'vue'
// 1. 검색 버튼 호버 시 이미지가 바뀌도록!
const defaultBtn = '/src/assets/magnifier_icon.png'
const hoverBtn = '/src/assets/magnifier_icon_red.png'
const btnSrc = ref(defaultBtn)

const darkDefaultBtn = '/src/assets/magnifier_icon_white.png'      // 어두운 배경에서 쓸 검색아이콘
const darkHoverBtn = '/src/assets/magnifier_icon_red.png'    // 어두운 배경에서 호버



// 2. 스크롤 시 navbar의 글씨색/검색버튼 이미지가 바뀌도록!
// 스크롤에 따라 다크/라이트 모드
const isDark = ref(false)

const getDarkThreshold = () => window.innerHeight * 0.2

const handleScroll = () => {
  isDark.value = window.scrollY > getDarkThreshold()
}

// 다크모드에서 호버 후에도 흰색 이미지가 디폴트값(검은색 이미지)으로 바뀌지 않도록
// + 호버 시 좀 더 부드럽게 전환되도록
const isFading = ref(false)
const fadeBtnImg = (newSrc) => {
  isFading.value = true
  setTimeout(() => {
    btnSrc.value = newSrc
    isFading.value = false
  }, 120)
}

const handleSearchMouseOver = () => {
  fadeBtnImg( isDark.value ? darkHoverBtn : hoverBtn )
}
const handleSearchMouseOut = () => {
  fadeBtnImg(isDark.value ? darkDefaultBtn : defaultBtn) 
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('resize', handleScroll) // 창 크기 바뀔 때도 반영
  handleScroll() // 초기 상태 반영
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleScroll)
})

watch(isDark, (val) => {
  fadeBtnImg(val ? darkDefaultBtn : defaultBtn)
})
</script>


<style scoped>
nav {
  position: sticky;
  /* sticky 상태에서 위쪽에 고정되도록 */
  top: 0;
  /* 스크롤 시 다른 컴포넌트보다는 앞에 오도록 + 회원가입/로그인 모달 창보다는 뒤에 오도록 */
  z-index: 20;
}

#logo {
  height: 50px;
  width: auto;
  align-items: center;
}

/* 메뉴 항목 정렬용 */
.navbar-nav .nav-item {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}


.search-icon {
  height: 40px;
  width: auto;
  padding: 0px;
}

.search-btn {
  border: none;
  background-color: transparent;
}


/* 현재 선택된 메뉴 빨간색 강조 */
.nav-link.active {
  color: #FF0000;
}

/* 비활성 상태일 때 hover 효과 */
.nav-link:not(.active):hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #FF0000;
  cursor: pointer;
}


/* 스크롤 시 네비게이션 바 메뉴들 글씨 색 변경 */
/* 기본(라이트) 모드 */
.nav-link,
.form-control {
  color: #222;
  transition: color 0.3s;
}

/* 다크 모드 */
nav.dark .nav-link,
nav.dark .form-control {
  color: #fff;
}


/* 스크롤 시 네비게이션 바 색상 변경 */
/* 기본(라이트) 모드 */
.navbar {
  background-color: transparent;
  /* 부드럽게 전환 */
  transition: background-color 0.4s, box-shadow 0.4s;
  box-shadow: none;
}

/* 다크 모드 */
.navbar.dark {
  background-color: #111;
  /* box-shadow: 0 2px 16px 0 rgba(0,0,0,0.08); */
}
</style>