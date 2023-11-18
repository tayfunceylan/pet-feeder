<template>
  <v-app>
    <!-- app bard -->
    <v-app-bar :elevation="2">
      <v-app-bar-title>
        <v-progress-circular v-model=ws.isConnected :indeterminate=ws.isLoading size=25 color="primary" />
        <NuxtLink to="/" style="text-decoration: none; color: inherit;">
          Pet Feeder
        </NuxtLink>
      </v-app-bar-title>

      <v-btn @click="meals.datePicker = new Date();" icon="mdi-undo" />
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

    <v-main v-if="meals.error">
      {{ meals.date }}
      <v-alert type="error" dismissible>
        {{ meals.error }}
      </v-alert>
      <v-alert type="info" dismissible>
        maybe try to refresh page
      </v-alert>
    </v-main>
    <v-main v-else-if="[meals, foods, pets, helper].some((resp) => resp.data == null)">
    </v-main>
    <v-main v-else>
      <!-- date picker -->
      <v-container class="mt-3">
        <v-row justify="center" align="center">
          <v-btn @click=meals.jumpdays(-1) icon="mdi-step-backward" variant="plain" />
          <v-menu location="bottom center" v-model:model-value="dateDialog">
            <template v-slot:activator="{ props }">
              <v-btn width="90" v-bind="props" variant="plain">
                {{ dayAsText }}
              </v-btn>
            </template>
            <VueDatePicker class="elevation-24" inline auto-apply locale="de" v-model=meals.datePicker
              @update:model-value='dateDialog=false' :enable-time-picker="false" />
          </v-menu>
          <v-btn @click=meals.jumpdays(+1) icon="mdi-step-forward" variant="plain" />
        </v-row>
      </v-container>

      <!-- listing of meals -->
      <v-list item-props lines="two" v-auto-animate>
        <v-list-item v-if="meals.data.results.length == 0">
          Keine Meals für diesen Tag
        </v-list-item>
        <template v-for="(meal, index) in meals.data.results" :key="meal.id">
          <v-list-item @click="editMeal(meal)">
            <v-list-item-title>{{ toTimeString(meal.fed_at) }}</v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">
                {{ `${meal.quantity}${foods.data[meal.food].unit}
                                ${helper.data.maps.categories[foods.data[meal.food].category]}` }}
              </span>
              &mdash; {{ foods.data[meal.food].name }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider v-if="index < meals.data.results.length - 1" />
        </template>
        <v-list-item @click="editMeal(null)">
          <v-btn block color="grey-darken-2" variant="outlined">
            ADD MEAL
          </v-btn>
        </v-list-item>
      </v-list>

      <!-- listing of schedules -->
      <v-list item-props lines="two" v-auto-animate v-if="schedules.data.active">
        <p @click="editSchedule(null)" class="text-h5 ml-4 mt-3">
          Schedules
        </p>
        <template v-for="schedule, index in schedules.data.results" :key="schedule.id">
          <v-list-item @click="editSchedule(schedule)">
            <v-list-item-title>{{ getScheduleTimeString(schedule.hour, schedule.minute) }}
              <a class="font-italic text-disabled">Amount: {{ schedule.amount * 8 }}g</a>
            </v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">Mo Di Mi Do Fr Sa So</span>
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider v-if="index < schedules.data.results.length - 1" />
        </template>
        <v-list-item @click="editSchedule(null)">
          <v-btn block color="grey-darken-2" variant="outlined">
            ADD SCHEDULE
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
                <v-chip v-for="pet in pets.data.results" @click="addOrRemovePet(pet.id)" class="mb-2 ma-1"
                  :color="selectedMeal && selectedMeal.pets.includes(pet.id) ? 'indigo' : 'grey'" text-color="white"
                  prepend-icon="mdi-account-circle">
                  {{ pet.name }}
                </v-chip>
              </div>
              <v-divider />
              <!-- select food category -->
              <div class="mt-2 mb-2">
                <v-chip v-for="category in helper.data.lists.categories" @click="selectCategory(category)"
                  class="mb-2 ma-1" :color="selectedMeal.category == category.k ? 'deep-purple' : 'grey'"
                  text-color="white" prepend-icon="mdi-cards-outline">
                  {{ category.v }}
                </v-chip>
              </div>
              <!-- select food -->
              <template v-if="selectedMeal.category">
                <v-divider />
                <div class="mt-2 mb-2">
                  <template v-for="food in foods.data">

                    <v-chip v-if="selectedMeal.category == foods.data[food.id].category" @click="selectFood(food)"
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
                      :label="`Menge in ${selectedMeal.food ? foods.data[selectedMeal.food].unit : ''}`"
                      v-model=selectedMeal.quantity variant="outlined" type="number" />
                  </v-col>
                  <v-col class="mt-1">
                    <v-chip v-for="quantity in foods.data[selectedMeal.food].top_quantities"
                      @click="selectedMeal.quantity = quantity" class="mb-2 ma-1"
                      :color="selectedMeal.quantity == quantity ? 'purple' : 'grey'" text-color="white">
                      {{ `${quantity}${foods.data[selectedMeal.food].unit}` }}
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

      <!-- dialog to save and edit schedules -->
      <v-dialog v-model="selectedSchedule">
        <v-sheet>
          <v-container>
            <v-form>
              <VueDatePicker time-picker v-model=selectedSchedule.timePicker mode-height="170" class="mb-10" />
              <!-- select pets -->

              <v-slider v-model="selectedSchedule.amount" :min="1" :max="10" :step="1" thumb-label="always"
                color="indigo">
                <template v-slot:thumb-label="{ modelValue }">
                  {{ modelValue * 8 }}g
                </template>
              </v-slider>

              <v-chip v-for="day in ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']" @click="" class="mb-2 ma-1"
                :color="true ? 'indigo' : 'grey'" text-color="white">
                {{ day }}
              </v-chip>

              <v-row class="justify-space-evenly mt-4 mb-0">
                <v-btn @click="delSchedule()" rounded variant="outlined" color="grey">
                  <v-icon size="large" color="red" icon="mdi-delete" />
                </v-btn>
                <v-btn @click="saveSchedule()" rounded variant="outlined" color="grey">Save</v-btn>
              </v-row>
            </v-form>
          </v-container>
        </v-sheet>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
// fetch data from backend and date in params
const meals = useMealsStore()
const pets = usePetsStore()
const foods = useFoodsStore()
const helper = useHelperStore()
const schedules = useSchedulesStore()

const ws: any = useWebsocketStore()

const selectedSchedule = ref()
const editSchedule = (schedule: any) => {
  if (schedule) {
    selectedSchedule.value = structuredClone({ ...toRaw(schedule) })
    selectedSchedule.value.timePicker = {
      hours: schedule.hour,
      minutes: schedule.minute,
      seconds: 0
    }
  }
  else {
    let now = new Date()
    selectedSchedule.value = {
      amount: 1,
      active: true,
      timePicker: {
        hours: now.getHours(),
        minutes: 0,
        seconds: 0
      }
    }
  }
}
const saveSchedule = async () => {
  let schedule: any = selectedSchedule.value
  schedule.hour = schedule.timePicker.hours
  schedule.minute = schedule.timePicker.minutes
  await postSchedule(schedule)
  selectedSchedule.value = false
}
const delSchedule = async () => {
  await deleteSchedule(selectedSchedule.value.id);
  selectedSchedule.value = false;
}

const selectedMeal = ref()
const editMeal = (meal: any) => {
  if (meal) {
    let mealDate = new Date(meal.fed_at * 1000)
    selectedMeal.value = structuredClone({ ...toRaw(meal) })
    selectedMeal.value.category = foods.data[meal.food].category
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
      fed_at: meals.datePicker,
      timePicker: {
        hours: now.getHours(),
        minutes: now.getMinutes(),
        seconds: now.getSeconds()
      }
    }
  }
}
const saveMeal = async () => {
  let meal: any = selectedMeal.value
  meal.fed_at.setHours(meal.timePicker.hours)
  meal.fed_at.setMinutes(meal.timePicker.minutes)
  meal.fed_at.setSeconds(meal.timePicker.seconds)
  await postMeal(meal)
  selectedMeal.value = false
}
const delMeal = async () => {
  await deleteMeal(selectedMeal.value.id);
  selectedMeal.value = false;
}

const dateDialog = ref(false)

const dayToText = () => {
  // return today, tomorrow, yesterday, or date
  const today = new Date()
  // total numbers of days between today and selected date
  let diff = Math.round((meals.datePicker.getTime() - today.getTime()) / (1000 * 3600 * 24))
  if (diff === 0) return 'Heute'
  if (diff === 1) return 'Morgen'
  if (diff === -1) return 'Gestern'
  return meals.datePicker.toLocaleDateString('de-DE', {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric'
  })
}
const dayAsText = computed(dayToText)

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
  selectedMeal.value.quantity = foods.data[food.id].top_quantities[0]
}

window.addEventListener('keydown', (e) => {
  if (e.key == 'ArrowLeft') meals.jumpdays(-1)
  if (e.key == 'ArrowRight') meals.jumpdays(+1)
})
</script>