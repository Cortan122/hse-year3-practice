<template>
  <div @mousedown="click" @mouseup="click" @keydown.esc="hide" :class="overlay(shown)">
    <div class="m-auto bg-white shadow-md rounded-lg px-6 py-4 sm:max-w-md relative" @mousedown="stop" @mouseup="stop">
      <button @click="hide" class="rounded-full w-8 h-8 text-center absolute -top-3 -right-3
      bg-gradient-to-br from-red-500 to-red-600 hover:from-red-400 hover:to-red-600">
        <i class="codicon codicon-close !text-2xl text-white" aria-hidden="true"></i>
      </button>

      <h3 class="text-center text-xl font-medium border-b-2 mx-10 border-red-700 mb-2" v-if="title">
        {{ title }}
      </h3>

      <div v-if="error" class="mb-4 text-sm italic text-red-600">
        Что-то пошло не так! Возможно, этот {{error}} уже занят.
      </div>

      <form :action="url" method="POST">
        <label class="block mt-2" v-for="field in fields" :key="field.sort">
          <span :class="redstar(field.required)"> {{ field.name }} </span>

          <input v-if="field.type == String" :name="field.sort" class="textbox mt-1 block"
            :type="field.inputtype || 'text'" :required="field.required" :autocomplete="field.autocomplete"
            v-model="form[field.sort]" :readonly="field.readonly"/>

          <input v-if="field.type == Boolean" :name="field.sort" type="checkbox" class="mx-2 translate-y-0.5"
            v-model="form[field.sort]"/>

          <select v-if="field.type == 'select'" :name="field.sort" :required="field.required" class="textbox mt-1 block"
            v-model="form[field.sort]">
            <option :value="opt.id" v-for="opt in options[field.options]" :key="opt.id">{{ opt.name }}</option>
          </select>

          <textarea v-if="field.type == 'textarea'" :name="field.sort" :required="field.required"
            class="textbox mt-1 block resize-none w-96" v-model="form[field.sort]"></textarea>

          <div v-if="field.type == 'tags'">
            <input :required="field.required" :name="field.sort" type='hidden' :value="jsonTags">
            <VueTagsInput
              v-model="tag" :tags="tags" :autocomplete-items="filteredItems" class="w-3/5 mt-1"
              @tags-changed="newTags => {form[field.sort] = tags = newTags; tag = ''}"/>
          </div>

          <div v-if="field.type == 'duration'" class="mt-1 mx-3 flex flex-row">
            <input :required="field.required" :name="field.sort" type='hidden' :value="numTime">
            <VueSlider v-model="slider" width="5rem" orientation="circular" track-color="#D1D5DB" color="#10b981"
              :circle-offset="270" :height="10" :alwaysShowHandle="true" :handleScale="1.5"/>
            <div class="self-center ml-5">
              {{duration}}
            </div>
          </div>
        </label>

        <div class="flex items-center justify-end mt-4">
          <button class="button ml-4">
            {{buttonText}}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import VueTagsInput from '@sipec/vue3-tags-input'
  import VueSlider from 'vue3-slider'
  import humanizeDuration from 'humanize-duration'

  export default {
    name: 'CreationForm',
    components: {
      VueTagsInput,
      VueSlider,
    },
    props: {
      url: {type: String, required: true},
      buttonText: {type: String, default: 'Create'},
      fields: {type: Array, required: true},
      title: String,
    },
    data() {
      return {
        shown: false,
        form: {},
        options: {},
        error: this.$route.query.err,
        lastclick: 0,
        tags: [],
        tag: '',
        slider: 17,
      };
    },
    created() {
      if(this.$route.query.err) this.show();

      if(this.fields.filter(e => e.type == 'select' || e.type == 'tags').length) {
        var ctx = this;
        ctx.$http.get('/api/options').then(e => ctx.options = e.data);
      }
    },
    methods: {
      click() {
        if(this.lastclick == -1) {
          this.lastclick = 0;
          return;
        }
        var now = Date.now();
        if(now - this.lastclick < 1000) this.shown = false;
        this.lastclick = now;
      },
      stop() {
        this.lastclick = -1;
      },
      redstar(required) {
        return "text-sm font-medium text-slate-700" + (required ? " after:content-['*'] after:ml-0.5 after:text-red-500" : "");
      },
      overlay(shown) {
        return "w-full fixed top-0 left-0 overflow-hidden z-20 flex transition-[height] " + (
          shown ? "h-full bg-opacity-70 bg-black" : "h-0"
        );
      },
      show() {
        this.shown = true;
      },
      hide() {
        this.shown = false;
      },
      updateValue() {
        for(var field of this.fields) {
          if(field.value) {
            this.form[field.sort] = field.value;
          }
        }
      },
    },
    computed: {
      filteredItems() {
        if(!this.options['Tag'])return [];

        return this.options['Tag'].filter(i => {
          return i.name.toLowerCase().indexOf(this.tag.toLowerCase()) !== -1;
        }).map(i => {
          return {text: i.name};
        });
      },
      jsonTags() {
        return this.tags.map(e => e.text.trim());
      },
      numTime() {
        return (Math.pow(this.slider, 1.445) + 5) * 60000;
      },
      duration() {
        return humanizeDuration(this.numTime, { round: true, largest: 1, units: ['d', 'h', 'm'] });
      },
    },
  }
</script>

<style>
  .vue-tags-input .ti-tag {
    @apply bg-gradient-to-br from-emerald-500 to-emerald-600 text-white;
  }

  .vue3-slider.circular .handle-container .handle.hover {
    @apply bg-gradient-to-br from-emerald-600 to-emerald-700;
  }

  .vue3-slider.circular .handle-container .handle.hover:hover {
    @apply from-emerald-500 to-emerald-700;
  }
</style>
