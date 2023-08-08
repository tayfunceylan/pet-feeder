<script setup lang="ts">

import NavBar from "~/Components/nav-bar.vue";
import MealInfo from "~/Components/meal-info.vue";
</script>>

<template>
  <h1>MealPage</h1>
  <div class="meal-list">
    <meal-info/>
  </div>
  <nav-bar/>

</template>

<style scoped lang="sass">
.meal-list
  display: flex
  width: 100vw
  height: 100vh
  justify-content: center
</style>