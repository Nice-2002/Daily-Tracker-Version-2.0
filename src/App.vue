<template>
  <div id="app">
    <!--<router-view></router-view>-->
    <br><br>
    <router-view></router-view>
  </div>
</template>


<script>
import index from "./components/index.vue"
export default {
  name: 'app',
  data () {
    return {
    }
  },
  components: {
    "index-page": index
  }
}
</script>

<style>

</style>
