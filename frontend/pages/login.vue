<template>
    <v-sheet class="pa-10">
        <v-responsive class="mx-auto" max-width="344" align="center">
            <v-container class="mb-5">
                <v-row>
                    <v-progress-circular model-value="100" size=30 :width="5" color="primary"/>
                    <div class="text-h5">
                        &nbsp;Pet Feeder
                    </div>
                </v-row>
            </v-container>
            <v-form class="mb-5">
                <v-text-field max-wid="10" v-model="username" label="Username" variant="outlined"/>
                <v-text-field @keyup.enter="login" v-model="password" label="Password" type="password" variant="outlined"/>
                <v-btn color="grey-darken-2" block @click="login" variant="outlined">Login</v-btn>
            </v-form>
            <v-alert :model-value="error" text="Login Fehlgeschlagen, versuch es erneut" type="error"></v-alert>
        </v-responsive>
    </v-sheet>
</template>

<script setup lang="ts">
const username = ref('')
const password = ref('')
const error = ref(false)
await checkIfLoggedIn()
const login = async () => {
    const result = await postLogin(username.value, password.value)
    if (result.status.value == 'error') {
        error.value = true
    }
}
</script>