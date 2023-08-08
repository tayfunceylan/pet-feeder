<script setup lang="ts">

</script>

<template>
  <div class="tool-height">
    <div class="tool-holder">
      <div class="active"></div>
      <div class="nav-button">
        <router-link to="food-page" class="bold">food</router-link>
      </div>
      <div class="nav-button">
        <router-link to="meal-page" class="bold">meal</router-link>
      </div>
      <div class="nav-button">
        <router-link to="pet-page" class="bold">pet</router-link>
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
  position: absolute
  background-color: #9ac1ed
  mix-blend-mode: lighten
  /* calculate the position of the active button */
  transform: translateX(- $button-width + ($button-width * 1))


</style>