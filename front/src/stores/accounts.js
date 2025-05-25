import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('', () => {
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000/'

  // 0. states
  const auth = ref({
    token: '',
    isAuthenticated: false,
    userPk: null,
  })

  // 1. SignUp
  const signUp = ({ username, email, password1, password2, modal }) => {
    axios({
      url: API_URL + 'accounts/signup/',
      method: 'post',
      data: {
        username, email, password1, password2
      }
    }).then((res) => {
      auth.value.token = res.data.key
      getMyInfo(modal)
    }).catch((err) => {
      console.log(err)
      alert(err.response.data.email)
    })
  }

  // 2. logIn
  const logIn = ({ email, password, modal }) => {
    axios({
      url: API_URL + 'accounts/login/',
      method: 'post',
      data: {
        email, password
      }
    }).then((res) => {
      auth.value.token = res.data.key
      getMyInfo(modal)
    }).catch((err) => {
      alert('이메일 또는 비밀번호를 확인해 주세요.')
      console.log(err)
    })
  }

  // 3. get my info
  const getMyInfo = (modal) => {
    axios({
      url: API_URL + 'accounts/myinfo/',
      method: 'get',
      headers: {
        Authorization: `Token ${auth.value.token}`
      }
    }).then((res) => {
      auth.value.userPk = res.data.pk
      auth.value.isAuthenticated = true
      console.log('로그인 성공!')
      modal.hide()
      router.push({ name: 'main-page' })
    }).catch(err => {
      console.log(err)
    })
  }

  // 4. logout
  const logOut = () => {
    axios({
      url: API_URL + 'accounts/logout/',
      method: 'post',
      headers: {
        Authorization: `Token ${auth.value.token}`
      }
    }).then((res) => {
      auth.value.userPk = null
      auth.value.isAuthenticated = false
      auth.value.token = ''
    }).catch(err => {
      console.log(err)
    })
  }


  return {
    auth, API_URL,
    signUp, logIn, getMyInfo, logOut
  }
}, { persist: true })
