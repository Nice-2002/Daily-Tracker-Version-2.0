<template>
    <div class="container">
        <h1 class="mb-3">Update log into {{ tracker.tracker_name }}</h1>
        <form id="log-into-tracker-form" @submit.prevent="submit">
            <div class="form-group">
                <label for="TrackerQuestion">Tracker Question: {{ tracker.tracker_question }}</label>
                <br><br>
                <p><strong>Current tracker value is {{ log.log_value }}.</strong></p>
                <div class="form-group" v-if="tracker.tracker_type == 'boolean'">
                    <br><br>
                    <div class="form-check form-check-inline" >
                        <input class="form-check-input" v-model="log_value.value" type="radio" name="input_val" id="inlineRadio1" value="True">
                        <label class="form-check-label" for="interger">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" v-model="log_value.value" type="radio" name="input_val" id="inlineRadio1" value="False">
                        <label class="form-check-label" for="boolean">No</label>
                    </div>
                    <small class="form-text text-muted">Choose one option.</small>
                </div>
                
                <div v-if="tracker.tracker_type != 'boolean'">
                    <input name="input_val" v-if="tracker.tracker_type != 'boolean'" v-model="log_value.value" class="form-control" required />
                    <small class="form-text text-muted" v-if="tracker.tracker_type != 'boolean'">Enter the tracker value.</small>
                </div>
                <br><br>
                <button class="btn btn-success" @click="submit">Submit</button>
                <button @click="home()" class="btn btn-secondary">Go Home</button>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: "update_log",
        data() {
            return {
                tracker: "",
                log: "",
                log_value: {
                    "value": ""
                }

            }
        },
        async mounted() {
            await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}/log/${this.$route.params.log_id}`, {
                method: "GET",
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.$store.getters.token
                }
            })
            .then(response => response.json())
            .then(data => {
                this.log = data
                console.log(this.log)
            })
            .catch(err => console.log(err))

            await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}`, {
                headers: {
                    "Authentication-Token": this.$store.getters.token
                }
            })
            .then(response => response.json())
            .then(data => {
                this.tracker = data
                console.log(this.tracker)
            })
            .catch(err => console.log(err))
        },
        methods: {
            async submit() {
                console.log(this.log_value)
                await fetch(`http://127.0.0.1:5000/tracker/${this.$route.params.tracker_id}/log/${this.$route.params.log_id}`, {
                    method: "PUT",
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json",
                        "Authentication-Token": this.$store.getters.token
                    },
                    body: JSON.stringify(this.log_value)
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(err => console.log(err))

                this.$router.push(`/tracker_details/${this.$route.params.tracker_id}`)
            },
            home() {
                this.$router.push(`/`);
            },
        }
    }
</script>