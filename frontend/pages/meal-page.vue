<script setup lang="ts">

import NavBar from "~/Components/tool-bar.vue";
import MealInfo from "~/Components/meal-info.vue";
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

.meal-list
  margin-top: $navbar-height
  padding-top: 15px
  display: flex
  width: 100vw
  padding-bottom: 20px
  flex-direction: column
  align-items: center
  justify-content: center
  gap: 15px




</style>