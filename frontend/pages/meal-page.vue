<script setup lang="js">
import MealInfo from "~/Components/meal-card.vue";
import PageHeader from "~/Components/page-header.vue";
import ToolBar from "~/Components/tool-bar.vue";
import axios from "axios";
import { useNow, useDateFormat } from '@vueuse/core'

const formatted = useDateFormat(useNow(), 'YYYY-MM-DD')
const meal_list = ref(null)
const pets = reactive(null)

axios.get('http://127.0.0.1:8000/Meal/?date='+formatted)
    .then(response => {
      meal_list.value = response.data
    })
    .catch(error => {
      console.log(error);
    })
axios.get('http://127.0.0.1:8000/Pet/')
    .then(response => {
      pets.value = response.data
      console.log("pets ", pets.value)
    })
    .catch(error => {
      console.log(error);
    })
/*
async function getMealList(){
  const res = await fetch('http://127.0.0.1:8000/Meal/?date='+formatted)
  const finalRes = await  res.json()
  meal_list.value = finalRes
}
getMealList()
async function getPets(){
  const res = await fetch('http://127.0.0.1:8000/Pet/')
  const finalRes = await res.json()
  pets.value = finalRes
}
getPets()

 */
</script>>

<template>
  <div class="page">
    <page-header></page-header>
    <div class="meal-list">
      <meal-info v-for="meal in meal_list" :petsList="pets" :meal_data="meal" />

    </div>
    <tool-bar/>

  </div>

</template>

<style scoped lang="sass">
@import "assets/colors"

.page
  height: 100vh
  width: 100vw
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