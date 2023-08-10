<script setup lang="ts">
defineProps(['active', 'fed', 'pets', 'num_pets', 'food', 'time', 'quantity', 'unit'])
defineEmits(['open-meal', "update-pets"])
const food_types = ["food 1", "steak"]
const feeding = ref([])
</script>

<template>
  <Transition>
    <div class="meal-input-wrap">
      <div  class="pet-selector">
        <div v-for="pet in pets" id="{{pet}}"
             class="pets"
             :class="[fed.includes(pet) ? 'isFed' : 'starving']"
             :style="{backgroundColor: pet == 1 ? '#9ac1ed' : '#efab92'}"
             @click="$emit('update-pets', pet)"
        />
      </div>
      <div class="row-wrapper">
        <div >
          <label>Food:</label>
          <select class="food">
            <option v-for="food in food_types" value="{{food}}">{{food}}</option>
          </select>
        </div>
        <div class="quantity">
          <input class="quantity-input" type="number" value="{{quantity}}">
          <label>{{unit}}</label>
        </div>
      </div>
      <div class="row-wrapper">
        <div class="date">
          <label>Date</label>
          <input class="date-picker" type="date" value="{{quantity}}">
        </div>
        <div class="time">
          <label>Time</label>
          <input class="time-picker" type="time" value="{{quantity}}">
          <label>Uhr</label>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped lang="sass">
@import "assets/colors"
@include text-standard


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
    height: 30px
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
    gap: 10px
    width: 80px
    input
      @include text-style-normal
      text-align: center
      height: 30px
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
  .date-picker
    width: 120px

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


.v-enter-active,
.v-leave-active
  transition: all 0.5s ease


.v-enter-from,
.v-leave-to
  opacity: 0

</style>