<template>
    <div class="container">
        <h1 class="display-4">Export Options</h1>
        <div class="row">
            <div class="col-md-8" v-if="trackers.length > 0">  
                <h2>There is {{trackers.length}} tracker in your profile.</h2>
                <br>
                <button @click="export_logs('logs')" class="btn btn-primary" download="log_report.csv">Export all data</button>
                <br><br>
                <button @click="home()" class="btn btn-secondary">Go Home</button>
            </div>
            <div class="col-md-8" v-else>
                <h2>
                    There are no trackers in your profile. 
                    Please  create a tracker from below link.
                </h2>
                <br>
                <button @click="create_tracker()" class="btn btn-primary">+Add Tracker</button>
                <br><br>
                <button @click="home()" class="btn btn-secondary">Go Home</button>
            </div>
            <div class ="col-md-4">
                <sidebar></sidebar>
            </div>
        </div>
    </div>
</template>

<script>
    import sidebar from './sidebar.vue'
    import Sidebar from './sidebar.vue'
    export default {
        name: "export-options",
        data() {
            return {
                trackers: [],
                user: ""
            }
        },
        methods: {
            async export_logs(value) {
                var saveAs = require("file-saver");
                const status = fetch(`http://127.0.0.1:5000/export_options`, {
                    method: "POST",
                    headers: {
                        "Authentication-Token": this.$store.getters.token,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    responseType: "blob",
                    body: JSON.stringify({ "value": value })
                });
                status.then(response => response.blob())
                    .then(blob => saveAs(blob, this.user.user_name + ".csv"));
            },
            create_tracker() {
                this.$router.push(`create_tracker`);
            },
            home() {
                this.$router.push(`/`);
            },
        },
        async mounted() {
            await fetch("http://127.0.0.1:5000/", {
                method: "GET",
                headers: {
                    "Authentication-Token": this.$store.getters.token
                }
            })
            .then(response => response.json().catch(err => console.log("unexpected error")))
            .then(data => {
            this.trackers = data;
            console.log(this.trackers);
            })
            .catch(err => console.log(err.message));

            await fetch(`http://127.0.0.1:5000/get_user`, {
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
        },
        comments: {
            sidebar
        },
        components: { Sidebar }
    }
</script>