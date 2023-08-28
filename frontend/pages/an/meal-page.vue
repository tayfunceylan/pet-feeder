<script setup lang="js">
const date = ref(new Date().toISOString().substring(0, 10))
const dateMeals = ref(null)

//define useStores Authentication and Pets
const authStore = useAuthStore()
const petStore = usePetsStore()

// variables for hard-refresh
const mealcounter = ref(0)
const counter = ref(0)

onMounted(async () => {
  // when page is loaded fetch the meal and pets
  await  fetchMealList()
  await petStore.fetchPets()
})

async function fetchMealList(){
  // fetch meal from API and add the data to ref, if not null
  const listResponse = await fetchMealListURL(authStore, date.value)
  dateMeals.value = listResponse?.data
  mealcounter.value++
  // increase meal counter to hard-reset the meal-list through :key
}

const changeDate = (day) => {
  // Change the date to the next day +1 for tomorrow and -1 for yesterday
  let temp = date.value
  const currentDate = new Date(temp)
  const nextDate = new Date(currentDate)
  nextDate.setDate(currentDate.getDate() + day)
  // set the date.value and refresh the meal list
  date.value = nextDate.toISOString().substring(0, 10)
  fetchMealList()
}

const addMeal = () => {
  // add a temp meal, to the list. this meal will be posted upon saving in meal-card
  let meal = {
    quantity: 0,
    food: 1,
    pet: [],
    time: Date.now()
  }
  dateMeals.value.meals.push(meal)
}
</script>>

<template>
    <div class="date-picker" :key="counter">
      <button @click="changeDate(-1)">&lt</button>
      <input type="date" v-model="date">
      <button @click="changeDate(1)">></button>
    </div>

    <p v-if="!dateMeals && !petStore.pets">Loading ...</p>
    <div v-else class="meal-list" :key="mealcounter">
      <button class="add" @click="addMeal">+</button>
      <meal-card v-for="meal in dateMeals.meals" :petsList="petStore.pets" :mealID="meal" @refresh-list="fetchMealList"/>
    </div>
</template>

<style scoped lang="sass">
@import "assets/colors"
p
  @include text-standard

.meal-list
  @include all-center
  background-color: $background-dark
  width: 100vw
  padding-bottom: 50px + $navbar-height
  flex-direction: column
  gap: 15px


.date-picker
  margin-top: $navbar-height
  display: flex
  height: 80px
  flex-direction: row
  justify-content: space-evenly
  align-items: center

  *
    @include text-style-normal

input
  background-color: $background-bright
  padding: 5px 15px 5px 15px
  border-radius: 8px
button
  @include text-style-normal
  background-color: $background-bright
  border-radius: 50px
  width: 30px
  height: 30px

.add
  width: 200px
  transition: 0.7s ease-in-out
  &:active
    width: 220px
  &:active
    opacity: 0.8
    background-color: white

</style>