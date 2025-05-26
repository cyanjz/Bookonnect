<template>
  <!-- footer가 항상 하단에 고정되도록 wrap 사용 -> 유일한 wrap이므로 id로 부여 -->
  <div id="wrap">
    <footer>
      <div class="footer-inner">
        <img src="@/assets/LOGO_white.png" alt="logo_img.png" class="logo">
        <nav>
          <a href="https://www.notion.so/isaacshin/1e4469106168806d96ccc85906cb9c1d">
            <img src="@/assets/notion_icon.png" alt="Notion" class="link-icon-notion">
          </a>
          <a href="https://www.figma.com/design/KOCRExKa4dtO6s1nEGjOuw/UI-UX-Design?node-id=0-1&t=x4mTYSBWj3Ck3QEV-0">
            <img src="@/assets/figma_icon.png" alt="Figma" class="link-icon-figma">
          </a>
        </nav>
        <p>
          <span>저자: 김재채</span>
          <br>
          <span>이메일: ssafy13@ssafy.ac.kr</span>
          <br>
          <span>Copyright © 2025. JaeChaeKim. All Rights Reserved.</span>
        </p>
      </div>
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
  color: #cccccce5;
  /* padding: 10px 0; */
  margin-bottom: 30px;

  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}

/* .footer-inner {
  display: flex;
  flex-direction: column;
  /* 묶음 안에서는 왼쪽 정렬 */
  /* align-items: flex-start;
} */

.logo {
  height: 50px;
  margin-bottom: 10px;
}

footer nav {
  margin: 15px 0;
  justify-content: center;
}

.link-icon-notion {
  height: 30px;
  width: auto;
}

.link-icon-figma {
  height: 30px;
  width: auto;
  padding-left: 30px;
}

footer p {
  margin: 20px 0;
}

</style>