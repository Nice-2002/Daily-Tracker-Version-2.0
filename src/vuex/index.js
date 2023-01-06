import Vuex from 'vuex'
import Vue from 'vue'
import router from '../router/router.js'
Vue.use(Vuex)


const store = new Vuex.Store({
  // ...
  state: {
    loggedIn: localStorage.getItem('token') ? true : false,
  },
  getters: {
    token(state) {
      if (state.loggedIn === true) {
        return localStorage.getItem('token')
      } else {
        return null
      }
    },
  },
  mutations: {
    login(state) {
      state.loggedIn = true
    },
    logout(state) {
      state.loggedIn = false
    },
  },
  // FetchFunction({p=s1, p2=s1, p3=s3})

  actions: {
    async loginUser({ commit }, user) {
      const res = fetch(`http://127.0.0.1:5000/login?include_auth_token`, {
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" },
        body: JSON.stringify(user)
      })
      res
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            const authToken = data.response.user.authentication_token
            console.log(authToken)
            localStorage.setItem('token', authToken)
            commit('login')
            router.push('/')
        })
        .catch((err) => {
          console.log(err)
        })
        location.reload(true);
    },
    logoutUser({ commit }) {
      
      const res = fetch(`http://127.0.0.1:5000/logout`, {
        method: "GET",
        headers: { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" },
      })
      res.then((response) => response.json())
      .then(data => console.log(data))
      .catch((err) => console.log(err))
      localStorage.removeItem('token')
      commit('logout')
      alert("Logged out successfully.")
      router.push('/login')
    },
    delete_account({commit}) {
      alert("Are you sure to delete the account?")
      fetch(`http://127.0.0.1:5000/delete_account`,{
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication-Token": store.getters.token
        }
      })
      .then((response) => response.json())
      .then((data) => {
          console.log(data)
      })
      .catch((err) => {
        console.log(err)
      })
      localStorage.removeItem('token')
      commit('logout')
      router.push('/login')
    }
  },
})

export default store