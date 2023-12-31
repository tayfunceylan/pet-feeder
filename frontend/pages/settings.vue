<template>
  <v-app>
    <v-app-bar :elevation="2">
      <v-app-bar-title>
        <v-progress-circular v-model=ws.isConnected :indeterminate=ws.isLoading size=25 color="primary" />
        <NuxtLink to="/" style="text-decoration: none; color: inherit;">
          Pet Feeder
        </NuxtLink>
      </v-app-bar-title>
      <v-btn @click="toggleTheme" icon="mdi-theme-light-dark" />

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

    <v-main v-if="pets.error">
      <v-alert type="error" dismissible>
        {{ pets.error }}
      </v-alert>
      <v-alert type="info" dismissible>
        refresh page
      </v-alert>
    </v-main>
    <v-main v-else-if="[foods, foodOptions, pets, helper].some((resp) => resp.data == null)">
    </v-main>
    <v-main v-else>
      <!-- listing for pets -->
      <v-list item-props lines="three" v-auto-animate>
        <p @click="editPet(null)" class="text-h5 ml-4 mt-3">
          Pets <v-icon class="mb-1" size="25">mdi-plus</v-icon>
        </p>
        <v-list-item v-if="pets.list.length == 0">
          Klicke auf das Plus um ein Haustier hinzuzufügen
        </v-list-item>
        <template v-for="(pet, index) in pets.list" :key="pet.id">
          <v-list-item @click="editPet(pet)">
            <v-list-item-title>{{pet.name}}
              <span class="font-italic text-disabled">
              {{`(${getAge(pet.birthday_on)})`}}
              </span>
            </v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">{{ pet.race }}</span>
              &mdash; {{ pet.description }}
            </v-list-item-subtitle>
            <template v-slot:prepend>
              <v-avatar size="50">
                <v-img :src=baseURL+pet.picture></v-img>
              </v-avatar>
            </template>
          </v-list-item>
          <v-divider v-if="index < pets.list.length - 1" inset />
        </template>
      </v-list>

      <!-- listing of foods -->
      <v-list item-props lines="two" v-auto-animate>
        <p @click="editFood(null)" class="text-h5 ml-4 mt-3">
          Foods <v-icon class="mb-1" size="25">mdi-plus</v-icon>
        </p>
        <v-list-item v-if="foods.list.length === 0 ">
          Klicke auf das Plus um ein Futter hinzuzufügen
        </v-list-item>
        <template v-for="food, index in foods.list" :key="food.id">
          <v-list-item @click="editFood(food)">
            <v-list-item-title> <a :class="[food.active?'':'text-disabled']">{{ food.name+" " }}</a>
              <a class="font-italic text-disabled">({{ food.left }} übrig)</a>
            </v-list-item-title>
            <v-list-item-subtitle>
              <span class="text-primary">{{ helper.data.maps.categories[food.category] }}</span>
              &mdash; {{ `${food.num_packets}*${food.packet_size}${food.unit} für ${food.price}€ (${food.pl})` }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider v-if="index < foods.list.length - 1" />
        </template>
      </v-list>

      <!-- dialog to save and edit pet -->
      <v-dialog v-model="selectedPet.dialog">
        <v-sheet>
          <v-container>
            <v-form>
              <v-container>
                <v-row>
                  <v-avatar size="60" class="mr-2">
                    <v-img :src="baseURL+(selectedPet.picture??'/images/default.png')" alt="pic"
                    ></v-img>
                  </v-avatar>
                  <v-file-input v-model="selectedPet.image" label="Upload Picture"></v-file-input>
                </v-row>
              </v-container>
              <VueDatePicker class="mb-5" auto-apply locale="de" :enable-time-picker="false" v-model="selectedPet.datePicker" :format="dateFormat" />
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
      <v-dialog v-model="selectedFood.dialog">
        <v-sheet>
          <v-container>
            <v-form>
              <v-text-field v-model="selectedFood.name" label="Name" variant="outlined" />
              <v-row>
                <v-col>
                  <v-text-field v-model="selectedFood.brand" label="Marke" variant="outlined" />
                </v-col>
                <v-col cols="4">
                  <v-checkbox v-model="selectedFood.active" label="aktiv"></v-checkbox>
                </v-col>
              </v-row>
              <v-text-field v-model="selectedFood.num_packets" label="Anzahl Packungen" variant="outlined"
              type="number" />
              <v-text-field v-model="selectedFood.packet_size" label="Packungen Größe" variant="outlined" type="number" />
              <v-select v-model="selectedFood.unit" :items=foodOptions.data.units item-title="name"
              item-value="value" label="Einheit" variant="outlined" />
              <v-select v-model="selectedFood.category" :items=foodOptions.data.categories item-title="name"
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

<script setup lang="js">
import { useTheme } from 'vuetify'
const theme = useTheme()
const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}

const baseURL = useRuntimeConfig().public.baseURL

const pets = usePetsStore()
const foods = useFoodsStore()
const helper = useHelperStore()
const foodOptions = useFoodOptionsStore()

const ws = useWebsocketStore()

const selectedPet = ref({dialog: false})
const editPet = (pet) => {
  selectedPet.value = structuredClone({
    ...pet,
    datePicker: new Date(pet?.birthday_on ?? new Date()),
    dialog: true,
  })
}

const savePet = async () => {
  // format is YYYY-MM-DD
  selectedPet.value.birthday_on = selectedPet.value.datePicker.toISOString().substring(0, 10)
  await postPet(selectedPet.value)
  selectedPet.value = false
}

const selectedFood = ref({dialog: false})
const editFood = (pet) => {
  selectedFood.value = structuredClone({
    ...pet,
    dialog: true,
    active: pet?.active ?? true,
  })
}
const saveFood = async () => {
  let food = selectedFood.value
  food.amount = food.num_packets * food.packet_size
  await postFood(selectedFood.value)
  selectedFood.value = false
}
</script>