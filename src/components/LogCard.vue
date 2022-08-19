<template>
  <div class="w-full flex items-center">
    <div class="p-2">
      <CircleProgress fill-color="#41b883" :is-gradient="!log.finished"
        :percent="percent" :size="60" :border-width="7" :border-bg-width="7" :show-percent="true"
        :gradient="{angle: percent, startColor: '#bef264', stopColor: '#41b883'}"
      />
    </div>
    <div class="my-1">
      <a :href="'mailto:' + log.user.email" class="text-lg font-semibold" target="_blank">
        {{log.user.first_name}} {{log.user.last_name}}
      </a>
      <span class="text-neutral-400">&nbsp;•&nbsp;</span>
      <span :title="tooltip">{{duration}}</span>

      <div class="line-clamp-2">
        <span v-if="!isToday" class="italic text-sm">
          {{date.toLocaleDateString("ru-RU")}}
          <span class="text-neutral-400" v-if="log.description">&nbsp;•&nbsp;</span>
        </span>
        {{log.description}}
      </div>
    </div>
  </div>
</template>

<script>
  import "vue3-circle-progress/dist/circle-progress.css"
  import CircleProgress from "vue3-circle-progress"
  import moment from 'moment'

  export default {
    name: 'LogCard',
    props: {
      log: {type: Object, required: true},
      workload: {type: Number, default: 3600_000}, // 1 hour
    },
    components: {
      CircleProgress,
    },
    data() {
      return {
        interval: null,
      };
    },
    computed: {
      percent() {
        return this.log.duration / this.workload * 100;
      },
      duration() {
        return moment.duration(this.log.duration).humanize();
      },
      tooltip() {
        return new Date(this.log.duration).toISOString().substr(11, 8);
      },
      date() {
        return new Date(this.log.start_date);
      },
      isToday() {
        if(!this.log.start_date)return true;

        var date1 = this.date;
        var date2 = new Date();
        return Date.now() - date1.getTime() < 3600_000 * 12 || (
          date1.getFullYear() == date2.getFullYear() &&
          date1.getMonth() == date2.getMonth() &&
          date1.getDate() == date2.getDate()
        );
      },
    },
    created() {
      if(!this.log.finished){
        var log = this.log;
        var last = Date.now();
        var interval = setInterval(() => {
          try {
            if(log.finished)clearInterval(interval);
            log.duration += Date.now() - last;
            last = Date.now();
          } catch(e) {
            clearInterval(interval);
          }
        }, 1000);
        this.interval = interval;
      }
    },
    beforeUnmount() {
      clearInterval(this.interval);
    },
  }
</script>
