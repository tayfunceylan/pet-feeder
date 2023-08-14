<script setup lang="ts">

</script>

<template>
  <div class="wrapper">
    <slot/>
  </div>
</template>

<style scoped lang="sass">
@import "assets/colors"

.wrapper
  background-color: $background-dark
  width: 100vw
  height: 100vh
  display: flex
  justify-content: center
  align-items: center
  align-content: center
</style>