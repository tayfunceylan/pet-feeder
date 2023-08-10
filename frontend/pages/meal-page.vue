<script setup lang="ts">

import NavBar from "~/Components/tool-bar.vue";
import MealInfo from "~/Components/meal-card.vue";
import PageHeader from "~/Components/page-header.vue";
import ToolBar from "~/Components/tool-bar.vue";
</script>>

<template>

  <page-header></page-header>
  <div class="meal-list">
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
    <meal-info/>
  </div>
  <tool-bar/>

</template>

<style scoped lang="sass">
@import "assets/colors"

body
  background-color: $background-dark

.meal-list
  @include all-center
  background-color: $background-dark
  padding-top: 19px + $navbar-height
  width: 100vw
  padding-bottom: 50px + $navbar-height
  flex-direction: column
  gap: 15px




</style>