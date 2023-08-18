import axios from "axios";
import {useLocalStorage} from "@vueuse/core";
import {authURL} from "~/helpers/api";

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
            axios.post(authURL, {
                username: credentials.username,
                password: credentials.password,
            }).then((response) => {
                this.refreshToken = response.data.refresh
                this.accessToken = response.data.access
                this.loggedIn = true
                return response
            }).catch(err => {
                console.log(err)
                this.incorrectAuth = true
            })
        }
    }
})

