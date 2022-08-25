<template>
  <div class="w-full md:w-1/2 lg:w-[27rem] 2xl:w-1/3 px-3 mb-6">
    <div class="p-5 bg-white shadow-md rounded-xl">
      <div class="flex items-center mb-2">
        <img v-if="task.completed" class="h-16 w-16 object-contain" src="@/assets/undraw_handcrafts_delete_green.svg">
        <img v-else class="h-16 w-16 object-contain" src="@/assets/undraw_handcrafts_pinned_file.svg">
        <div class="pl-4">
          <p class="text-xl">{{task.name}}</p>
          <p v-if="!isLong && task.description"
            class="text-red-600 italic text-ellipsis overflow-hidden whitespace-nowrap max-w-xs">
            {{task.description}}
          </p>
          <p class="text-sm">
            <i class="codicon codicon-dashboard translate-y-0.5" aria-hidden="true"></i>
            {{ duration(task.workload) }}
          </p>
        </div>
      </div>

      <p v-if="isLong" class="italic">{{task.description}}</p>

      <TagsEditor :tags="tags" @add-tag="addTag" @delete-tag="deleteTag" @replace-tag="replaceTag" />

      <PerfectScrollbar class="max-h-32 border mb-2" v-if="history.length">
        <LogCard :workload="task.workload" :log="log" v-for="log in history" :key="log.id"/>
      </PerfectScrollbar>

      <button :class="buttonClass" @click="click" :disabled="!buttonEnabled">{{buttonText}}</button>
    </div>
  </div>

  <CreationForm v-if="tasklog_id" :url="`/api/finalize/${tasklog_id}`" :fields="fields" ref="form"
    title="Завершение работы" button-text="Commit"/>
</template>

<script>
  import humanizeDuration from 'humanize-duration'
  import TagsEditor from '@/components/TagsEditor'
  import LogCard from '@/components/LogCard'
  import PerfectScrollbar from '@/components/PerfectScrollbar'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'TaskCard',
    components: {
      TagsEditor,
      PerfectScrollbar,
      LogCard,
      CreationForm,
    },
    props: {
      task: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        occupied_by: this.task.occupied_by,
        history: this.task.history,
        tags: this.task.tags,
        tasklog_id: null,
        fields: [
          {name: 'Commit URL', sort: 'github_url', type: String, inputtype: 'url', placeholder: 'https://github.com/'},
          {name: 'Description', sort: 'description', type: 'textarea'},
          {name: 'Task completed?', sort: 'is_completed', type: Boolean},
        ],
      };
    },
    methods: {
      duration(milliseconds) {
        return humanizeDuration(milliseconds, { round: true, largest: 1, units: ['d', 'h', 'm'] });
      },
      start() {
        this.$root.user.has_current_task = true;
        this.occupied_by = this.$root.user;
        this.history.push({duration: 0, user: this.$root.user});
        this.$http.post(`/api/task/${this.task.id}/start`);
      },
      stop() {
        var ctx = this;
        ctx.occupied_by = null;
        ctx.$root.user.has_current_task = false;
        ctx.history[ctx.history.length-1].finished = true;
        ctx.$http.post(`/api/stop`).then(e => {
          ctx.tasklog_id = parseInt(e.data.id);
          setTimeout(() => ctx.$refs.form.show(), 100);
        });
      },
      click() {
        this.occupied_by ? this.stop() : this.start();
      },
      addTag(tag) {
        this.$http.post(`/api/task/${this.task.id}/tags/${tag}`).then(this.updateTags);
      },
      deleteTag(tag) {
        this.$http.delete(`/api/task/${this.task.id}/tags/${tag}`).then(this.updateTags);
      },
      replaceTag(tag, newtag) {
        this.$http.patch(`/api/task/${this.task.id}/tags/${tag}/to/${newtag}`).then(this.updateTags);
      },
      updateTags(tags) {
        this.tags = tags.data;
      },
    },
    computed: {
      isLong() {
        return this.task.description?.length > 32;
      },
      buttonText() {
        if(this.task.completed)return 'задача выполнена';

        var occupied = this.occupied_by;
        if(occupied){
          if(this.$root.user.id == occupied.id){
            return 'стоп';
          }
          return `работает ${occupied.first_name}`;
        }
        if(this.$root.user.has_current_task){
          return 'идёт таймер';
        }
        return 'старт';
      },
      buttonEnabled() {
        return !this.buttonText.includes(' ');
      },
      buttonClass() {
        const common = "focus:outline-none bg-gradient-to-br font-semibold rounded-lg py-2 px-5 text-white uppercase block w-2/3 mx-auto";
        const activeColor = "from-red-600 to-red-700 hover:from-red-500 hover:to-red-700";
        const inactiveColor = "from-red-300 to-red-200";
        return common + ' ' + (this.buttonEnabled ? activeColor : inactiveColor);
      },
    },
  }
</script>
