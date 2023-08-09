<script setup lang="ts">
import {a} from "unplugin-vue-router/dist/options-56006a88";

const active_elm = ref("one")

</script>

<template>
  <div class="tool-height">
    <div class="tool-holder">
      <div class="active" :class="[active_elm]"></div>
      <div class="nav-button">
        <button class="bold" @click="active_elm = 'zero'">food</button>
      </div>
      <div class="nav-button">
        <button class="bold" @click="active_elm = 'one'">meal</button>
      </div>
      <div class="nav-button">
        <button class="bold" @click="active_elm = 'two'">pet</button>
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
  transform: translateX(v-bind(active_x)px)
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