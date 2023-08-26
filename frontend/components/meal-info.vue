<script setup lang="js">
const props = defineProps(['active', 'foodDetail', 'mealDetail', 'pets'])
defineEmits(['open-meal', 'delete-meal'])
const formatted = (date) => new Date(date).toISOString().substring(11, 16)

</script>

<template>
  <div v-if="mealDetail === null || foodDetail === null || pets === null ">Loading Info...</div>
  <div v-else class="meal-holder" :class="[!active? 'open': 'closed']" @click="$emit('open-meal')">

    <div class="meal-info">
      <div class="pet-info" :class="[!active? 'open': 'closed']" :key="props.pets">
        <div class="pet" v-for="pet in props.pets"
             :class="[props.mealDetail.pet.includes(pet.id) ? 'fed' : 'starving']"
             :style="{'background-color': props.mealDetail.pet.includes(pet.id) ? pet.color : 'none'}">
        </div>
      </div>

      <div class="meal-details">
        <Transition>
          <b class="bold" v-if="!active" id="food-type">{{ foodDetail.name }}</b>
        </Transition>
        <p id="time">{{ formatted(mealDetail.time) }} Uhr</p>
      </div>
    </div>

    <div v-if=!active class="meal-quantity">
      <b class="bold" id="quantity">{{ props.mealDetail.quantity }}{{ props.foodDetail.unit }}</b>
    </div>
    <div v-else class="meal-quantity delete" @click="$emit('delete-meal')">
      <b class="bold" id="quantity">X</b>
    </div>

  </div>
</template>

<style scoped lang="sass">
@import "assets/_colors"
@include  text-standard
.meal-holder
  display: flex
  width: 320px
  flex-direction: row
  gap: 0
  transition: all 0.5s ease-in-out

  &.open
    height: $meal-height

  &.closed
    height: 40px

  &.closed .meal-info
    border-radius: $radius 0 0 0
    transition: border-radius 0.5s ease-in-out

  .meal-info
    @include all-center
    border-radius: $radius 0 0 $radius
    flex: 1
    width: 270px

    background-color: $background-bright
    justify-content: space-evenly
    flex-direction: row
    padding-left: 15px

    .pet-info
      height: 50px
      width:  50px
      display: flex
      align-items: center
      flex-wrap: wrap
      gap: 2px
      transition: 0.3s ease-in-out

      &.closed
        width:  70px

      .pet
        width: 20px
        height: 20px
        border-radius: 50%
        background-color: $background-dark

      .fed
        transition: all 0.3s ease-in-out
        background-color: $primary-red

      .starving
        transition: all 0.3s ease-in-out
        background-color: $background-dark

    .meal-details
      @include all-center
      flex: 2
      width: 120px
      height: 30px
      flex-direction: column
      flex-shrink: 0

    &.open .meal-details
      @include all-center


  .meal-quantity
    @include all-center
    background-color: $primary-blue
    width: 60px
    border-radius: 0 $radius $radius 0
    &.delete
      background-color: indianred

  &.closed .meal-quantity
    transition: border-radius 0.5s ease-in-out
    border-radius: 0 $radius 0 0


.v-enter-active,
.v-leave-active
  transition: line-height 0.5s ease, opacity 0.5s ease, color 0.5s ease-in-out


.v-enter-from,
.v-leave-to
  line-height: 0
  opacity: 0
  color: transparent


</style>