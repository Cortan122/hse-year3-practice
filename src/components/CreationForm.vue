<template>
  <div @mousedown="click" :class="overlay(shown)">
    <div class="m-auto bg-white shadow-md rounded-lg px-6 py-4 sm:max-w-md relative" @mousedown="formclick">
      <button @click="click" class="rounded-full w-8 h-8 text-center absolute -top-3 -right-3
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
            v-model="form[field.sort]"/>

          <input v-if="field.type == Boolean" :name="field.sort" type="checkbox" class="mx-2 translate-y-0.5"
            v-model="form[field.sort]"/>

          <select v-if="field.type == 'select'" :name="field.sort" v-model="form[field.sort]" class="textbox mt-1 block">
            <option :value="opt.id" v-for="opt in options[field.options]" :key="opt.id">{{ opt.name }}</option>
          </select>
        </label>

        <div class="flex items-center justify-end mt-4">
          <button class="button ml-4">
            Create
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'CreationForm',
    props: {
      url: {type: String, required: true},
      fields: {type: Array, required: true},
      title: String,
    },
    data() {
      return {
        shown: false,
        form: {},
        options: {},
        error: this.$route.query.err,
      };
    },
    created() {
      if(this.$route.query.err) this.show();

      var ctx = this;
      ctx.$http.get('/api/options').then(e => ctx.options = e.data);
    },
    methods: {
      click() {
        this.shown = false;
      },
      formclick(e) {
        e.stopPropagation();
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
    },
  }
</script>
