<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import MealInfo from "~/Components/meal-info.vue"
import MealInput from "~/Components/meal-input.vue";
import {integer} from "vscode-languageserver-types";
import axios from "axios";
const props = defineProps(["mealID", "petsList"])


let meal = ref(null);
let food = ref(null);
let isActive = ref(false);

onMounted(async () => {
  await fetchMeal();
});


async function fetchMeal(){
  const mealResponse = await axios.get(`http://127.0.0.1:8000/Meal/${props.mealID.id}/`)
  meal.value = mealResponse.data

  // Use the food id from meal data to fetch the food data
  const foodId = meal.value.food
  const foodResponse = await axios.get(`http://127.0.0.1:8000/Food/${foodId}/`)
  food.value = foodResponse.data
}


</script>

<template>
  <OnClickOutside @trigger="isActive=false">
    <div class="meal-card" :class="isActive ? 'open' : ''" v-if="meal" :key="meal">
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
    <div v-else>Loading Card...</div>

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

.inputs-enter-active,
.inputs-leave-active
  transition: all 0.5s ease


.inputs-enter-from,
.inputs-leave-to
  opacity: 0


</style>