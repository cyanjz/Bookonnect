<template>
  <div class="modal fade" id="logInModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5" id="exampleModalLabel">로그인</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onLogIn">
            <div class="mb-3">
              <label for="email" class="col-form-label">이메일</label>
              <input type="text" class="form-control" id="email" v-model="email">
            </div>
            <div class="mb-3">
              <label for="message-text" class="col-form-label">비밀번호</label>
              <input type="password" class="form-control" id="message-text" v-model="password"></input>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 login-button">로그인</button>
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

let loginModal = null;

onMounted(() => {
  const bootstrap = window.bootstrap
  loginModal = new bootstrap.Modal(document.getElementById('logInModal'))
})

const email = ref('')
const password = ref('')

const accountstore = useAccountStore()

const onLogIn = () => {
  if (email.value === '') {
    alert('이메일을 입력해주세요.')
  }
  else if (password.value === '') {
    alert('비밀번호를 입력해주세요.')
  }
  else {
    const payload = {
      email: email.value,
      password: password.value,
      modal : loginModal,
    }
    accountstore.logIn(payload)
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