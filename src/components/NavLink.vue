<template>
  <router-link :to="href" :class="classes">
    <slot></slot>
  </router-link>
</template>

<script>
  export default {
    name: 'NavLink',
    props: {
      href: String,
      active: Boolean,
    },

    computed: {
      classes() {
        return 'inline-flex items-center px-1 pt-1 border-b-2 focus:outline-none transition ' + (this.active ?
          'border-red-600 text-gray-900 focus:border-red-700' :
          'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 focus:text-gray-700 focus:border-gray-300');
      }
    }
  }
</script>
