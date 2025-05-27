<template>
  <section class="profile-card border rounded mx-auto">
    <header>
      <div class="banner-container flex-wrap position-relative">
        <img class="banner-img border rounded" :src="accountStore.API_URL + userInfo.user_banner_img" alt="이미지가 없습니다.">
        <div class="profile-container position-absolute">
          <img class="profile-img" :src="accountStore.API_URL + userInfo.user_profile_img" alt="프로필이 없습니다.">
        </div>
      </div>
    </header>
    <div class="container">
      <div class="name-update-container d-flex">
        <h2 class="name">{{ userInfo.username }}</h2>
        <button type="button" class="update-button ms-auto btn" data-bs-toggle="modal"
          data-bs-target="#profileUpdateModal" v-if="accountStore.auth.userPk == route.params.userId"
          data-bs-whatever="@mdo">프로필 수정</button>
      </div>
      <hr class="my-4">
      <div class="border rounded introduction-container">
        <p v-if="userInfo.user_introduction">{{ userInfo.user_introduction }}</p>
        <p v-else class="introduction-write">설명이 없습니다...</p>
      </div>
      <div class="follow-container d-flex justify-content-between mx-4 my-3 align-items-center">
        <p class="m-0">팔로워 {{ userInfo.num_followers }}</p>
        <p class="m-0">팔로잉 {{ userInfo.num_followings }}</p>
        <div v-if="Number(route.params.userId) !== accountStore.auth.userPk">
          <button class="btn btn-outline-primary" @click="onFollow" v-if="!userInfo.isFollowed">
            팔로우
          </button>
          <button class="btn btn-outline-primary" @click="onFollow" v-else>
            언팔로우
          </button>
        </div>
      </div>
      <hr class="my-4">
      <div class="d-flex justify-content-between mx-4 mb-3">
        <p>댓글 {{ userInfo.num_comments }}</p>
        <p>쓰레드 {{ userInfo.num_threads }}</p>
      </div>
    </div>
  </section>

  <!-- profile update form -->
  <div class="modal fade" id="profileUpdateModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5 mt-4 mb-3" id="exampleModalLabel">프로필 수정</h1>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onUpdate">
            <div class="mb-3">
              <label for="update-username" class="col-form-label">닉네임</label>
              <input type="text" class="form-control" id="update-username" v-model="username">
            </div>
            <div class="mb-3">
              <label for="update-userintro" class="col-form-label">소개글</label>
              <textarea type="text" class="form-control" id="update-userintro" v-model="user_introduction"></textarea>
            </div>
            <div class="mb-3">
              <label for="update-userprofile" class="col-form-label">프로필 이미지</label>
              <input type="file" class="form-control" id="update-userprofile" @change="profileUpdate">
            </div>
            <div class="mb-3">
              <label for="update-userbanner" class="col-form-label">배너 이미지</label>
              <input type="file" class="form-control" id="update-userbanner" @change="bannerUpdate">
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 update-finish-button">업데이트</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 0. import & route, store, props
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'

const route = useRoute()
const accountStore = useAccountStore()
const props = defineProps({
  userInfo: {
    type: Object,
  }
})

// 1. Follow
const emits = defineEmits(['follow', 'updateProfile'])

const onFollow = () => {
  axios({
    url: `http://127.0.0.1:8000/accounts/${route.params.userId}/follow/`,
    method: 'post',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`
    }
  }).then(res => {
    emits('follow', res.data)
  }).catch(err => {
    console.log(err)
  })
}

// 2. Update
const username = ref(props.userInfo.username)
const user_introduction = ref(props.userInfo.user_introduction)
const user_banner_img = ref('')
const user_profile_img = ref('')

let updateModal = null
onMounted(() => {
  const bootstrap = window.bootstrap
  updateModal = new bootstrap.Modal(document.querySelector('#profileUpdateModal'))
})

const profileUpdate = (event) => {
  user_profile_img.value = event.target.files[0]
}
const bannerUpdate = (event) => {
  user_banner_img.value = event.target.files[0]
}
const onUpdate = () => {
  const formData = new FormData();
  formData.append('username', username.value)
  formData.append('user_introduction', user_introduction.value)
  formData.append('user_banner_img', user_banner_img.value)
  formData.append('user_profile_img', user_profile_img.value)
  axios({
    url: accountStore.API_URL + `/accounts/${route.params.userId}/update/`,
    data: formData,
    method: 'put',
    headers: {
      Authorization: `Token ${accountStore.auth.token}`,
      "Content-Type": 'multipart/form-data'
    }
  }).then(res => {
    emits('updateProfile', res.data)
    updateModal.hide()
  }).catch(err => {
    console.log(err)
  })
}
</script>


<style scoped>
/* 프로필 화면의 프로필 카드 */
.profile-card {
  color: white;
  width: 1000px;
  min-width: 1000px;
  max-width: 1000px;
  margin: 40px auto 0 auto;  /* 가운데 정렬 및 상단 여백 */
  box-shadow: 0 4px 24px #666565;
  border-radius: 18px;
  padding: 0;
}


.banner-container {
  width: 100%;
  padding-bottom: 60px;
  overflow: hidden;
}

.banner-img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.profile-container {
  position: absolute;
  width: 100px;
  height: 100px;
  left: 5%;
  border-radius: 100%;
  overflow: hidden;
  bottom: 13px;
  box-shadow: 0 4px 10px #8a8a8a;
}

.profile-img {
  width: 100px;
  height: 100px;
}


.container {
  width: 1000px;
}


.name-update-container {
  display: flex;
  align-items: center;
  padding: 0px 20px 0px 35px;
}

.update-button {
  border-color: rgb(171, 173, 175);
  color: rgb(171, 173, 175);
}
.update-button:hover {
  box-shadow: 0 2px 12px 0 #ccc;
}


.introduction-container {
  height: 10rem;
  margin: 0px 20px;
}

.introduction-write {
  margin: 10px;
}


.follow-button {
  border-color: #FF2C54;
  color: #FF2C54;
}
.follow-button:hover {
  box-shadow: 0 2px 12px 0 #FF2C54;
}


/* 프로필 수정 modal */
h1 {
  font-size: 1.5em !important;
}

.update-finish-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.update-finish-button:active {
  background-color: #df0c34;
  color: white;
}

.form-control:focus {
  border-color: #ff2c54;
  box-shadow: none;
}
</style>