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
            <v-form>
                <v-text-field max-wid="10" v-model="username" label="Username" variant="outlined"/>
                <v-text-field @keyup.enter="login(username, password)" v-model="password" label="Password" type="password" variant="outlined"/>
                <v-btn color="grey-darken-2" block @click="login(username, password)" variant="outlined">Login</v-btn>
            </v-form>
        </v-responsive>
    </v-sheet>
</template>

<script setup lang="ts">
const username = ref('')
const password = ref('')
await checkIfLoggedIn()
</script>