<template>
    <div class="container">
        <h1>Add a tracker</h1>
        <form class="create_tracker_form" @submit.prevent="submit">
            <div class="form-group">
                <label for="TrackerName">Tracker Name:</label>
                <input type="text" v-model="tracker.tracker_name" name="tracker_name" class="form-control" placeholder="e.g. Run" required />
                <small class="form-text text-muted">Enter the tracker name.</small>
            </div>
            <br><br>
            <div class="form-group">
                <label for="TrackerQuestion">Tracker Question:</label>
                <input type="text" v-model="tracker.tracker_question" name="tracker_question" class="form-control" placeholder="e.g. How many miles did you ran today?" required />
                <small class="form-text text-muted">Enter the tracker question.</small>
            </div>
            <br><br>
            <div class="form-group">
                <label for="TrackerType">Tracker Type:</label>
                <br><br>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" v-model="tracker.tracker_type" type="radio" name="track_type" id="inlineRadio1" value="number">
                    <label class="form-check-label" for="interger">Numeric</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" v-model="tracker.tracker_type" type="radio" name="track_type" id="inlineRadio1" value="boolean">
                    <label class="form-check-label" for="boolean">Boolean</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" v-model="tracker.tracker_type" type="radio" name="track_type" id="inlineRadio1" value="text">
                    <label class="form-check-label" for="text">Text</label>
                </div>
            </div>
                    
            <br><br>
            <div>
                <button type="submit_form" class="btn btn-primary">Submit</button>
                <button @click="home()" class="btn btn-secondary">Go Home</button>
            </div>
        </form>
        <h3 v-show="exist">Tracker already exist. Please use a different tracker name.</h3>
    </div>
</template>

<script>
    import "babel-polyfill";
    export default {
        name: "create_tracker",
        data() {
            return {
                tracker: {
                    "tracker_name": "",
                    "tracker_type": "",
                    "tracker_question": "",
                },
                exist: false,
            }
        },
        methods: {
            async submit () {
                await fetch(`http://127.0.0.1:5000/create_tracker`, {
                    method: "POST",
                    headers: { 
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json",
                        "Authentication-Token": this.$store.getters.token
                    },
                    body: JSON.stringify(this.tracker)
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(err => console.log(err))

                this.$router.push(`/`)
            },
            home() {
                this.$router.push(`/`);
            },
        }
    }
</script>