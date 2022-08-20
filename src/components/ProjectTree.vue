<template>
  <div class="bg-gray-200 border-r border-gray-100 min-w-[20rem] flex flex-col">
    <div class="overflow-y-auto flex-auto p-2">
      <h3 class="text-center text-xl font-medium border-b-2 mx-10 border-red-700 mb-2">Список проектов</h3>
      <TreeView class="tree" :load-nodes-async="loadNodesAsync" :modelDefaults="modelDefaults" >
        <template v-slot:text="{ model }">
          <router-link :to="model.id" v-if="model.children.length == 0" :class="this.$route.path == model.id ? 'font-bold' : ''">
            {{model.label}}
          </router-link>
          <span v-else>{{model.label}}</span>
        </template>

        <template v-slot:loading-root>
          <div class="flex h-[calc(100vh-11rem)]"><Spinner class="m-auto"/></div>
        </template>
      </TreeView>
    </div>

    <IntervalTimer v-if="showTimer" :initial-value="timerValue" class="flex-initial pb-2"/>
  </div>
</template>

<script>
  import TreeView from "@grapoza/vue-tree"
  import Spinner from 'vue-spinner/src/MoonLoader'
  import IntervalTimer from '@/components/IntervalTimer'
  import '@vscode/codicons/dist/codicon.css'

  export default {
    name: 'ProjectTree',
    components: {
      TreeView,
      Spinner,
      IntervalTimer,
    },
    data() {
      return {
        modelDefaults: {
          state: {
            expanded: true,
          }
        }
      };
    },
    methods: {
      loadNodesAsync() {
        return this.$http.get('/api/project_tree').then(e => e.data);
      }
    },
    computed: {
      showTimer() {
        return this.$root.user.has_current_task;
      },
      timerValue() {
        return this.$root.user.timer || 0;
      }
    },
  }
</script>

<style>
  .grtv-wrapper.grtv-default-skin .grtvn-self-expander i.grtvn-self-expanded-indicator::before {
    content: '\eab6';
    font: normal normal normal 16px/1 codicon;
  }

  .grtv-wrapper.grtv-default-skin .grtvn-self-expander.grtvn-self-expanded i.grtvn-self-expanded-indicator::before {
    content: '\eab4';
    font: normal normal normal 16px/1 codicon;
  }
</style>

<style scoped>
  .tree {
    --baseHeight: 1.3rem;
    --itemSpacing: 0px;
  }
</style>
