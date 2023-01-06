<template>  
    <div id="index-page" class="container">
        <h1 class="display-4">Tracker List</h1>
        <div class="row">
            <div class="col-md-8">
                <table v-if="trackers.length > 0" class="table">
                    <thead class="thead-dark">
                        <tr>
                            <th>SNo.</th>
                            <th>Tracker Name</th>
                            <th>Tracker Type</th>
                            <th>Tracker question</th>
                            <th>Actons</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(tracker, index) in trackers">
                            <td>{{ index + 1}}</td>
                            <td>{{tracker.tracker_name}} <button @click="tracker_details(tracker.tracker_id)" class="btn btn-primary">Get Details</button></td>
                            <td>{{tracker.tracker_type}}</td>
                            <td>{{tracker.tracker_question}}</td>
                            <td>
                                <button @click="log(tracker.tracker_id)" class="btn btn-primary">Log</button>
                                <button @click="update_tracker_fun(tracker.tracker_id)" class="btn btn-primary">Update</button>
                                <button @click="delete_tracker(tracker.tracker_id)" class="btn btn-danger">Delete</button>
                            </td> 
                        </tr>
                    </tbody>
                </table>
                <h3 v-else>No Trackers Found</h3>
                <button @click="create_tracker()" class="btn btn-primary">+Add Tracker</button>
                <br><br>

                <button v-if="trackers.length > 0" @click="export_logs('Trackers')" class="btn btn-secondary">Export</button>

                <button @click="export_options('Trackers')" class="btn btn-secondary">Other Export Options</button>

            </div>
            <div class ="col-md-4">
                <sidebar></sidebar>
            </div>
        </div>
    
    </div>
</template>

<script>
    import sidebar from './sidebar.vue'
    import { useRouter } from 'vue-router/dist/vue-router'
    import Sidebar from './sidebar.vue'
    export default {
    name: "index-page",
    data() {
        return {
            trackers: []
        };
    },
    methods: {
        tracker_details(tracker_id) {
            this.$router.push(`tracker_details/${tracker_id}`);
        },
        create_tracker() {
            this.$router.push(`create_tracker`);
        },
        update_tracker_fun(tracker_id) {
            this.$router.push(`update_tracker/${tracker_id}`);
        },
        export_options() {
            this.$router.push(`export_options`);
        },
        log(tracker_id) {
            this.$router.push(`tracker/${tracker_id}/logs`);
        },
        delete_tracker(tracker_id) {
            
            const status = fetch(`http://127.0.0.1:5000/tracker/${tracker_id}`, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": this.$store.getters.token
                }
            });
            const response = status.then(response => response.ok).catch(err => console.log(err));
            response.then(() => {
                console.log("Tracker deleted successfully");
                location.reload(true);
            }, () => {
                console.log("Cannot delete tracker");
            });
            alert("Tracker deleted successfully.")
        },
        export_logs(value) {
            var saveAs = require('file-saver');

            const status = fetch(`http://127.0.0.1:5000/export`, {
                method: "POST",
                headers: {
                    "Authentication-Token": this.$store.getters.token,
                    'Content-Type': "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                responseType: "blob",
                body: JSON.stringify({"value": value})
            })
            status.then(response => response.blob())
            .then(blob => saveAs(blob, 'export_trackers.csv'))
        }
    },
    mounted() {
        if (this.$store.state.loggedIn === false) {
            this.$router.push("/login");
        }
        try {
            fetch("http://127.0.0.1:5000/", {
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
        }
        catch (err) {
            console.log(err);
        }
    },
    comments: {
        sidebar
    },
    components: { Sidebar }
}
</script>
