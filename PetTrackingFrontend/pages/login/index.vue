<template>
    <div class="login">
        <v-sheet width="300" class="mx-auto">
            <v-form @submit.prevent>
            <v-text-field
                v-model="username"
                :rules="rules"
                label="Username"
            ></v-text-field>
            <v-text-field
                v-model="password"
                :rules="rules"
                label="Password"
            ></v-text-field>
            <v-btn type="submit" block class="mt-2">Login</v-btn>
            </v-form>
        </v-sheet>
    </div>
</template>

<script>
export default {
    data: () => ({
    username: '',
    password: '',
    rules: [
        value => {
            if (value) return true
            return 'this field is required'
        },
    ],
    }),
}
</script>

<style scoped>
.login {
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
<!-- name: "App",
data() {
  return {
    username: "",
    password: "",
    confirmPassword: "",
    isRegister : false,
    errorMessage: "",
    stateObj: {
       register :{
          name: 'Register',
          message: 'Aleady have an Acoount? login.'
       },
       login : {
          name: 'Login',
          message: 'Register'
       }
    }
  };
},
methods: {
  login() {
    const { username } = this;
    console.log(username + "logged in")
  },
},
    computed: {
     toggleMessage : function() { 
        return this.isRegister ? this.stateObj.register.message : this.stateObj.login.message }
  } -->