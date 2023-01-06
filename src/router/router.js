import Vue from 'vue'
import VueRouter from 'vue-router'


import update_tracker from '../components/update_tracker.vue'
import index from '../components/index.vue'
import tracker_details from '../components/tracker_details.vue'
import log_into_tracker from '../components/log_into_tracker.vue'
import create_tracker from '../components/create_tracker'
import update_log from '../components/update_log.vue'
import export_options from '../components/export_options.vue'
import login from '../view/login.vue'
import signup from '../view/signup.vue'

Vue.use(VueRouter)

const routes = [
    { path: '/update_tracker/:tracker_id', name: "update_tracker", component: update_tracker },
    { path: '/create_tracker', name: "create_tracker", component: create_tracker },
    { path: '/tracker/:tracker_id/logs', name: "log_into_tracker", component: log_into_tracker},
    { path: '/tracker_details/:tracker_id', name: "tracker_details", component: tracker_details },
    { path: '/tracker/:tracker_id/log/:log_id', name: "update_log", component: update_log },
    { path: '/export_options', name: "exports", component: export_options },
    { path: '/login', name: 'login', component: login},
    { path: '/signup', name: 'signup', component: signup },
    { path: '/', component: index}
  ];
  
  const router = new VueRouter({
    routes
  })

export default router