<template>
  <div class="flex flex-col mb-5">
    <h2 class="text-center text-3xl font-medium pb-1">Графики активности</h2>
    <div class="border-b-2 border-red-700 mx-20 lg:mx-32 2xl:mx-[20%]"></div>
  </div>

  <div class="flex justify-center flex-col space-y-10" v-if="!loading">
    <Line :chart-data="data" :chart-options="title(data)" v-for="(data, i) in charts" :key="i"
      class="w-2/3 mx-auto" :height="250" />
  </div>

  <div class="flex h-[calc(100vh-10rem)]" v-if="loading">
    <Spinner class="m-auto" size="200"/>
  </div>
</template>

<script>
  import { Line } from 'vue-chartjs'
  import { Chart } from 'chart.js'
  import Spinner from 'vue-spinner/src/MoonLoader'
  import 'chart.js/auto'
  import autocolors from 'chartjs-plugin-autocolors'
  import merge from 'lodash/merge'

  Chart.register(autocolors)

  export default {
    name: 'BasicChart',
    components: {
      Spinner,
      Line,
    },
    methods: {
      title(data) {
        return merge({}, this.options, {
          plugins: {
            title: {
              display: true,
              text: data.title,
              font: {
                size: 18,
              }
            }
          }
        })
      },
    },
    data() {
      return {
        loading: true,
        options: {
          scales: {
            y: {
              ticks: {
                callback(value) {
                  return value + ' hours';
                }
              }
            }
          },
          plugins: {
            autocolors: {
              offset: 5
            }
          },
          elements: {
            line: {
              tension: 0.2,
            }
          },
        },
        charts: null,
      };
    },
    async mounted() {
      var responce = await this.$http.get('/api/stats');
      this.charts = responce.data;
      this.loading = false;
    },
  }
</script>
