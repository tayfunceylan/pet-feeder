import axios from "axios";

// =================================[ Helper Functions ]=====================================================
const tokenHeader = (store) => {return {
    headers: {
        Authorization: `Bearer ${store.accessToken}`
    }
}}
export const basicFetch = async (authStore, url, name="default") => {
    return axios.get(url, tokenHeader(authStore)).catch((error) => {
                console.log(name, error.response)
                if(error.response.status === 401) navigateTo('/login')
    })
}

export const basicPost = async (authStore, url, data, name="default") => {
    return axios.post(url, data,tokenHeader(authStore)).catch((error) => {
        console.log(name, error.response)
        if(error.response.status === 401) navigateTo('/login')
    })
}

export const basicPut = async (authStore, url, data, name="default") => {
    return axios.put(url, data,tokenHeader(authStore)).catch((error) => {
        console.log(name, error.response)
        if(error.response.status === 401) navigateTo('/login')
    })
}

export const basicDelete = async (authStore, url, name="default") => {
    return axios.delete(url, tokenHeader(authStore)).catch((error) => {
        console.log(name, error.response)
        if(error.response.status === 401) navigateTo('/login')
    })
}
// ======================================[ URL's ]==========================================================
const baseURL = "http://127.0.0.1:8000"
const mealURL = "Meal"
const foodURL = "Food"
const petURL = "Pet"
export const authURL = `${baseURL}/api-token/`

// ======================================[ Meal Requests ]=================================================================
export const fetchMealListURL = async (authStore, date) => basicFetch(authStore, `${baseURL}/${mealURL}/get_day/?date=${date}`, "date")
export const fetchMealID = async (authStore, MID) => basicFetch(authStore, `${baseURL}/${mealURL}/${MID}`, "meal (id)")
export const postMeal = async (authStore, data) => basicPost(authStore, `${baseURL}/${mealURL}/`, data, "Meal Post")
export const putMeal = async (authStore, MID, data) => basicPut(authStore, `${baseURL}/${mealURL}/${MID}/`, data, "Meal Put")
export const deleteMealID = async (authStore, MID) => basicDelete(authStore, `${baseURL}/${mealURL}/${MID}`, "meal Delete (id)")


// =====================================[ Food Requests ]=============================================================================
export const fetchFoodList = async (authStore) => basicFetch(authStore, `${baseURL}/${foodURL}/`, "food List")
export const fetchFoodID = async (authStore, FID) => basicFetch(authStore, `${baseURL}/${foodURL}/${FID}`, "food (id)")


// =====================================[ Pet Requests ]==============================================================
export const fetchPetsURL = async (authStore) => basicFetch(authStore, `${baseURL}/${petURL}/`, "pets")
