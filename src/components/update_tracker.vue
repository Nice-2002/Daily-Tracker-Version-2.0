<template>
    <div id="update_tracker" class="container">
        <h1>Update Tracker "{{tracker['tracker_name']}}"</h1>
        <form class="update_tracker_form" @submit.prevent="submit">
            <div class="form-group">
                <p><strong>Current tracker Name: {{tracker['tracker_name']}}</strong> </p>
                <label for="TrackerName">Tracker Name:</label>
                <input type="text" v-model="updated_tracker.tracker_name" name="tracker_name" class="form-control" placeholder="e.g. Run" required />
                <small class="form-text text-muted">Enter the tracker name.</small>
            </div>
            <br><br>
            <div class="form-group">
                <p><strong>Current tracker Question: {{tracker['tracker_question']}}</strong></p>
                <label for="TrackerQuestion">Tracker Question:</label>
                <input type="text" v-model="updated_tracker.tracker_question" name="tracker_question" class="form-control" placeholder="e.g. How many miles did you ran today?" required />
                <small class="form-text text-muted">Enter the tracker question.</small>
            </div>
            <br><br>
            <div class="form-group">
                <label for="TrackerType">Tracker Type:</label>
                <br><br>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" v-model="updated_tracker.tracker_type" type="radio" name="track_type" id="inlineRadio1" value="number">
                    <label class="form-check-label" for="interger">Numeric</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" v-model="updated_tracker.tracker_type" name="track_type" id="inlineRadio1" value="boolean">
                    <label class="form-check-label" for="boolean">Boolean</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" v-model="updated_tracker.tracker_type" name="track_type" id="inlineRadio1" value="text">
                    <label class="form-check-label" for="text">Text</label>
                </div>
            </div>

            <br><br>
                <button type="submit_form" class="btn btn-primary">Submit</button>
                <button @click="home()" class="btn btn-secondary">Go Home</button>
                

        </form>
    </div>
</template>

<script>
    import "babel-polyfill";
    export default {
        name: "update_tracker",
        data() {
            return {
                tracker: {
                    "tracker_id": -1,
                    "tracker_name": "",
                    "tracker_type": "",
                    "tracker_question": "",
                    "user_id": -1,
                },
                updated_tracker: {
                    "tracker_name": "",
                    "tracker_question": "",
                    "tracker_type": ""
                }
            }
        },
        methods: {
            submit() {
                const status = fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}`, {
                    method: "PUT",
                    headers: {
                        "Access-Control-Allow-Origin": '*',
                        'Content-Type': "application/json",
                        "Authentication-Token": this.$store.getters.token
                    },
                    body: JSON.stringify(this.updated_tracker)
                })
                status.then(
                    () => {
                            console.log("Tracker updated Successfully")
                            this.$router.push(`/`)
                        },
                    () => console.log("Tracker update failed")
                )
                
            },
            home() {
                this.$router.push(`/`);
            },
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
        }
    }
</script>