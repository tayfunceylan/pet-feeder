<template>
  <v-toolbar color="secondary">
    <v-spacer></v-spacer>
    <v-btn>&lt</v-btn>
    <v-btn>Heute</v-btn>
    <v-btn>></v-btn>
    <v-spacer></v-spacer>
  </v-toolbar>

  {{ petList }}
  
  <v-table v-for="category in categories">
    <thead @click=editMeal(NaN)>
    <tr>
      <th>
        {{ category.name }}
      </th>
      <th v-for="n in Math.max(0, category.meals.length - 1)">
      </th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="meal in category.meals" :key="meal.time" @click=editMeal(meal)>
      <td>{{ petsToString(meal.pets) }}</td>
      <td>{{ meal.quantitiy + foods[meal.food].unit }}</td>
      <td>{{ toTimeString(meal.time) }}</td>
    </tr>
    </tbody>
  </v-table>

  <v-dialog v-model=dialog width="700">
    <v-card>
        <v-card-item>
          <v-row  class="mt-4">
            <v-col cols="12" md="4">
              <v-select label="Pets" :items=petList item-title="name" item-value="id" v-model=selectedMeal.pets
                        variant="outlined" multiple></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field :label="`Menge in ${selectedMeal.food.length ? foods[selectedMeal.food].unit : ''}`"
                            v-model=selectedMeal.quantitiy variant="outlined" type="number"></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-select label="Futter" :items=foodList item-title="name" item-value="id" v-model=selectedMeal.food
                        variant="outlined"></v-select>
            </v-col>
          </v-row>
          <v-row class="justify-space-evenly mb-3">
            <v-card-actions>
              <v-btn color="primary" block @click="dialog = false">Close</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn color="primary" block @click=duplicateMeal()>Duplicate</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn color="primary" block @click=saveMeal()>Save</v-btn>
            </v-card-actions>
          </v-row>
        </v-card-item>
    </v-card>
  </v-dialog>
  <p>{{ meals }}</p>
  <br>
  <br>
  <p>{{ date }}</p>
  <br>
  <br>
  <v-btn color="primary"  @click=refresh>Refresh data</v-btn>
  <v-btn color="primary"  @click=postdata>post data</v-btn>
  <v-btn color="primary"  @click=logout>Logout</v-btn>
</template>

<script setup lang="ts">
// get date in format YYYY-MM-DD
let date = new Date().toISOString().slice(0, 10)

// fetch data from backend and date in params
const { data: meals, refresh } = await useFetch('/api/meal/get_day/',
  {
    query: {
      date: date,
    },
    // redirect to /api/auth/login if status is 403
    onResponse({ response }) {
      if (response.status == 403) {
        window.location.href = '/api/auth/login'
      }
    },
  },
)
// fetch data from backend and date in params
const { data: petList } = await useFetch('/api/pet/')

// petList contains results
// set petList to petList.results


const foodList = ref()
foodList.value = [
  {
    id: 1,
    name: 'MjAMjAM',
    unit: 'g',
  },
  {
    id: 2,
    name: 'Animonda',
    unit: 'g',
  }
]

// const petList = ref()
petList.value = [
  {
    id: 1,
    name: 'Manga',
  },
  {
    id: 2,
    name: 'Duman',
  }
]

const reduceList = (list: any[]) => {
  return list.reduce((obj: any, item: any) => {
    obj[item.id] = item
    return obj
  }, {})
}

const pets = ref(reduceList(petList.value))
const foods = ref(reduceList(foodList.value))

const categories = ref()
categories.value = [
  {
    name: 'Nassfutter',
    meals: [
      {
        id: 1,
        pets: [1, 2],
        quantitiy: 60,
        time: 1691110294,
        food: 1,
      },
      {
        id: 2,
        pets: [1, 2],
        quantitiy: 80,
        time: 1691110294,
        food: 1,
      },
      {
        id: 3,
        pets: [1, 2],
        quantitiy: 100,
        time: 1691110294,
        food: 1,
      },
    ],
  },
  {
    name: 'Trockenfutter',
    meals: [
      {
        id: 4,
        pets: [1, 2],
        quantitiy: 70,
        time: 1691110294,
        food: 1,
      },
      {
        id: 5,
        pets: [1],
        quantitiy: 90,
        time: 1691110294,
        food: 1,
      },
      {
        id: 6,
        pets: [1, 2],
        quantitiy: 110,
        time: 1691110294,
        food: 2,
      },
    ],
  },
  {
    name: 'Snacks',
    meals: [],
  }
]

// dialog pops up when dialog = true
const dialog = ref(false)

// function that turns timestamp into a date string HH:MM
const toTimeString = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleTimeString('de-DE', {
    hour: '2-digit',
    minute: '2-digit',
  }) + ' Uhr'
}

// pets: [1, 2], -> pets: "Manga, Duman"
// join with .join(", ")
const petsToString = (petsList: number[]) => {
  return petsList.map((petID) => pets.value[petID].name).join(', ')
}

const petIdsToList = (petIds: number[]) => {
  return petIds.map((petID) => pets.value[petID].name)
}

const selectedMeal = ref()

const editMeal = (meal: any) => {
  selectedMeal.value = {
    pets: [],
    quantitiy: "",
    food: [],
  }
  if (meal) {
    selectedMeal.value.id = meal.id
    selectedMeal.value.pets = meal.pets
    selectedMeal.value.quantitiy = meal.quantitiy
    selectedMeal.value.food = meal.food
  }
  dialog.value = true
}

const saveMeal = async (duplicate: boolean = false) => {
  var id = duplicate ? NaN : selectedMeal.value.id
  var pets = petIdsToList(selectedMeal.value.pets)
  var quantitiy = selectedMeal.value.quantitiy + foods.value[selectedMeal.value.food].unit
  var food = foods.value[selectedMeal.value.food]
  console.log(`id: ${id} pets: ${pets} quantitiy: ${quantitiy} food: ${food.name}`)
  // do post request to /api/meal
  // with body: {pet: pets, quantitiy: quantitiy, food: food}
  await useFetch('/api/meal/', {
    method: 'POST',
    body: {
      csrftoken: useCookie('csrftoken'),
      pet: pets,
      quantitiy: quantitiy,
      food: food,
    },
    onResponse({ response }) {
      if (response.status == 200) {
        refresh()
        dialog.value = false
      }
    },
  })
}

const postdata = async () => {
  // fetch /api first to get csrftokenmiddlewaretoken
  // content type is text/html
  await useFetch('/api/token', {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
    },
    onResponse({ response }) {
      if (response.status == 200) {
        // print response to console
        
      }
    },
  })
  // do post request to /api/meal
  // await useFetch('/api/meal/', {
  //   method: 'POST',
  //   body: {
  //     pet: [1,2],
  //     quantitiy: 123,
  //     food: 1,
  //   },
  //   onResponse({ response }) {
  //     if (response.status == 200) {
  //       refresh()
  //       dialog.value = true
  //     }
  //   },
  // })
}

const duplicateMeal = () => {
  saveMeal(true)
}

const logout = async () => {
  await useFetch('/api/auth/logout', {
    onResponse({ response }) {
      if (response.status == 200) window.location.href = '/api/auth/login'
    },
  })
}
</script>