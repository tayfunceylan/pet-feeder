<script setup lang="ts">
const props = defineProps(['input', 'active', 'fed', 'pets', 'num_pets',])
defineEmits(['close-meal', "update-pets", 'update'])

// TODO: Request available food
const food_types = ["food 1", "steak"]

const input_data = ref({
  fed: [1],
  food: props.input.food,
  date: props.input.date,
  time: props.input.time,
  quantity: props.input.quantity,
  unit: props.input.unit,
})

</script>

<template>
  <Transition>
    <div class="meal-input-wrap">
      <div  class="pet-selector">
        <div v-for="pet in input.pets" id="{{pet}}"
             class="pets"
             :class="[fed.includes(pet) ? 'isFed' : 'starving']"
             :style="{backgroundColor: pet == 1 ? '#9ac1ed' : '#efab92'}"
             @click="$emit('update-pets', pet)"
        />
      </div>
      <div class="row-wrapper">
        <div >
          <label>Food:</label>
          <select class="food" v-model="input_data.food">
            <option v-for="food in food_types">{{food}}</option>
          </select>
        </div>
        <div class="quantity">
          <input class="quantity-input" type="number" v-model="input_data.quantity">
          <label>{{input_data.unit}}</label>
        </div>
      </div>
      <div class="row-wrapper">
        <div class="date">
          <label>Date</label>
          <input class="date-picker" type="date" v-model="input_data.date">
        </div>
        <div class="time">
          <label>Time</label>
          <input class="time-picker" type="time" v-model="input_data.time">
        </div>
      </div>
      <div class="row-wrapper button-wrap">
        <button class="cancel" @click="$emit('close-meal')"><span>cancel</span></button>
        <button class="save" @click="$emit('update', input_data)">
          <span>save</span>
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped lang="sass">
@import "assets/colors"
@include text-standard

$row-height: 40px

label
  width: 50px


.row-wrapper
  width: 300px
  display: flex
  justify-content: space-between
  align-items: center
  flex-direction: row
  gap: 20px
  .food
    height: $row-height
    width: 130px
    font-weight: bold
    margin-left: 10px
    font-size: $default-size
    color: $default-text-color
    border: 2px solid $background-bright
    border-radius: 10px
    text-align: center
    transition: background-color 0.5s ease-in-out

    &:focus
      outline: none
      background-color: $background-bright

    option
      background-color: $background-dark
      border-radius: 10px
      transition: 0.2s ease-in-out

    option:hover
      background-color: $background-bright
      border-radius: 10px

  .quantity
    display: flex
    flex-direction: row
    justify-content: space-between
    align-items: center
    width: 80px
    gap: 10px
    input
      @include text-style-normal
      text-align: center
      height: $row-height
      width: 50px
      border: 2px solid $background-bright
      border-radius: 10px
      transition: 0.3s ease-in-out

    input:focus
      outline: none
      border: 2px solid $background-bright
      border-radius: 10px
      background-color: $background-bright

  .date
    display: flex
    flex-direction: row
    align-items: center
    .date-picker
      @include text-style-normal
      height: $row-height
      width: 100px
      transition: 0.3s ease-in-out
      &:focus
        outline: none
        border: 2px solid $background-bright
        background-color: $background-bright
        border-radius: 10px

  .time
    display: flex
    flex-direction: row
    justify-content: space-between
    align-items: center
    .time-picker
      height: $row-height
      @include text-style-normal
      transition: 0.3s ease-in-out

      &:focus
        outline: none
        border: 2px solid $background-bright
        background-color: $background-bright
        border-radius: 10px

.meal-input-wrap
  padding: 10px
  display: flex
  flex-direction: column
  gap: 10px
.pet-selector
  display: flex
  flex-direction: row
  align-content: space-between
  justify-content: space-evenly
  width: 100%

.pets
  width: 45px
  height: 45px
  border-radius: 50%
  border: 1px solid $background-bright
  &.isFed
    background-color: $primary-red
    stroke: 2px $primary-red

.button-wrap
  justify-content: space-evenly

button
  width: 80px
  height: 30px
  border-radius: 10px
  @include text-style-normal
  font-weight: bold
  transition: all 0.4s ease-in-out

.cancel
  background-color: transparent
  span
    text-decoration: underline $default-text-color
    transition: 0.3s ease-in-out

  &:active
    transform: scale(0.9)
    span
      letter-spacing: 1px


.save
  background-color: $primary-blue
  &:active
    transform: scale(1.1)
    background-color: $secondary-blue

.v-enter-active,
.v-leave-active
  transition: all 0.5s ease


.v-enter-from,
.v-leave-to
  opacity: 0

</style>