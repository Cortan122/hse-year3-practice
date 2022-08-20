<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <NavigationBar :routes="routes" :authLevel="authLevel" />
    <div class="flex flex-row flex-grow max-h-page">
      <ProjectTree :class="this.$route.name?.trim() == 'My Projects' ? '' : 'hidden'" v-if="authLevel" />
      <main class="flex-grow overflow-y-auto">
        <router-view/>
      </main>
    </div>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar'
import ProjectTree from '@/components/ProjectTree'
import routes from '@/routes.js'

export default {
  name: 'App',
  components: {
    NavigationBar,
    ProjectTree,
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
      "true": 2,
    }[user.is_admin];

    return {routes, user, authLevel};
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
