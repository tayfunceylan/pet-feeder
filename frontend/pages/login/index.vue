<template>
    <v-sheet width="300" class="mx-auto">
        <v-form @submit.prevent>
            <v-text-field v-model="username" :rules="rules" label="Username"></v-text-field>
            <v-text-field v-model="password" :rules="rules" label="Password"></v-text-field>
            <v-btn @click="login()" type="submit" block class="mt-2">Login</v-btn>
        </v-form>
        {{csrfmiddlewaretoken}}
    </v-sheet>
</template>

<script setup lang="ts">


const rules = [
    (v: string) => !!v || 'Eingabe erforderlich',
]

const username = ref('')
const password = ref('')
const csrfmiddlewaretoken = ref('csrfmiddlewaretoken')

// get csrf token
const { data, pending, error, refresh } = await useFetch('http://localhost:8000/login/', 
        {
            // url encoded form data
            method: 'GET',
            credentials: 'include',
            onRequestError({ request, options, error }) {
                // Handle the request errors
                throw new Error('Request error')
            },
            onResponse({ request, response, options }) {
                // if response is != 200, then throw error
                if (response.status != 200) {
                    throw new Error('Response status is not 200: bad response from server')
                }
                // get csrfmiddlewaretoken from response
                console.log("hallo")

                // csrftoken.value =  document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            onResponseError({ request, response, options }) {  
                // Handle the response errors
                throw new Error('Response error')
            }
        }
    )

const login = async () => {
    const { data, pending, error, refresh } = await useFetch('http://localhost:8000/login/', 
        {
            // url encoded form data
            method: 'POST',
            credentials: 'include',
            body: new URLSearchParams({
                username: username.value,
                password: password.value,
            }),
            onRequest({ request, options }) {
            },
            onRequestError({ request, options, error }) {
                // Handle the request errors
            },
            onResponse({ request, response, options }) {
            },
            onResponseError({ request, response, options }) {
                // Handle the response errors
            }
        }
    )
}
</script>