<template>
  <v-app>
    <v-app-bar :elevation="2">
      <v-app-bar-title>
        <v-progress-circular v-model=isConnected :indeterminate=isLoading size=25 color="primary" />
        <NuxtLink to="/" style="text-decoration: none; color: inherit;">
          Pet Feeder
        </NuxtLink>
      </v-app-bar-title>

      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-dots-vertical" />
        </template>

        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Ausloggen</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main v-if="pets.error.value">
      <v-alert type="error" dismissible>
        {{ pets.error }}
      </v-alert>
      <v-alert type="info" dismissible>
        refresh page
      </v-alert>
    </v-main>
    <v-main v-else-if="[foods, foodOptions, pets, helper].some((item) => item.data.value == null)">
    </v-main>
    <v-main v-else>
      <!-- listing for pets -->
      <v-list item-props lines="three" v-auto-animate>
        <p class="text-h5 ml-4 mt-3">Pets</p>
        <template v-for="(pet, index) in pets.data.value.results">
          <v-list-item @click="editPet(pet)">
            <v-list-item-title>{{ pet.name }}</v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">{{ pet.race }}</span>
              &mdash; {{ pet.description }}
            </v-list-item-subtitle>
            <template v-slot:prepend>
              <v-avatar size="50">
                <v-img :src=pet.picture></v-img>
              </v-avatar>
            </template>
          </v-list-item>
          <v-divider v-if="index < pets.data.value.results.length - 1" inset />
        </template>
      </v-list>

      <!-- listing of foods -->
      <v-list item-props lines="two" v-auto-animate>
        <p @click="editFood(null)" class="text-h5 ml-4 mt-3">
          Foods<v-btn icon="mdi-plus" variant="plain" />
        </p>
        <template v-for="food, index in foods.data.value">
          <v-list-item @click="editFood(food)">
            <v-list-item-title>{{ food.name }}
              <a class="font-italic text-disabled">({{ food.left }} übrig)</a>
            </v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">{{ helper.data.value.maps.categories[food.category] }}</span>
              &mdash; {{ `${food.num_packets}*${food.packet_size}${food.unit} für ${food.price}€ (${food.pl})` }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider v-if="index < foods.data.value.length - 1" />
        </template>
      </v-list>

      <!-- dialog to save and edit pet -->
      <v-dialog v-model="selectedPet">
        <v-sheet>
          <v-container>
            <v-form>
              <v-text-field v-model="selectedPet.name" label="Name" variant="outlined" />
              <v-text-field v-model="selectedPet.race" label="Rasse" variant="outlined" />
              <v-textarea v-model="selectedPet.description" label="Beschreibung" variant="outlined" rows="3" />

              <v-row class="justify-space-evenly">
                <v-btn @click="savePet()">Save</v-btn>
                <!-- <v-btn @click="deletePet()" color="error">Delete</v-btn> -->
              </v-row>
            </v-form>
          </v-container>
        </v-sheet>
      </v-dialog>

      <!-- dialog to save and edit food -->
      <v-dialog v-model="selectedFood">
        <v-sheet>
          <v-container>
            <v-form>
              <v-text-field v-model="selectedFood.name" label="Name" variant="outlined" />
              <v-text-field v-model="selectedFood.brand" label="Marke" variant="outlined" />
              <v-text-field v-model="selectedFood.num_packets" label="Anzahl Packungen" variant="outlined"
                type="number" />
              <v-text-field v-model="selectedFood.packet_size" label="Packungen Größe" variant="outlined" type="number" />
              <v-select v-model="selectedFood.unit" :items=foodOptions.data.value.units item-title="name"
                item-value="value" label="Einheit" variant="outlined" />
              <v-select v-model="selectedFood.category" :items=foodOptions.data.value.categories item-title="name"
                item-value="value" label="Kategorie" variant="outlined" />
              <v-text-field v-model="selectedFood.price" label="Preis in €" variant="outlined" type="number" />

              <v-row class="justify-space-evenly">
                <v-btn @click="saveFood()">Save</v-btn>
                <!-- <v-btn @click="deletePet()" color="error">Delete</v-btn> -->
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

let petsPromise = getPets()
let foodsPromise = getFoods()
let foodOptionsPromise = getFoodOptions()
let helperPromise = getHelper()
const pets: any = await petsPromise
const foods: any = await foodsPromise
const foodOptions: any = await foodOptionsPromise
const helper: any = await helperPromise

const updateFunc = async (e: MessageEvent) => {
  let msg = e.data
  isLoading.value = true
  if (['newPet', null].includes(msg)) pets.refresh()
  if (['newFood', 'newMeal', null].includes(msg)) foods.refresh()
  isLoading.value = false
}

const isConnected = ref(1)
const ws: any = await connectToWebsocket(updateFunc, isConnected, isLoading)

const selectedPet = ref()
const editPet = (pet: any) => {
  selectedPet.value = structuredClone({ ...pet })
}
const savePet = async () => {
  isLoading.value = true
  await postPet(selectedPet.value)
  selectedPet.value = false
  isLoading.value = false
}

const selectedFood = ref()
const editFood = (pet: any) => {
  if (pet) selectedFood.value = JSON.parse(JSON.stringify(pet))
  else selectedFood.value = {
    name: null,
    brand: null,
    category: null,
    price: null,
    unit: null,
    num_packets: null,
    packet_size: null,
  }

}
const saveFood = async () => {
  isLoading.value = true
  let food = selectedFood.value
  food.amount = food.num_packets * food.packet_size
  await postFood(selectedFood.value)
  selectedFood.value = false
  isLoading.value = false
}

// on unmount disconnect from websocket
onUnmounted(() => {
  console.log('disconnecting from websocket')
  ws.customClose()
})
</script>