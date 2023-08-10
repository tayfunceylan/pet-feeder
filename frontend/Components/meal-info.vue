<script setup lang="ts">
defineProps(['active', 'pets', 'fed', 'num_pets', 'food', 'time', 'quantity', 'unit'])
defineEmits(['open-meal'])
</script>

<template>
    <div class="meal-holder" :class="[!active? 'open': 'closed']" @click="$emit('open-meal')">
      <div class="meal-info">
        <div class="pet-info">
          <div class="pet" v-for="pet in pets" :class="[fed.includes(pet) ? 'fed' : '']"></div>
        </div>
        <div class="meal-details">
          <Transition>
            <b class="bold" v-if="!active" id="food-type">{{ food }}</b>
          </Transition>
          <p id="time">{{ time }} Uhr</p>
        </div>
      </div>
      <div class="meal-quantity">
        <b class="bold" id="quantity">{{ quantity }}{{ unit }}</b>
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

      .pet
        width: 20px
        height: 20px
        border-radius: 50%
        background-color: $background-dark

      .fed
        background-color: $primary-red

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


.v-enter-active,
.v-leave-active
  transition: line-height 0.5s ease, opacity 0.5s ease, color 0.5s ease-in-out


.v-enter-from,
.v-leave-to
  line-height: 0
  opacity: 0
  color: transparent


</style>