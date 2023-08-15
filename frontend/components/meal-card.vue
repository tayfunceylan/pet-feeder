<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import MealInfo from "~/components/meal-info.vue"
import MealInput from "~/components/meal-input.vue";
import {integer} from "vscode-languageserver-types";
import axios from "axios";
import {useAuthStore} from "~/stores/auth";
const props = defineProps(["mealID", "petsList"])


let meal = ref(null);
let food = ref(null);
let isActive = ref(false);
const authStore = useAuthStore()

onMounted(async () => {
  await fetchMeal();
});

const counter = ref(0)

async function fetchMeal(){
  const mealResponse = await axios.get(`http://127.0.0.1:8000/Meal/${props.mealID.id}/`,{
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`
    },
  }).catch((error) => {
    console.log(`Meal error: ${error.status}`)
    if(error.status) navigateTo('/login')
  })
  meal.value = mealResponse.data

  // Use the food id from meal data to fetch the food data
  const foodId = meal.value.food
  const foodResponse = await axios.get(`http://127.0.0.1:8000/Food/${foodId}/`, {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`
    },
  }).catch((error) => {
    console.log(`Food error: ${error.status}`)
    if(error.status) navigateTo('/login')
  })
  food.value = foodResponse.data
  counter.value += 1
  console.log(counter)
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