<script setup lang="js">

import {useAuthStore} from "~/stores/auth";
import {url} from "~/helpers/api";
import axios from "axios";

// const formatted = useDateFormat(useNow(), 'YYYY-MM-DD')
const date = ref(new Date().toISOString().substring(0, 10))
const counter = ref(0)
const authStore = useAuthStore()
const mealcounter = ref(0)
const dateMeals = ref(null)

async function fetchMealList(){
  const listResponse = await axios.get(`${url}/Meal/get_day/?date=${date.value}`, {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`
    },
  }).catch((error) => {
    console.log(`mealsList error: ${error.response.status}`)
    if(error.response.status === 401) navigateTo('/login')
  })
  dateMeals.value = listResponse.data
  mealcounter.value++
}

onMounted(async () => {
   await  fetchMealList()
  console.log("meal_list: ", meal_list.value)
})
/*
const {pending: pendingMeals, data: dateMeals, refresh: refreshMeals} = await useAsyncData(
    "mealsList",
    () => $fetch(`${url}/Meal/get_day/?date=${date.value}`, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
      lazy: true,
      server: false,
    }).catch((error) => {
      console.log(`mealsList error: ${error.status}`)
      if(error.status === 401) navigateTo('/login')
    }),
    {
      watch: [date]
    }
)
*/
const {pending: pendingPets, data: pets} = await useAsyncData(
    "pets",
    () => $fetch(`${url}/Pet/`,{
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
      lazy: true,
      server: false,
    }).catch((error) => {
      console.log(`Pets error: ${error.status}`)
      if(error.status === 401) navigateTo('/login')
    })
)
const changeDate = (day) => {
  let temp = date.value
  const currentDate = new Date(temp)
  const nextDate = new Date(currentDate)
  nextDate.setDate(currentDate.getDate() + day)
  date.value = nextDate.toISOString().substring(0, 10)
  fetchMealList()
}

const addMeal = () => {
  let meal = {
    quantity: 0,
    food: 1,
    pet: [],
    time: Date.now()
  }
  dateMeals.value.meals.push(meal)
  console.log(dateMeals.value.meals)

}
</script>>

<template>
    <div class="date-picker" :key="counter">
      <button @click="changeDate(-1)">&lt</button>
      <input type="date" v-model="date">
      <button @click="changeDate(1)">></button>
    </div>
    <p v-if="!dateMeals !== null && pendingPets">Loading ...</p>
    <div class="meal-list" v-else-if="dateMeals != null" :key="mealcounter">
      <button class="add" @click="addMeal">+</button>
      <meal-card v-for="meal in dateMeals.meals" :petsList="pets" :mealID="meal" @refresh-list="fetchMealList"/>
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
  @include text-style-normal
  background-color: $background-bright
  border-radius: 50px
  width: 30px
  height: 30px

.add
  width: 200px
  transition: 0.7s ease-in-out
  &:active
    width: 220px
  &:active
    opacity: 0.8
    background-color: white

</style>