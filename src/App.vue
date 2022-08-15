<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <NavigationBar :routes="routes" :authLevel="authLevel" />
    <main class="flex-grow">
      <router-view/>
    </main>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'
import routes from '@/routes.js'

export default {
  name: 'App',
  components: {
    NavigationBar,
  },
  data() {
    var userstr = document.getElementById('app').attributes['data-user'].nodeValue;
    var user = {};
    try {
      user = JSON.parse(userstr);
    } catch (e) {
      console.log("Failled to parse user JSON, probably running without flask");
    }
    var authLevel = {
      "undefined": 0,
      "false": 1,
      "ture": 2,
    }[user.is_admin];

    return {routes, user, authLevel};
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
