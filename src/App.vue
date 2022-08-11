<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <NavigationBar :routes="routes" />
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
    return {routes};
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
