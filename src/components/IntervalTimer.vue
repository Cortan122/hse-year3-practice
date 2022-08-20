<template>
  <div class="w-full tabular-nums slashed-zero lining-nums text-3xl text-center">
    <span>{{hours}}</span>
    <span :class="invisible">:</span>
    <span>{{minutes}}</span>
    <span :class="invisible">:</span>
    <span>{{seconds}}</span>
  </div>
</template>

<script>
  export default {
    name: 'IntervalTimer',
    props: {
      initialValue: {type: Number, default: 0},
    },
    data() {
      return {
        value: this.initialValue/1000,
        interval: null,
        even: false,
      };
    },
    computed: {
      seconds() {
        return Math.round(this.value % 60).toString().padStart(2, '0');
      },
      minutes() {
        return Math.round(this.value / 60 % 60).toString().padStart(2, '0');
      },
      hours() {
        return Math.round(this.value / 60 / 60 % 60).toString().padStart(2, '0');
      },
      invisible() {
        return (this.even ? 'invisible' : '') + ' px-0.5 text-neutral-400 relative -top-0.5';
      }
    },
    created() {
      var ctx = this;
      var last = Date.now();
      var interval = setInterval(() => {
        try {
          ctx.value += (Date.now() - last)/1000;
          ctx.even = !ctx.even;
          last = Date.now();
        } catch(e) {
          clearInterval(interval);
        }
      }, 500);
      this.interval = interval;
    },
    beforeUnmount() {
      clearInterval(this.interval);
    },
  }
</script>
