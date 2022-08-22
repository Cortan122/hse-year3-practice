<template>
  <div class="flex h-[calc(100vh-10rem)]" v-if="loading">
    <Spinner class="m-auto" size="200"/>
  </div>

  <div v-else class="max-w-7xl mx-auto sm:px-6 lg:px-8 py-12">
    <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
      <!-- Search Input -->
      <div class="mb-6 flex justify-between items-center" v-if="filters">
        <SearchFilter v-model="form.search" class="w-full max-w-md mr-4" @reset="reset" />
      </div>
      <!-- Table -->
      <div class="bg-white rounded overflow-x-auto">
        <table class="w-full whitespace-no-wrap">
          <!-- Headers -->
          <tr class="text-left font-bold">
            <th class="px-6 pt-6 pb-4 cursor-pointer" v-for="col in columns" :key="col" @click="sort(col.sort)"
              :class="{ 'sorted-decs': form.sort == col.sort.toUpperCase(), 'sorted-asc': form.sort == col.sort }">
              {{col.name}}
            </th>
          </tr>
          <!-- Table Rows -->
          <tr v-for="entry in list" :key="entry.id" class="hover:bg-gray-100 focus-within:bg-gray-100">
            <slot :entry="entry"></slot>
          </tr>
          <!-- No data message -->
          <tr v-if="list?.length == 0">
            <td class="border-t px-6 py-4" colspan="4">No data found.</td>
          </tr>
        </table>
      </div>

      <!-- Pagination? -->
      <!-- <pagination :links="links" /> -->
    </div>
  </div>
</template>

<script>
import SearchFilter from '@/components/SearchFilter'
import Spinner from 'vue-spinner/src/MoonLoader'
import mapValues from 'lodash/mapValues'
import pickBy from 'lodash/pickBy'
import throttle from 'lodash/throttle'

export default {
  name: "SortableTable",
  components: {
    SearchFilter,
    Spinner,
  },
  props: {
    columns: {type: Array, required: true},
    url: {type: String, required: true},
  },
  data() {
    return {
      loading: true,
      list: null,
      filters: null,
      form: {
        search: null,
        sort: null,
        tag: null,
      },
    }
  },
  methods: {
    reset() {
      this.form = mapValues(this.form, () => null);
    },
    sort(newsort) {
      if (newsort == '') {
        return;
      }

      if (this.form.sort == newsort) {
        this.form.sort = newsort.toUpperCase();
      } else {
        this.form.sort = newsort;
      }
    },
    init(e) {
      this.list = e.data.list;

      if(this.loading){
        this.filters = e.data.filter;
        this.form.search = e.data.filter.search;
        this.form.sort = e.data.filter.sort;
        this.form.tag = e.data.filter.tag;
        this.$watch('form', throttle(this.update, 200), {deep: true});
        this.loading = false;
      }
    },
    update() {
      var params = pickBy(this.form);
      this.$http.get(this.url, {params}).then(this.init);
    },
  },
  created() {
    this.update();
  },
}
</script>

<style scoped>
  .sorted-decs:after {
    color: #dc2626;
    content: " \25E4";
  }

  .sorted-asc:after {
    color: #dc2626;
    content: " \25E3";
  }
</style>
