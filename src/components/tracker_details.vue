<template>
    <div class="container">
        <h1 class="mb-3">Tracker details related to {{tracker.tracker_name}}</h1>
        <br><br>
        <h4><strong>Tracker Question: <i>{{tracker.tracker_question}}</i></strong></h4>
        <table id = "all-logs" class="table" v-if="logs.length > 0">
            
            <thead class="thead-dark">
                <tr>
                    <th scope="col">SNo</th>
                    <th scope="col">Logging Date</th>
                    <th scope="col">Logging time</th> 
                    <th scope="col">Tracker Value</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(log, index) in logs">
                    <td scope="row">{{index + 1}}</td>
                    <td>{{to_date(log.time_stamp)}}</td>
                    <td>{{to_time(log.time_stamp)}}</td>
                    <td>{{log.log_value}}</td>
                    <td>
                        <button @click="update_log(tracker.tracker_id, log.log_id)" class="btn btn-primary">Update</button>
                        <button @click="delete_log(tracker.tracker_id, log.log_id)" class="btn btn-danger">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <h3 v-else>There are no log information related to this tracker.<br>Add values now!</h3>
        <br>
        <button @click="log()" class="btn btn-primary">Log</button>
        <button @click="home()" class="btn btn-secondary">Go Home</button>
        <br><br>
        <div v-if="logs.length > 0">
            <button @click="export_logs('logs', tracker.tracker_id)" class="btn btn-secondary" download="log_report.csv">Export</button>
        </div>
        
        <br><br>
        <div v-if="tracker.tracker_type == 'number' && logs.length > 0" >
            <img  id="image"/>
        </div>
        
        <!--<div v-if="tracker.tracker_type == 'number'">
            <canvas id="myChart" width="400" height="400"></canvas>
            <line-chart :data="chartdata"></line-chart>
            <graph :tracker_id="tracker.tracker_id"></graph>
            <section class="container">	
	            <div class="columns">
	                <div class="column">
	                    <chartjs-bar :labels="labels" :data="dataset" :bind="true"></chartjs-bar>
	                </div>	    
	            </div>    
	        </section>
        </div>-->
    </div>
</template>

<script>
    export default {
    name: "tracker-details",
    data() {
        return {
            logs: [],
            tracker: "",
            date: "",
            time: "",
            trend_line: ''
        };
    },
    async mounted() {
        var saveAs = require("file-saver");
        await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}/logs`, {
            method: "GET",
            headers: {
                "Authentication-Token": this.$store.getters.token
            }
        })
            .then(response => response.json())
            .then(data => {
            this.logs = data;
            console.log(this.logs);
        })
            .catch(err => console.log(err));

        await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}`, {
            headers: {
                "Authentication-Token": this.$store.getters.token
            }
        })
            .then(response => response.json())
            .then(data => {
            this.tracker = data;
            console.log(this.tracker);
        })
            .catch(err => console.log(err));
        
        await fetch(`http://127.0.0.1:5000/trendline/${this.$route.params.tracker_id}`, {
            headers: {
                "Authentication-Token": this.$store.getters.token,
                'Content-Type': 'image/jpeg'
            },
            responseType: "blob"
        })
        .then(response => response.blob())
        .then(blob => {
            //this.trend_line = blob
            var objectURL = URL.createObjectURL(blob);
            document.querySelector("#image").src = objectURL;
        })
        .catch(err => console.log("Not a number type tracker"))

    },
    methods: {
        update_log(tracker_id, log_id) {
            this.$router.push(`/tracker/${tracker_id}/log/${log_id}`);
        },
        to_time(date) {
            date = new Date(date);
            //date = date.toUTCString()
            return date.getUTCHours() + ":" + date.getUTCMinutes() + ":" + date.getUTCSeconds();
        },
        to_date(date) {
            date = new Date(date);
            return date.getUTCFullYear() + ":" + date.getUTCMonth() + ":" + date.getUTCDate();
        },
        home() {
            this.$router.push(`/`);
        },
        log() {
            this.$router.push(`/tracker/${this.$route.params.tracker_id}/logs`);
        },
        delete_log(tracker_id, log_id) {
            const status = fetch(`http://127.0.0.1:5000/tracker/${tracker_id}/log/${log_id}`, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": this.$store.getters.token
                }
            });
            status.then(() => {
                console.log("Log deleted successfully");
                location.reload(true);
            }, () => console.log("Cannot delete the log value"));
            alert("Log deleted successfully.")
        },
        export_logs(value, tracker_id) {
            var saveAs = require("file-saver");
            const status = fetch(`http://127.0.0.1:5000/export`, {
                method: "POST",
                headers: {
                    "Authentication-Token": this.$store.getters.token,
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    
                },
                responseType: "blob",
                body: JSON.stringify({ "value": value, "tracker_id": tracker_id })
            });
            status.then(response => response.blob())
                .then(blob => saveAs(blob, this.tracker.tracker_name + '.csv'));
        }
    }
}
</script>

<style>
    section {
      width: 700px ;
      margin-left: auto ;
      margin-right: auto ;
      padding-top: 10%;
      }
</style>