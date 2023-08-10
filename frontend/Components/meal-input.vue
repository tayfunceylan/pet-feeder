<script setup lang="ts">
defineProps(['active', 'fed', 'pets', 'num_pets', 'food', 'time', 'quantity', 'unit'])
defineEmits(['open-meal'])


const feeding = ref([])
</script>

<template>
  <Transition>
    <div class="meal-input-wrap">
      <div  class="pet-selector">
        <div v-for="pet in pets" id="{{pet}}" class="pets" :style="{backgroundColor: '#9ac1ed'}">

        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped lang="sass">
@import "assets/colors"
@include text-standard

.pet-selector
  display: flex
  flex-direction: row
  align-content: space-between
  justify-content: space-evenly
  width: 100%

.pets
  width: 50px
  height: 50px
  border-radius: 50%

.v-enter-active,
.v-leave-active
  transition: all 0.5s ease


.v-enter-from,
.v-leave-to
  opacity: 0

</style>