<template>
  <v-app>
    <v-app-bar :elevation="2">
      <v-app-bar-title>
        <v-progress-circular model-value=100 :indeterminate=loading size=25 color="primary"/>
        Pet Feeder
      </v-app-bar-title>
      
      <v-btn @click="refreshData" icon="mdi-refresh"></v-btn>
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-dots-vertical"></v-btn>
        </template>
        
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Ausloggen</v-list-item-title>
          </v-list-item>
          <v-list-item @click="test">
            <v-list-item-title>Einstellugen</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    
    <v-main>
      <v-toolbar color=white flat>
        <v-spacer></v-spacer>
        <v-btn @click=jumpdays(-1) icon="mdi-step-backward" variant="plain"/>
        <v-menu location="bottom center" v-model:model-value="dateDialog">
          <template v-slot:activator="{ props }">
            <v-btn width="70"  v-bind="props" variant="plain">
              {{ dayAsText }}
            </v-btn>

            <!-- <v-date-picker 
              @click:save=updateDay() 
              @click:cancel="dateDialog = false"
              color="primary" 
              elevation="5" 
              v-model=datePicker
              show-adjacent-months></v-date-picker> -->
          </template>

          <VueDatePicker class="elevation-24" inline auto-apply locale="de"
            v-model=datePicker
            @update:model-value=updateDay()
            :enable-time-picker="false"/>
        </v-menu>
        <v-btn @click=jumpdays(+1) icon="mdi-step-forward" variant="plain"/>
        <v-spacer></v-spacer>
      </v-toolbar>
    
      <v-table v-for="(mealsOfCat, category) in meals.data.value.meals">
        <thead @click=editMeal(NaN)>
        <tr>
          <th> {{ category }} </th>
          <th v-for="n in 2"></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="meal in mealsOfCat" :key="meal.time" @click=editMeal(meal)>
          <td>{{ petsToString(meal.pets) }}</td>
          <td>{{ meal.quantity + foodsMap[meal.food].unit }}</td>
          <td>{{ toTimeString(meal.time) }}</td>
        </tr>
        </tbody>
      </v-table>
    
      <v-dialog v-model=dialog width="700">
        <v-card>
            <v-card-item>
              <v-row  class="mt-4">
                <v-col cols="12" md="4">
                  <!-- <VueDatePicker 
                  time-picker mode-height="120" 
                  v-model=selectedMeal.time/> -->
                </v-col>
                <v-col cols="12" md="4">
                  <v-select label="Pets" :items=pets.data.value.results item-title="name" item-value="id" v-model=selectedMeal.pets
                            variant="outlined" multiple></v-select>
                </v-col>
                <v-col>
                  <v-select label="Futter" :items=foods.data.value.results item-title="name" item-value="id" v-model=selectedMeal.food
                            variant="outlined"></v-select>
                </v-col>
                <v-col >
                  <v-text-field :label="`Menge in ${selectedMeal.food.length ? foodsMap[selectedMeal.food].unit : ''}`"
                                v-model=selectedMeal.quantity variant="outlined" type="number"></v-text-field>
                </v-col>
              </v-row>
              <v-row class="justify-space-evenly mb-3">
                <v-card-actions>
                  <v-btn color="primary" block @click="dialog = false">
                    <v-icon
                      size="large"
                      icon="mdi-close"
                    ></v-icon>
                  </v-btn>
                </v-card-actions>
                <v-card-actions>
                  <v-btn color="primary" block @click=duplicateMeal()>
                    <v-icon
                      size="large"
                      icon="mdi-content-duplicate"
                    ></v-icon></v-btn>
                </v-card-actions>
                <v-card-actions>
                  <v-btn color="primary" block @click=saveMeal()>
                    <v-icon
                      size="large"
                      icon="mdi-content-save"
                    ></v-icon>
                  </v-btn>
                </v-card-actions>
                <v-card-actions v-if=selectedMeal.id>
                  <v-btn color="primary" block @click=delMeal()>
                    <v-icon
                      size="large"
                      color="red"
                      icon="mdi-delete"
                    ></v-icon>
                  </v-btn>
                </v-card-actions>
              </v-row>
            </v-card-item>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
const loading = ref(false)
const datePicker = ref(new Date())

// fetch data from backend and date in params
let mealsPromise = getMealsDate(datePicker.value.toLocaleDateString('en-CA'))
let petsPromise = getPets()
let foodsPromise = getFoods()
const meals: any = await mealsPromise
const pets: any = await petsPromise
const foods: any = await foodsPromise

const petsMap = ref(reduceList(pets.data.value.results))
const foodsMap = ref(reduceList(foods.data.value.results))

// dialog pops up when dialog = true
const dialog = ref(false)
const dateDialog = ref(false)

// pets: [1, 2], -> pets: "Manga, Duman"
// join with .join(", ")
const petsToString = (petsList: number[]) => {
  return petsList.map((petID) => petsMap.value[petID].name).join(', ')
}

const petIdsToList = (petIds: number[]) => {
  return petIds.map((petID) => petsMap.value[petID].name)
}

const selectedMeal = ref()

const editMeal = (meal: any) => {
  console.log(meal.id)
  selectedMeal.value = {
    pet: [],
    quantity: "",
    food: [],
  }
  if (meal) {
    selectedMeal.value.id = meal.id
    selectedMeal.value.pets = meal.pets
    selectedMeal.value.quantity = meal.quantity
    selectedMeal.value.food = meal.food
  }
  dialog.value = true
}

const saveMeal = async (duplicate: boolean = false) => {
  let meal: any = selectedMeal.value
  if (duplicate) meal.id = NaN
  await postMeal(meal.food, meal.quantity, meal.pets, meal.id)
  meals.refresh()
  dialog.value = false
}

const duplicateMeal = () => {
  saveMeal(true)
}

const updateDay = async () => {
  const newResult = await getMealsDate(datePicker.value.toLocaleDateString('en-CA'))
  meals.data.value = newResult.data.value
  meals.pending = newResult.pending
  meals.error = newResult.error
  meals.refresh = newResult.refresh

  dayAsText.value = dayToText()
  dateDialog.value = false
}

const jumpdays = async (offset: number) => {
  datePicker.value.setDate(datePicker.value.getDate() + offset)
  await updateDay()
}

const delMeal = async () => {
  await deleteMeal(selectedMeal.value.id);
  updateDay();
  dialog.value = false;
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


const test = () => {
  console.log("test")
}

const refreshData = async () => {
  loading.value = true
  await Promise.all([meals.refresh(), pets.refresh(), foods.refresh()])
  loading.value = false
}

const dayAsText = ref(dayToText())
</script>