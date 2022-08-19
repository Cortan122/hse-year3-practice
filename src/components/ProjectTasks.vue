<template>
  <div class="flex flex-col mb-5">
    <h2 class="text-center text-3xl font-medium pb-1">Задачи проекта «{{name}}»</h2>
    <div class="border-b-2 border-red-700 mx-20 lg:mx-32 2xl:mx-[20%]"></div>
    <div class="text-right w-7/12 italic mr-3 place-self-end">{{proj?.description}}</div>
  </div>

  <div class="flex flex-wrap" v-if="!loading">
    <TaskCard :task="task" v-for="task in proj?.tasks" :key="task.id"/>
  </div>

  <div class="flex h-[calc(100vh-10rem)]" v-if="loading">
    <Spinner class="m-auto" size="200"/>
  </div>
</template>

<script>
  import Spinner from 'vue-spinner/src/MoonLoader'
  import TaskCard from '@/components/TaskCard'

  export default {
    name: 'ProjectTasks',
    components: {
      Spinner,
      TaskCard,
    },
    data() {
      return {
        id: 0,
        loading: true,
        proj: null,
        name: null,
      };
    },
    created() {
      this.init();
    },
    methods: {
      init() {
        var ctx = this;
        var id = parseInt(ctx.$route.params.id);

        ctx.id = id;
        ctx.name = `Проект №${id}`;
        ctx.loading = true;
        ctx.proj = null;

        if(isNaN(id))return;

        ctx.$http.get(`/api/project/${id}`).then(e => {
          ctx.loading = false;
          ctx.proj = e.data;
          ctx.name = e.data.name;
        });
      }
    },
    watch: {
      '$route.params.id': function() {
        this.init();
      }
    },
  }
</script>
