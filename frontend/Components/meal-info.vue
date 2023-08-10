<script setup lang="js">
import {OnClickOutside} from "@vueuse/components";

const active = ref("closed")

</script>

<template>
  <OnClickOutside @trigger="active='closed'">
    <div class="meal-holder" :class="[active]" @click="active='open'">
      <div class="meal-info">
        <div class="pet-info">
          <div class="pet fed"></div>
          <div class="pet"></div>
        </div>
        <div class="meal-details">
          <b class="bold" id="food-type">Food type</b>
          <p id="time">12:30 Uhr</p>
        </div>
      </div>
      <div class="meal-quantity">
        <b class="bold" id="quantity">100g</b>
      </div>
    </div>
  </OnClickOutside>
</template>

<style scoped lang="sass">
@import "assets/_colors"

@include  text-standard
.meal-holder
  display: flex
  width: 320px
  height: $meal-height
  flex-direction: row
  gap: 0
  box-shadow: $default-shadow
  transition: all 0.4s ease-in-out
  border-radius: $radius

  &.open
    height: $meal-height + 100px
    flex-direction: column

  .meal-info
    @include all-center
    border-radius: $radius 0 0 $radius
    flex: 1
    width: 270px
    height: $meal-height
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
      width: 100%

  .meal-quantity
    @include all-center
    background-color: $primary-blue
    width: 60px
    height: $meal-height
    border-radius: 0 $radius $radius 0


</style>