<script setup lang="js">
import {OnClickOutside} from "@vueuse/components/index"
import MealInfo from "~/Components/meal-info.vue"
import MealInput from "~/Components/meal-input.vue";

const isActive = ref(false)

const data = ref({
  pets: [1, 2],
  fed: [1],
  num_pets: 2,
  food: 'steak',
  date: '2023-10-05',
  time: '12:30',
  quantity: 100,
  unit: 'g',
})

function change_fed(id){
  if(data.value.fed.includes(id)) data.value.fed.splice(data.value.fed.indexOf(id), 1)
  else data.value.fed.push(id)
}

function update_everything(data){
  data.value.food = data.food
  data.value.date = data.date
  data.value.time = data.time
  data.value.quantity = data.quantity
  data.value.unit = data.unit
}
</script>

<template>
  <OnClickOutside @trigger="isActive=false">
    <div class="meal-card" :class="isActive ? 'open' : ''">
      <Transition>
        <meal-info
            :active="isActive"
            :fed="data.fed"
            :pets="data.pets"
            :num_pets="data.num_pets"
            :food="data.food"
            :time="data.time"
            :quantity="data.quantity"
            :unit="data.unit"
            @open-meal="isActive=true"
        />
      </Transition>
      <Transition name="inputs">
        <meal-input
            v-if="isActive"
            :active="isActive"
            :pets="data.pets"
            :fed="data.fed"
            :num_pets="data.num_pets"
            :food="data.food"
            :time="data.time"
            :date="data.date"
            :quantity="data.quantity"
            :unit="data.unit"
            @open-meal="isActive=true"
            @update-pets="(id) => change_fed(id)"
            @update-everything="(new_data) => update_everything(new_data)"
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