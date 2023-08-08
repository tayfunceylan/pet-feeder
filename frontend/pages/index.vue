<template>
  <div>
    <NuxtPage/>
  </div>
  <tool-bar/>
</template>

<style lang="sass">
@import '/assets/_colors'
body
  background-color: $background-dark

.bold
  font-weight: bold
  font-size: $bold-size
  color: $default-text-color
p
  font-size: $default-size
  color: $default-text-color
</style>

<script setup lang="ts">


import NavBar from "~/Components/tool-bar.vue";
import ToolBar from "~/Components/tool-bar.vue";
</script>