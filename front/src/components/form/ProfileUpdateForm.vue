<template>
  <div class="modal fade" id="profileUpdateModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex flex-column">
          <div>
            <img src="@/assets/LOGO.png" alt="">
          </div>
          <h1 class="modal-title fs-5" id="exampleModalLabel">프로필 수정</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="">
            <div class="mb-3">
              <label for="update-username" class="col-form-label">닉네임</label>
              <input type="text" class="form-control" id="update-username" v-model="username">
            </div>
            <div class="mb-3">
              <label for="update-userintro" class="col-form-label">소개글</label>
              <input type="text" class="form-control" id="update-userintro" v-model="userIntroduction">
            </div>
            <div class="mb-3">
              <label for="update-userprofile" class="col-form-label">프로필 이미지</label>
              <input type="image" class="form-control" id="update-userprofile">
            </div>
            <div class="mb-3">
              <label for="update-userbanner" class="col-form-label">배너 이미지</label>
              <input type="image" class="form-control" id="update-userbanner">
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn w-100 update-button">업데이트</button>
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

let profileUpdateModal = null;

onMounted(() => {
  const bootstrap = window.bootstrap
  profileUpdateModal = new bootstrap.Modal(document.getElementById('profileUpdateModal'))
})

const username = ref('')
const userIntroduction = ref('')

const accountstore = useAccountStore()

</script>


<style scoped>
.update-button {
  background-color: #ff2c54;
  border: none;
  color: white;
}

.update-button:active {
  background-color: #df0c34;
  color: white;
}

.form-control:focus {
  border-color: #ff2c54;
  box-shadow: none;
}
</style>