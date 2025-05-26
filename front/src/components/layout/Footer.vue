<template>
  <div id="wrap">
    <!-- footer가 항상 하단에 고정되도록 wrap 사용 -> 유일한 wrap이므로 id로 부여 -->
    <footer>
      <img src="@/assets/LOGO_white.png" alt="logo_img.png">
      <nav>
        <a href="https://www.notion.so/isaacshin/1e4469106168806d96ccc85906cb9c1d">
          Notion</a>
        <span> | </span>
        <a href="https://www.figma.com/design/KOCRExKa4dtO6s1nEGjOuw/UI-UX-Design?node-id=0-1&t=x4mTYSBWj3Ck3QEV-0">
          Figma</a>
      </nav>
      <p>
        <span>저자: 김재채</span>
        <br>
        <span>이메일: ssafy13@ssafy.ac.kr</span>
        <br>
        <span>Copyright © 2025. JaeChaeKim. All Rights Reserved.</span>
      </p>
    </footer>
  </div>
</template>


<script setup>

</script>


<style scoped>
#wrap {
  min-height: 100vh;
  width: 100%;
  position: relative;
}

footer {
  height: 200px;
  width: 100%;
  bottom: 0px;
  position: absolute;
  background-color: transparent;
  color: #ccc;
  /* padding: 20px 40px; */
  padding: 10px 0;
}

footer img {
  height: 50px;
  padding-left: 190px;
}

footer nav {
  margin: 15px 0; /* 텍스트 위아래 여백 */
  padding-left: 200px;
}

footer p {
  margin: 15px 0; /* 텍스트 위아래 여백 */
  padding: 0 20px;
  padding-left: 200px;
}

</style>