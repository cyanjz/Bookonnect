<template>
  <div class="modal fade" id="signUpModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5" id="exampleModalLabel">회원가입</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onSignUp">
            <div class="mb-3">
              <label for="signup-username" class="col-form-label">닉네임</label>
              <input type="text" class="form-control" id="signup-username" v-model="username">
            </div>
            <div class="mb-3">
              <label for="signup-email" class="col-form-label">이메일</label>
              <input type="text" class="form-control" id="signup-email" v-model="email">
            </div>
            <div class="mb-3">
              <label for="password1" class="col-form-label">비밀번호</label>
              <input type="password" class="form-control" id="password1" v-model="password1"></input>
            </div>
            <div class="mb-3">
              <label for="password2" class="col-form-label">비밀번호 확인</label>
              <input type="password" class="form-control" id="password2" v-model="password2"></input>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 login-button">회원가입</button>
            </div>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts';

let signUpModal = null;

onMounted(() => {
  const bootstrap = window.bootstrap
  signUpModal = new bootstrap.Modal(document.getElementById('signUpModal'))
})

const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

const accountstore = useAccountStore()
const onSignUp = () => {
  if (email.value === '') {
    alert('이메일을 입력해주세요.')
  }
  else if (username.value === '') {
    alert('닉네임을 입력해주세요.')
  }
  else if (password1.value === '') {
    alert('비밀번호를 입력해주세요.')
  }
  else if (password1.value !== password2.value) {
    alert('비밀번호가 다릅니다.')
  }
  else {
    const payload = {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
      modal: signUpModal,
    }
    accountstore.signUp(payload)
  }
}
</script>


<style scoped>
.login-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.login-button:active {
  background-color: #df0c34;
  color: white;
}

.form-control:focus {
  border-color: #ff2c54;
  box-shadow: none;
}
</style>