<script setup lang="ts">

</script>

<template>
<div class="meal-holder">
  <div class="meal-info">
    <div class="pet-info">
      <div class="pet fed"></div>
      <div class="pet"></div>
    </div>
    <div class="meal-details">
      <b class="bold">Food type</b>
      <p>12:30 Uhr</p>
    </div>
  </div>
  <div class="meal-quantity">
    <b class="bold">100g</b>
  </div>
</div>
</template>

<style scoped lang="sass">
@import "assets/_colors"

.meal-holder
  display: flex
  width: 320px
  height: 100px
  flex-direction: row
  gap: 0
  box-shadow: $default-shadow

.meal-info
  border-radius: 5px 0 0 5px
  display: flex
  flex: 1
  width: 270px
  height: 100px
  background-color: $background-bright
  align-items: center
  justify-content: space-evenly
  align-content: center
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
    flex: 2
    width: 120px
    height: 30px
    display: flex
    flex-direction: column
    justify-content: center
    align-items: center
    flex-shrink: 0

.meal-quantity
  background-color: $primary-blue
  width: 60px
  height: 100px
  display: flex
  justify-content: center
  align-items: center
  border-radius: 0 5px 5px 0


</style>