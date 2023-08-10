<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import MealInfo from "~/Components/meal-info.vue"
import MealInput from "~/Components/meal-input.vue";
import axios from "axios";
import async from "async";
const props = defineProps(["meal_data", "petsList"])
const isActive = ref(false)
console.log("Pets: ", props.petsList)

console.log(props.meal_data)
const food = ref({
  brand: null,
  category: null,
  id: null,
  name: null,
  price: null,
  unit: null,
})
const meal = ref({
  food: null,
  id: null,
  pet: null,
  quantity: null,
  time: null,
})
/*
async function getMeal(){
  const res = await fetch('http://127.0.0.1:8000/Meal/'+props.meal_data.id)
  const finalRes = await res.json()
  meal.value = finalRes
}
getMeal()
async function getFood(){
  const res = await fetch('http://127.0.0.1:8000/Food/'+props.meal_data.food)
  const finalRes = await res.json()
  food.value = finalRes
}
getFood()
*/
axios.get('http://127.0.0.1:8000/Food/'+props.meal_data.food)
    .then(response => {
      food.value = response.data
    })
    .catch(error => {
      console.log(error);
    })

axios.get('http://127.0.0.1:8000/Meal/'+props.meal_data.id)
    .then(response => {
      meal.value = response.data
    })
    .catch(error => {
      console.log(error);
    })



const data = ref({
  pets: [1, 2],
  fed: [1],
  num_pets: 2,
  food: food.value.name,
  date: useDateFormat(meal.value.time, 'YYYY-MM-DD'),
  time: useDateFormat(meal.value.time, 'HH:mm'),
  quantity: 100,
  unit: 'g',
})

function change_fed(id){
  if(data.value.fed.includes(id)) data.value.fed.splice(data.value.fed.indexOf(id), 1)
  else data.value.fed.push(id)
}

// TODO: on update make put request
function update(new_data){
  data.value.food = new_data.food
  data.value.date = new_data.date
  data.value.time = new_data.time
  data.value.quantity = new_data.quantity
  data.value.unit = new_data.unit
}
</script>

<template>
  <OnClickOutside @trigger="isActive=false">
    <div class="meal-card" :class="isActive ? 'open' : ''">
      <Transition>
        <meal-info
            :active="isActive"
            :fed="meal.pet"
            :pets="props.pets"
            :food="food.name"
            :time="useDateFormat(meal.time, 'HH:mm')"
            :quantity="meal.quantity"
            :unit="food.unit"
            @open-meal="isActive=true"
        />
      </Transition>
      <Transition name="inputs">
        <meal-input
            v-if="isActive"
            :input="data"
            :active="isActive"
            :pets="data.pets"
            :fed="data.fed"
            :num_pets="data.num_pets"
            @update="(new_data) => update(new_data)"
            @close-meal="isActive=false"
            @update-pets="(id) => change_fed(id)"
        />
      </Transition>
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

.inputs-enter-active,
.inputs-leave-active
  transition: all 0.5s ease


.inputs-enter-from,
.inputs-leave-to
  opacity: 0


</style>