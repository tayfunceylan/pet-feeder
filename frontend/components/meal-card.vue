<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import {useAuthStore} from "~/stores/auth";
import MealInfo from "~/components/meal-info.vue"
import MealInput from "~/components/meal-input.vue";
import {deleteMealID, fetchFoodID, fetchMealID, postMeal, putMeal} from "~/helpers/api";

const props = defineProps(["mealID", "petsList"])
const emits = defineEmits(['refresh-list'])

let meal = ref(null);
let food = ref(null);
let isActive = ref(false);
const authStore = useAuthStore()

onMounted(async () => {
  // upon creation handle the mealCard differently if the meal came from the database or is newly created
  // if the id is undefined, it means that it was newly created else it came from the database
  if(props.mealID.id !== undefined) await fetchMeal()
  else{
    meal.value = props.mealID
    const foodResponse = await fetchFoodID(authStore, meal.value.food)
    food.value = foodResponse.data
    counter.value += 1
  }
});

const counter = ref(0)

// Fetch Meal with id and food name / units from meal
async function fetchMeal(id = null){
  const mealResponse = await fetchMealID(authStore, id ? id : props.mealID.id)
  meal.value = mealResponse.data

  // Use the food id from meal data to fetch the food data
  const foodId = meal.value?.food
  const foodResponse = await fetchFoodID(authStore, foodId)
  food.value = foodResponse.data
  counter.value += 1
}

function updateMeal(newMeal){
  // create meal Data
  let tempMeal = {
    quantity: newMeal.quantity,
    food: newMeal.food.id,
    pet: newMeal.fed,
    time: `${newMeal.date}T${newMeal.time}`
  }
  // Post if it doesn't exist put to update and refresh the meal data
  if(meal.value.id === undefined){
    const postResponse = postMeal(authStore, tempMeal)
    postResponse.then((response) => fetchMeal(response.data.id))
  }else{
    const putResponse = putMeal(authStore, meal.value.id, tempMeal)
    putResponse.then(() => fetchMeal(meal.value.id))
  }
}
function deleteMeal(){
  // only delete if the meal exists in the database (if id doesn't exist, then it means it is only local)
  if(meal.value.id !== undefined){
    const deleteResponse = deleteMealID(authStore, meal.value.id)
    deleteResponse.then(() => emits('refresh-list'))
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