import axios from "axios";
import {useLocalStorage} from "@vueuse/core";

export const useAuthStore = defineStore( 'auth', {
    state: () => {
        return {
            refreshToken: useLocalStorage('refreshToken', ""),
            accessToken: useLocalStorage('accessToken', ""),
            incorrectAuth: false,
            loggedIn: false
        }
    },
    actions: {
        async login(credentials){
            axios.post('http://127.0.0.1:8000/api-token/', {
                username: credentials.username,
                password: credentials.password,
            }).then((response) => {
                this.refreshToken = response.data.refresh
                this.accessToken = response.data.access
                this.loggedIn = true

                navigateTo('/meal-page')
                return response
            }).catch(err => {
                console.log(err)
                this.incorrectAuth = true
            })
        }
    }
})

