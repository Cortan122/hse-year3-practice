<template>
  <span v-for="tag in filteredTags" :key="tag.id" @dblclick="beginEdit(tag)"
    class="text-white mx-1 my-1.5 rounded-2xl px-2 py-1 inline-block"
    :class="{ 'bg-emerald-400': !readonly, 'bg-red-400': readonly}">
    &#8203;{{ tag.name }}&#8203;
  </span>

  <form @submit.prevent="done" class="inline-block">
    <input type="text" v-if="textbox_visible" ref="textbox" @blur="blur" v-model="textbox_value"
      class="text-white mx-1 my-1.5 bg-emerald-400 rounded-2xl px-3 py-1 inline-block border-none w-2/3 outline-emerald-600" />
  </form>

  <button tabindex="0" aria-label="Add tags" @click="addTag()" v-if="!textbox_visible && !readonly"
    class="text-white mx-1 my-1.5 rounded-2xl px-2 py-1 inline-block font-bold w-8
    bg-gradient-to-br from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-600">
    &#8203;&#xff0b;&#8203;
  </button>
</template>

<script>
export default {
  name: "TagsEditor",
  props: {
    tags: {type: Array, required: true},
    readonly: {type: Boolean, default: false},
  },
  data() {
    return {
      textbox_visible: false,
      textbox_value: '',
      selected_tag: null,
    }
  },
  computed: {
    filteredTags() {
      return this.tags.filter(i => i.id != this.selected_tag?.id);
    },
  },
  methods: {
    addTag() {
      this.textbox_visible = true;
      setTimeout(() => this.$refs.textbox.focus(), 1);
    },
    blur() {
      this.textbox_visible = false;
      if (this.selected_tag) {
        this.textbox_value = '';
        this.selected_tag = null;
      }
    },
    done() {
      var value = this.textbox_value.trim();
      if (this.selected_tag) {
        if (value == "") {
          this.$emit('deleteTag', this.selected_tag.name);
        } else if (this.selected_tag.name != value) {
          this.$emit('replaceTag', this.selected_tag.name, value);
        }
      } else {
        this.$emit('addTag', value);
      }

      this.selected_tag = null;
      this.textbox_visible = false;
      this.textbox_value = '';
    },
    beginEdit(tag) {
      if(this.readonly) return;
      this.textbox_value = tag.name;
      this.selected_tag = tag;
      this.textbox_visible = true;
      setTimeout(() => this.$refs.textbox.focus(), 1);
    },
  },
}
</script>
