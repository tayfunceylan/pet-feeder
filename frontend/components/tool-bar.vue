<script setup lang="ts">

const active_elm = ref("one")

</script>

<template>
  <div class="tool-height">
    <div class="tool-holder">
      <div class="active" :class="[active_elm]"></div>
      <div class="nav-button">
        <NuxtLink class="bold" to="/food-page" @click="active_elm = 'zero'">food</NuxtLink>
      </div>
      <div class="nav-button">
        <NuxtLink class="bold" to="/meal-page" @click="active_elm = 'one'">meal</NuxtLink>
      </div>
      <div class="nav-button">
        <NuxtLink class="bold" to="/pet-page" @click="active_elm = 'two'">pet</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped lang="sass">
/* Define the variables and mixins for this component */
@use "sass:math"
@import "assets/colors"
$bar-radius: 50px
$bar-width: 250px
$button-width: math.div($bar-width, 3)

@mixin button-design
  @include all-center
  width: math.div($bar-width, 3)
  height: 50px
  border-radius: $bar-radius

/* Style this component */
.tool-height
  @include all-center
  position: fixed
  bottom: 50px
  width: 100vw
  border-radius: $bar-radius

  .tool-holder
    @include all-center
    background-color: $background-bright
    flex-direction: row
    width: $bar-width
    height: 50px
    justify-content: space-evenly
    border-radius: $bar-radius
    box-shadow: $default-shadow

    .nav-button
      @include button-design

.bold
  text-decoration: none
  font-size: $bold-size
  color: $default-text-color


.active
  @include all-center
  @include button-design
  pointer-events: none
  position: absolute
  background-color: $primary-blue
  mix-blend-mode: lighten
  /* calculate the position of the active button */
  transform: translateX(- $button-width + ($button-width * 1))
  transition: transform 0.4s ease-in-out, background-color 0.5s ease-in-out

  &.zero
    background-color: $secondary-red
    transform: translateX(- $button-width + ($button-width * 0))

  &.one
    transform: translateX(- $button-width + ($button-width * 1))

  &.two
    background-color: $secondary-blue
    transform: translateX(- $button-width + ($button-width * 2))



</style>