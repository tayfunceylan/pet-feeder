<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import MealInfo from "~/components/meal-info.vue"
import MealInput from "~/components/meal-input.vue";
import axios from "axios";
import {useAuthStore} from "~/stores/auth";
import {url} from "~/helpers/api";

const props = defineProps(["mealID", "petsList"])
const emits = defineEmits(['refresh-list'])

let meal = ref(null);
let food = ref(null);
let isActive = ref(false);
const authStore = useAuthStore()

onMounted(async () => {
  if(props.mealID.id !== undefined) await fetchMeal()
  else{
    meal.value = props.mealID
    console.log("Meal: ", meal.value)
    const foodResponse = await axios.get(`${url}/Food/${meal.value.food}/`, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
    }).catch((error) => {
      console.log(`Food error: ${error.status}`)
      if(error.status === 401) navigateTo('/login')
    })
    food.value = foodResponse.data
    counter.value += 1
  }
});

const counter = ref(0)

// Fetch Meal with id and food name / units from meal
async function fetchMeal(id = null){
  const mealResponse = await axios.get(`${url}/Meal/${id ? id : props.mealID.id}/`,{
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`
    },
  }).catch((error) => {
    console.log(`Meal error: ${error.status}`)
    if(error.status === 401) navigateTo('/login')
  })
  meal.value = mealResponse.data

  // Use the food id from meal data to fetch the food data
  const foodId = meal.value.food
  const foodResponse = await axios.get(`${url}/Food/${foodId}/`, {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`
    },
  }).catch((error) => {
    console.log(`Food error: ${error.status}`)
    if(error.status === 401) navigateTo('/login')
  })
  food.value = foodResponse.data
  counter.value += 1
  console.log(counter)
}

function updateMeal(newMeal){
  meal.value.fed = newMeal.fed
  meal.value.food = newMeal.food.id
  meal.value.quantity = newMeal.quantity

  if(meal.value.id === undefined){
    axios.post(`${url}/Meal/`, {
      quantity: newMeal.quantity,
      food: newMeal.food.id,
      pet: newMeal.fed,
      time: `${newMeal.date}T${newMeal.time}`
    }, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
    }).then((response) => fetchMeal(response.data.id)).catch((error) => {
      console.log(`Meal error: ${error}`)
      if(error.status === 401) navigateTo('/login')
    })
  }else{
    axios.put(`${url}/Meal/${meal.value.id}/`, {
      quantity: newMeal.quantity,
      food: newMeal.food.id,
      pet: newMeal.fed,
      time: `${newMeal.date}T${newMeal.time}`
    }, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
    }).then(() => fetchMeal(meal.value.id)).catch((error) => {
      console.log(`Meal error: ${error}`)
      if(error.status === 401) navigateTo('/login')
    })
  }
}
function deleteMeal(){
  if(meal.value.id !== undefined){
    axios.delete(`${url}/Meal/${meal.value.id}`, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
    }).then((response) => {console.log("meal: ", meal.value.id); emits('refresh-list')}).catch((error) => {
      console.log(`Meal delete error: ${error}`)
      if(error.status === 401) navigateTo('/login')
    })
  }
}
</script>

<template>
  <OnClickOutside @trigger="isActive=false">
    <div class="wrapper">
      <Transition v-if="meal" name="card">
        <div class="meal-card" :class="isActive ? 'open' : ''" :key="counter">
          <Transition>
            <meal-info
                :active="isActive"
                :foodDetail="food"
                :mealDetail="meal"
                :pets="petsList"
                @open-meal="isActive=true"
                @delete-meal="deleteMeal"
            />
          </Transition>
          <Transition>
            <meal-input
                v-if="isActive"
                :active="!isActive"
                :foodDetail="food"
                :mealDetail="meal"
                :pets="petsList"
                @open-meal="isActive=true"
                @close-meal="isActive=false"
                @refresh-meal="fetchMeal"
                @update-meal="updateMeal"
            />
          </Transition>
        </div>
      </Transition>
      <div v-else>Loading Card...</div>
    </div>

  </OnClickOutside>

</template>

<style scoped lang="sass">
@import "assets/colors"
@include text-standard
/* we will explain what these classes do next! */
.v-enter-active,
.v-leave-active
  transition: all 0.5s ease


.v-enter-from
  height: 0

.v-leave-to
  opacity: 0

.meal-card
  width: 320px
  height: $meal-height
  box-shadow: $default-shadow
  transition: all 0.5s ease-in-out
  border-radius: $radius

  &.open
    height: $meal-height + 180px



.card-enter-active
  transition: all 0.6s ease-in-out
.card-leave-active
  position: fixed
  transition: all 0.6s ease-in-out


.card-enter-from
  opacity: 0
  transform: translateX(-400px)
.card-leave-to
  opacity: 0
  transform: translateX(400px)


</style>