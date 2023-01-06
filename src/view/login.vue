<template>
    <div class="container">
        <form action="">
            <h2>Please "Sign in"</h2>
            <label for="email">Email: </label>
            <input type="email" placeholder="email" v-model="userInfo.email">
            <br>
            <label for="password">Password: </label>
            <input type="password" placeholder="password" v-model="userInfo.password">
            <br>
            <button @click="loginUser(userInfo)" class="btn btn-outline-success"> Login </button>
        </form>
        <br>
        <h4>Don't have an account please sign up.</h4>
        <button @click="register" class="btn btn-outline-primary">Register here</button>
    </div>
</template>

<script>
    //import { loginUser, logoutUser } from "../vuex/index.js";
    import { mapActions } from "vuex";
  
    export default {
        //vuex: {
            //actions: { loginUser, logoutUser }
        //},
        data() {
            return {
                userInfo: {
                    email: null,
                    password: null
                }
            }
        },
        methods: {
            ...mapActions(['loginUser']),
            register() {
                this.$router.push('/signup')
            }
        }
    }
</script>