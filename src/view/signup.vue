<template>
    <div class="container">
        <h1>Please sign up</h1> 
        <form @submit.prevent="submit">
            <label for="username">Username: </label>
            <input type="text" placeholder="username.." v-model="signUpData.username"> <br>
            <label for="email">Email: </label>
            <input type="email" placeholder="email.." v-model="signUpData.email"> <br>
            <label for="password">Password: </label>
            <input type="password" placeholder="password.." v-model="signUpData.password"> <br>
            <button @click="SignUp" class="btn btn-outline-success">SignUp</button>
        </form>
        <br>
        <h4>Have and account please log in.</h4>
        <button @click="login" class="btn btn-outline-primary">Login here</button> 
    </div>
</template>

<script>
    export default {
        data() {
            return {
                signUpData: {
                    email: null,
                    password: null,
                    username: null,
                }
            }
        },
        methods: {
            SignUp() {
                const res = fetch(`http://127.0.0.1:5000/users`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(this.signUpData)
                })
                res.then((response) => {
                    console.log(response)
                })
                .catch((err) => {
                    console.log(err)
                })
                this.login()
            },
            login() {
                this.$router.push('/login')
            }
        }
    }
</script>