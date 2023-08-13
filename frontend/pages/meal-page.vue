<script setup lang="js">
import MealInfo from "~/components/meal-card.vue";
import PageHeader from "~/components/page-header.vue";
import ToolBar from "~/components/tool-bar.vue";
import axios from "axios";
import { useNow, useDateFormat } from '@vueuse/core'

// const formatted = useDateFormat(useNow(), 'YYYY-MM-DD')
const date = ref(new Date().toISOString().substring(0, 10))
const counter = ref(0)

const {pending: pendingMeals, data: dateMeals, execute: refreshMeals} = await useAsyncData(
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
const changeDate = (day) => {
  let temp = date.value
  const currentDate = new Date(temp)
  const nextDate = new Date(currentDate)
  nextDate.setDate(currentDate.getDate() + day)
  date.value = nextDate.toISOString().substring(0, 10)
  console.log("Next date is", nextDate.toISOString().substring(0, 10))
}
</script>>

<template>
    <div class="date-picker" :key="counter">
      <button @click="changeDate(-1)">&lt</button>
      <input type="date" v-model="date">
      <button @click="changeDate(1)">></button>
    </div>
    <p v-if="pendingMeals && pendingPets">Loading ...</p>
    <div class="meal-list" v-else-if="dateMeals != null" >
      <meal-info v-for="meal in dateMeals.meals" :petsList="pets" :mealID="meal" :key="meal.id"/>
    </div>
</template>

<style scoped lang="sass">
@import "assets/colors"
p
  @include text-standard

.meal-list
  @include all-center
  background-color: $background-dark
  width: 100vw
  padding-bottom: 50px + $navbar-height
  flex-direction: column
  gap: 15px


.date-picker
  margin-top: $navbar-height
  display: flex
  height: 80px
  flex-direction: row
  justify-content: space-evenly
  align-items: center

  *
    @include text-style-normal

input
  background-color: $background-bright
  padding: 5px 15px 5px 15px
  border-radius: 8px
button
  background-color: $background-bright
  border-radius: 50px
  width: 30px
  height: 30px


</style>