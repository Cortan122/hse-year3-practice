<template>
  <div class="relative">
    <slot></slot>
  </div>
</template>

<script>
  import PerfectScrollbar from 'perfect-scrollbar'
  import 'perfect-scrollbar/css/perfect-scrollbar.css'

  export default {
    name: 'PerfectScrollbar',
    data() {
      return {
        ps: null,
      };
    },
    methods: {
      update() {
        this.ps?.update();
      },
      init() {
        if (!this.ps) {
          this.ps = new PerfectScrollbar(this.$el, {
            wheelSpeed: 0.5,
            wheelPropagation: false,
            minScrollbarLength: 20,
          });
        } else {
          this.ps.update();
        }
      },
      uninit() {
        this.ps?.destroy();
        this.ps = null;
      }
    },
    watch: {
      $route() {
        this.update()
      }
    },
    mounted() {
      this.init()
    },
    updated() {
      this.$nextTick(this.update)
    },
    activated() {
      this.init()
    },
    deactivated() {
      this.uninit()
    },
    beforeUnmount() {
      this.uninit()
    }
  }
</script>
