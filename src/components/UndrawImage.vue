<template>
  <img class="w-5/6 lg:h-[50vh] m-auto mt-20" :src="require(`@/assets/undraw_${icon}.svg`)">
  <div v-if="text" class="text-center font-semibold mt-10 text-3xl">{{text}}</div>
</template>

<script>
  export default {
    name: 'UndrawImage',
    props: {
      icon: {type: String, required: true},
      text: String,
    },
  }
</script>
