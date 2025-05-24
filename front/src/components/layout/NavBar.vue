<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <!-- 왼쪽: 로고(메인 페이지) -->
      <RouterLink :to="{ name: 'main-page' }" class="nav-link" active-class="active">
        <img src="/src/assets/LOGO.png" alt="logo_img.png" id="logo">
      </RouterLink>

      <!-- 토글 버튼(작은 화면용) -->
      <button 
        class="navbar-toggler" type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#toggleContent"
        aria-controls="toggleContent" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 오른쪽: [로그인X] 회원가입, 로그인, 검색 / [로그인O] 회원가입(회원도 보이는게 맞겠지?), 프로필, 검색 -->
      <div class="collapse navbar-collapse" id="toggleContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex align-items-center">
          <li class="nav-item">
            <RouterLink :to="{ name: 'signup' }" class="nav-link" active-class="active">
              회원가입
            </RouterLink>
          </li>

          <!-- **v-if 써서 로그인 여부에 따라 "로그인or프로필" 구현해야함!! -->
          <li class="nav-item">
            <RouterLink :to="{ name: 'login' }" class="nav-link" active-class="active">
              로그인
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'profile' }" class="nav-link" active-class="active">
              프로필
            </RouterLink>
          </li>

          <!-- 검색 폼 (나중에 버튼 색 조정해주기) -->
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </ul>
      </div>
    </div>
  </nav>
</template>


<script setup>
// 별도 스크립트 없이 router만 사용 중!
</script>


<style scoped>
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


/* .nav-item {
  height: 25px;
  padding: 10px;
  display: flex;
  align-items: center;
  font-weight: 500;
} */

/* 기본 메뉴 스타일: 일반 텍스트처럼 보이기 */
/* cursor: default; -> 화살표를 올려도 포인터(링크용 손 모양)가 아니라 일반 화살표(텍스트용)처럼 보이게 함. */
/* .nav-link {
  color: #ccc;
  font-size: 20px;
  font-weight: 500;
  cursor: default;
} */

/* 현재 선택된 메뉴 빨간색 강조 */
.nav-link.active {
  /* color: #dc3545; */
  color: #FF0000;
  /* 로고랑 통일하고 싶어서 추출한 빨간색(#FF0000)인데 너무 쨍한가.. */
}

/* 비활성 상태일 때 hover 효과 */
.nav-link:not(.active):hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ccc;
  cursor: pointer;
}
</style>