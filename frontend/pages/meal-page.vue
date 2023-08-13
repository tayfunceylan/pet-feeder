<script setup lang="js">
import MealInfo from "~/Components/meal-card.vue";
import PageHeader from "~/Components/page-header.vue";
import ToolBar from "~/Components/tool-bar.vue";
import axios from "axios";
import { useNow, useDateFormat } from '@vueuse/core'

// const formatted = useDateFormat(useNow(), 'YYYY-MM-DD')
const date = ref(new Date().toISOString().substring(0, 10))

const {pending: pendingMeals, data: dateMeals, refresh: refreshMeals} = await useAsyncData(
    "mealsList",
    () => $fetch(`http://127.0.0.1:8000/Meal/get_day/?date=${date.value}`, {
      lazy: true,
      server: false,
    }).catch((error) => {console.log(`mealsList error: ${error}`)}),
    {
      watch: [date]
    }
)

const {pending: pendingPets, data: pets} = await useAsyncData(
    "pets",
    () => $fetch('http://127.0.0.1:8000/Pet/',{
      lazy: true,
      server: false,
    }).catch((error) => {console.log(`pets error: ${error}`)}),
)
</script>>

<template>
  <div class="page">
    <page-header></page-header>
    <div class="date-picker">
      <button>&lt</button>
      <input type="date" v-model="date" @change="() => console.log('data: ', date)">
      <button>></button>
    </div>
    <p v-if="pendingMeals && pendingPets">Loading ...</p>
    <div class="meal-list" v-else-if="dateMeals != null">
      <meal-info v-for="meal in dateMeals.meals" :petsList="pets" :mealID="meal" />
    </div>
    <tool-bar/>
  </div>

</template>

<style scoped lang="sass">
@import "assets/colors"
p
  @include text-standard
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


.date-picker
  margin-top: 60px
  border: 1px solid wheat
  display: flex
  height: 70px
  flex-direction: row
  justify-content: space-evenly
  align-items: center

  *
    @include text-style-normal

</style>