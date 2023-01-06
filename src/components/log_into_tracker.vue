<template>
    <div class="container">
        <h1 class="mb-3">Log into {{tracker.tracker_name}} Tracker</h1>
        <form class="log_into_tracker_form" @submit.prevent="submit">
            <div class="form-group" >
                <label for="TrackerQuestion"><h3>Tracker Question: {{tracker.tracker_question}}</h3></label>
                <br><br>
                <div class="form-group" v-if="tracker.tracker_type == 'boolean'">
                    <br><br>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" v-model="log_value" type="radio" name="input_val" id="inlineRadio1" value="True">
                        <label class="form-check-label label label-primary" for="interger">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" v-model="log_value" type="radio" name="input_val" id="inlineRadio1" value="False">
                        <label class="form-check-label label label-primary" for="boolean">No</label>
                    </div>
                    <small class="form-text text-muted">Choose one option.</small>
                </div>
                <div v-else-if="tracker.tracker_type == 'number'" class="form-group">  
                    <input type="number" v-model="log_value" name="input_val" class="form-control" placeholder="" required />
                    <h3 class="form-text text-muted"><h4>Enter the tracker value.</h4></h3>
                </div>
                <div v-else="tracker.tracker_type == 'number'" class="form-group">  
                    <input type="text" v-model="log_value" name="input_val" class="form-control" placeholder="" required />
                    <h3 class="form-text text-muted"><h4>Enter the tracker value.</h4></h3>
                </div>
            </div>
            <br><br>
            <button type="submit_form" class="btn btn-success">Submit</button>
            <button @click="home()" class="btn btn-secondary">Go Home</button>
        </form>
    </div>
</template>

<script>
    import "babel-polyfill";
    export default {
        name: "log_into_tracker",
        data() {
            return {
                tracker: {
                    "tracker_id": -1,
                    "tracker_name": "",
                    "tracker_type": "",
                    "tracker_question": "",
                    "user_id": -1,
                },
                log_value: ""
            }
        },
        async created() {
            await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}`, {
                method: "GET",
                headers: {
                    "Authentication-Token": this.$store.getters.token
                }
            })
            .then(response => response.json())
            .then(data => {
                this.tracker.tracker_id = data["tracker_id"]
                this.tracker.tracker_name = data["tracker_name"]
                this.tracker.tracker_question = data["tracker_question"]
                this.tracker.tracker_type = data["tracker_type"]
                this.tracker.user_id = data["user_id"]
            })
            .catch(err => console.log(err))
        },
        methods: {
            async submit() {
                const status = fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}/logs`, {
                    method: "POST",
                    headers: {
                        'Content-Type': "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Authentication-Token": this.$store.getters.token
                    },
                    body: JSON.stringify(this.log_value)
                })
                status.then(
                    () => {
                            console.log("Logged into Tracker Successfully")
                            this.$router.push(`/tracker_details/${this.$route.params.tracker_id}`)
                        },
                    () => console.log("Logging failed")
                )
                
            },
            home() {
                this.$router.push(`/`);
            },
        }
    }
</script>