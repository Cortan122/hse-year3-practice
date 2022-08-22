<template v-slot="navigation">
  <nav class="bg-white border-b border-gray-100 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/">
              <img class="block h-9 w-auto" src="@/assets/logo.png">
            </router-link>
          </div>

          <!-- Navigation Links -->
          <div v-for="item in links" :key="item.index" class="hidden space-x-8 sm:-my-px sm:ml-10 sm:flex">
            <NavLink :href="item.path" :active="item.name == this.$route.name?.trim()">
              {{ item.name }}
            </NavLink>
          </div>
        </div>

        <div class="hidden sm:flex sm:items-center sm:ml-6">
          <button class="ml-3 relative text-black" tabindex="-1">
            <router-link to="/login" v-if="authLevel == 0">Log In</router-link>
            <a href="/api/logout" v-else>Log Out</a>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import NavLink from '@/components/NavLink'

export default {
  name: 'NavigationBar',
  props: {
    routes: Array,
    authLevel: { type: Number, default: 0 },
  },
  components: {
    NavLink
  },
  computed: {
    links() {
      return this.routes.filter(item => item.name && item.authLevel <= this.authLevel);
    }
  }
}
</script>
