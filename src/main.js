import Vue from 'vue'
import router from './router/router.js'
import store from './vuex/index.js'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
//import VueChartkick from 'vue-chartkick'
//import VueChartkick from 'vue-chartkick'
//import Chart from 'chart.js'
////import "./plugins/echarts";

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
//Vue.use(Chart)
//Vue.use(VueChartkick.user(Chart))
//Vue.use(Vuex)


new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})