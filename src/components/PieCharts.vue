<template>
  <div class="flex flex-col mb-5">
    <h2 class="text-center text-3xl font-medium pb-1">{{titletmpl}} «{{name}}»</h2>
    <div class="border-b-2 border-red-700 mx-20 lg:mx-32 2xl:mx-[20%]"></div>
  </div>

  <div class="flex justify-center flex-col space-y-10" v-if="!loading">
    <div v-for="(data, i) in charts" :key="i">
      <Pie :chart-data="data" :chart-options="title(data)" :height="50" v-if="data.type == 'pie' || data.type == 'donut'" class="w-1/3 mx-auto" />
      <Line :chart-data="data" :chart-options="title(data)" :height="250" v-if="data.type == 'line'" class="w-2/3 mx-auto" />
    </div>
  </div>

  <div class="flex h-[calc(100vh-10rem)]" v-if="loading">
    <Spinner class="m-auto" size="200"/>
  </div>
</template>

<script>
  import { Pie, Line } from 'vue-chartjs'
  import { Chart } from 'chart.js'
  import Spinner from 'vue-spinner/src/MoonLoader'
  import 'chart.js/auto'
  import autocolors from 'chartjs-plugin-autocolors'
  import merge from 'lodash/merge'

  Chart.register(autocolors)

  export default {
    name: 'PieCharts',
    components: {
      Spinner,
      Pie,
      Line,
    },
    props: {
      url: {type: String, required: true},
      nametmpl: {type: String, required: true},
      titletmpl: {type: String, required: true},
    },
    methods: {
      title(data) {
        var opts = this.options_line;
        if(data.type == 'pie'){
          opts = this.options_pie;
        }else if(data.type == 'donut'){
          opts = merge({}, this.options_pie, {cutout: '50%'});
        }

        return merge({}, opts, {
          plugins: {
            title: {
              display: !!data.title,
              text: data.title,
              font: {
                size: 18,
              }
            },
          }
        })
      },
      async init() {
        if(this.$route.path.split('/')[2] != this.url.split('/')[3])return;
        var id = parseInt(this.$route.params.id);

        this.id = id;
        this.name = `${this.nametmpl} №${id}`;
        this.loading = true;
        this.charts = null;

        if(isNaN(id))return;

        var responce = await this.$http.get(`${this.url}/${id}`);
        this.charts = responce.data.list;
        this.name = responce.data.name;
        this.loading = false;
      }
    },
    data() {
      return {
        loading: true,
        id: null,
        name: null,
        options_pie: {
          plugins: {
            autocolors: {
              offset: 5,
              mode: 'data',
            }
          },
        },
        options_line: {
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
    mounted() {
      this.init();
    },
    watch: {
      '$route.params.id'() {
        this.init();
      },
      url() {
        this.init();
      },
    },
  }
</script>
