<script setup lang="ts">

</script>

<template>
  <div class="working">
    <img src="@/assets/lazy_cat.png" alt="sleeping cat">
    <p>We are working on it...</p>
  </div>
</template>

<style scoped lang="sass">
@import "assets/colors"

p
  @include text-style-normal
  width: 100%
  text-align: center

.working
  height: 100vh
  width: 100vw
  display: flex
  flex-direction: column
  justify-content: center
  align-content: center

</style>