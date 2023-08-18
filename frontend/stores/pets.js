import {fetchPetsURL} from "~/helpers/api";


export const usePetsStore = defineStore('pets',() => {
    const authStore = useAuthStore()
    const pets = ref(null)

    async function fetchPets(){
        const petResponse = fetchPetsURL(authStore)
        pets.value = (await petResponse)?.data
    }
    return {pets, fetchPets}
})


