<template>
    <div class="container">
        <br><br>
        <strong> Welcome <i> {{ user.user_name }}</i> </strong>
        <br><br>
        <button @click="logoutUser" class="btn btn-danger">Logout</button>
        <button @click="delete_account" class="btn btn-danger">Delete account</button>
    </div>
</template>

<script>
    import { mapActions } from "vuex";
    export default {
        name: "side-bar",
        data() {
            return {
                user: "",
            }
        },
        methods: {
            ...mapActions(['logoutUser', "delete_account"]),
        },
        mounted() {
            fetch(`http://127.0.0.1:5000/get_user`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.$store.getters.token
                }
            })
            .then((response) => response.json())
            .then((data) => {
                this.user = data
                console.log(this.user)
            })
            .catch((err) => console.log(err))
        }
    }
</script>