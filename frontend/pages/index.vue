<template>
  <v-app>
    <v-app-bar :elevation="2">
      <v-app-bar-title>
        <v-progress-circular v-model=isConnected :indeterminate=isLoading size=25 color="primary" />
        <NuxtLink to="/" style="text-decoration: none; color: inherit;">
          Pet Feeder
        </NuxtLink>
      </v-app-bar-title>

      <v-btn @click="datePicker = new Date(); updateDay()" icon="mdi-undo" />
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-dots-vertical" />
        </template>

        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Ausloggen</v-list-item-title>
          </v-list-item>
          <v-list-item to="/settings">
            <v-list-item-title>Einstellugen</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main v-if="meals.error.value">
      <v-alert type="error" dismissible>
        {{ meals.error }}
      </v-alert>
      <v-alert type="info" dismissible>
        maybe try to refresh page
      </v-alert>
    </v-main>
    <v-main v-else-if="[meals, foods, pets, helper].some((item) => item.data.value == null)">
    </v-main>
    <v-main v-else>
      <v-container class="mt-3">
        <v-row justify="center" align="center">
          <v-btn @click=jumpdays(-1) icon="mdi-step-backward" variant="plain" />
          <v-menu location="bottom center" v-model:model-value="dateDialog">
            <template v-slot:activator="{ props }">
              <v-btn width="90" v-bind="props" variant="plain">
                {{ dayAsText }}
              </v-btn>
            </template>
            <VueDatePicker class="elevation-24" inline auto-apply locale="de" v-model=datePicker
              @update:model-value=updateDay() :enable-time-picker="false" />
          </v-menu>
          <v-btn @click=jumpdays(+1) icon="mdi-step-forward" variant="plain" />
        </v-row>
      </v-container>

      <!-- listing of meals -->
      <v-list item-props lines="two" v-auto-animate>
        <v-list-item v-if="meals.data.value.meals.length == 0">
          Keine Meals für diesen Tag
        </v-list-item>
        <template v-for="(meal, index) in meals.data.value.meals" :key="meal.id">
          <v-list-item @click="editMeal(meal)">
            <v-list-item-title>{{ toTimeString(meal.fed_at) }}</v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">
                {{ `${meal.quantity}${foods.data.value[meal.food].unit}
                                ${helper.data.value.maps.categories[foods.data.value[meal.food].category]}` }}
              </span>
              &mdash; {{ foods.data.value[meal.food].name }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider v-if="index < meals.data.value.meals.length - 1" />
        </template>
        <v-list-item @click="editMeal(null)">
          <v-btn block color="grey-darken-2" variant="outlined">
            ADD MEAL
          </v-btn>
        </v-list-item>
      </v-list>

      <!-- dialog to save and edit meals -->
      <v-dialog v-model="selectedMeal">
        <v-sheet>
          <v-container>
            <v-form>
              <VueDatePicker time-picker v-model=selectedMeal.timePicker mode-height="170" class="mb-6" />
              <!-- select pets -->
              <div class="mt-2 mb-2">
                <v-chip v-for="pet in pets.data.value.results" @click="addOrRemovePet(pet.id)" class="mb-2 ma-1"
                  :color="selectedMeal && selectedMeal.pets.includes(pet.id) ? 'indigo' : 'grey'" text-color="white"
                  prepend-icon="mdi-account-circle">
                  {{ pet.name }}
                </v-chip>
              </div>
              <v-divider />
              <!-- select food category -->
              <div class="mt-2 mb-2">
                <v-chip v-for="category in helper.data.value.lists.categories" @click="selectCategory(category)"
                  class="mb-2 ma-1" :color="selectedMeal.category == category.k ? 'deep-purple' : 'grey'"
                  text-color="white" prepend-icon="mdi-cards-outline">
                  {{ category.v }}
                </v-chip>
              </div>
              <!-- select food -->
              <template v-if="selectedMeal.category">
                <v-divider />
                <div class="mt-2 mb-2">
                  <template v-for="food in foods.data.value">

                    <v-chip v-if="selectedMeal.category == foods.data.value[food.id].category" @click="selectFood(food)"
                      class="mb-2 ma-1" :color="selectedMeal.food == food.id ? 'purple' : 'grey'" text-color="white"
                      prepend-icon="mdi-cards-outline">
                      {{ food.name }}
                    </v-chip>
                  </template>
                </div>
              </template>
              <!-- select quantity -->
              <template v-if="selectedMeal.food">
                <v-divider />
                <v-row no-gutters class="mt-6">
                  <v-col cols="4" class="mr-4">
                    <v-text-field density="compact"
                      :label="`Menge in ${selectedMeal.food ? foods.data.value[selectedMeal.food].unit : ''}`"
                      v-model=selectedMeal.quantity variant="outlined" type="number" />
                  </v-col>
                  <v-col class="mt-1">
                    <v-chip v-for="quantity in foods.data.value[selectedMeal.food].top_quantities"
                      @click="selectedMeal.quantity = quantity" class="mb-2 ma-1"
                      :color="selectedMeal.quantity == quantity ? 'purple' : 'grey'" text-color="white">
                      {{ `${quantity}${foods.data.value[selectedMeal.food].unit}` }}
                    </v-chip>
                  </v-col>
                </v-row>
              </template>

              <v-row class="justify-space-evenly mt-4 mb-0">
                <v-btn @click="delMeal()" rounded variant="outlined" color="grey">
                  <v-icon size="large" color="red" icon="mdi-delete" />
                </v-btn>
                <v-btn @click="saveMeal()" rounded variant="outlined" color="grey">Save</v-btn>
              </v-row>
            </v-form>
          </v-container>
        </v-sheet>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
const isLoading = ref(true)

// fetch data from backend and date in params
const datePicker = ref(new Date())
const mealDate = ref(datePicker.value.toLocaleDateString('en-CA'))

// fetch data from backend and date in params
let mealsPromise = getMeals(mealDate)
let petsPromise = getPets()
let foodsPromise = getFoods()
let helperPromise = getHelper()
const meals: any = await mealsPromise
const pets: any = await petsPromise
const foods: any = await foodsPromise
const helper: any = await helperPromise

const updateFunc = async (msg: string) => {
  isLoading.value = true
  if (['newPet', undefined].includes(msg)) pets.refresh()
  if (['newFood', undefined].includes(msg)) foods.refresh()
  if (['newMeal', undefined].includes(msg)) meals.refresh()
  isLoading.value = false
}

const isConnected = ref(1)
const ws: any = await connectToWebsocket(updateFunc, isConnected, isLoading)

const selectedMeal = ref()
const editMeal = (meal: any) => {
  if (meal) {
    let mealDate = new Date(meal.fed_at * 1000)
    selectedMeal.value = structuredClone({ ...toRaw(meal) })
    selectedMeal.value.category = foods.data.value[meal.food].category
    selectedMeal.value.fed_at = mealDate
    selectedMeal.value.timePicker = {
      hours: mealDate.getHours(),
      minutes: mealDate.getMinutes(),
      seconds: mealDate.getSeconds()
    }
  }
  else {
    let now = new Date()
    selectedMeal.value = {
      pets: [1, 2],
      quantity: "",
      food: null,
      fed_at: datePicker.value,
      timePicker: {
        hours: now.getHours(),
        minutes: now.getMinutes(),
        seconds: now.getSeconds()
      }
    }
  }
}
const saveMeal = async () => {
  isLoading.value = true
  let meal: any = selectedMeal.value
  meal.fed_at.setHours(meal.timePicker.hours)
  meal.fed_at.setMinutes(meal.timePicker.minutes)
  meal.fed_at.setSeconds(meal.timePicker.seconds)
  await postMeal(meal)
  selectedMeal.value = false
  isLoading.value = false
}
const delMeal = async () => {
  await deleteMeal(selectedMeal.value.id);
  selectedMeal.value = false;
}

const dateDialog = ref(false)
const updateDay = async () => {
  isLoading.value = true
  mealDate.value = datePicker.value.toLocaleDateString('en-CA')
  isLoading.value = false

  dayAsText.value = dayToText()
  dateDialog.value = false
}
const jumpdays = async (offset: number) => {
  datePicker.value.setDate(datePicker.value.getDate() + offset)
  await updateDay()
  //   ws.onmessage = () => console.log('message received')
}
const dayToText = () => {
  // return today, tomorrow, yesterday, or date
  const today = new Date()
  // total numbers of days between today and selected date
  let diff = Math.round((datePicker.value.getTime() - today.getTime()) / (1000 * 3600 * 24))
  if (diff === 0) return 'Heute'
  if (diff === 1) return 'Morgen'
  if (diff === -1) return 'Gestern'
  return datePicker.value.toLocaleDateString('de-DE', {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric'
  })
}
const dayAsText = ref(dayToText())

const addOrRemovePet = async (id: number) => {
  if (selectedMeal.value.pets.includes(id)) selectedMeal.value.pets = selectedMeal.value.pets.filter((petId: number) => petId !== id)
  else selectedMeal.value.pets.push(id)
}

const selectCategory = async (category: any) => {
  selectedMeal.value.category = selectedMeal.value.category == category.k ? '' : category.k
  selectedMeal.value.food = null
}
const selectFood = async (food: any) => {
  selectedMeal.value.food = selectedMeal.value.food == food.id ? '' : food.id
  selectedMeal.value.quantity = foods.data.value[food.id].top_quantities[0]
}

// on unmount disconnect from websocket
onUnmounted(() => {
  console.log('disconnecting from websocket')
  ws.customClose()
})
</script>