<script setup lang="ts">

</script>

<template>
  <div class="header">
    <div class="profile"></div>
  </div>
</template>

<style scoped lang="sass">
@import "assets/colors"

.header
  top: 0
  position: fixed
  width: 100vw
  height: $navbar-height
  background-color: $background-dark
  display: flex
  justify-content: flex-end
  align-items: center
  padding-left: 20px
  padding-right: 30px
  box-shadow: $default-shadow

  .profile
    width: 40px
    height: 40px
    border-radius: 50%
    background-color: $primary-red
</style>