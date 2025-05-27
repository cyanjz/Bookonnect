<template>
  <div>
    <h1>ThreadList 내 하위 컴포넌트들</h1>
    <p>{{ thread }}</p>
  </div>
</template>


<script setup>
const props = defineProps({
  thread: {
    type: Object,
    required: true,
  }
})
</script>


<style scoped>

</style>