<template>
  <SortableTable :columns="columns" url="/api/tags" v-slot="{ entry }">
    <TableCell>
      <span v-if="is_deleted[entry.id]" class="text-red-600">
        DELETED
      </span>
      <span v-else>{{ entry.name }}</span>
    </TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.tags_count }}</TableCell>
    <TableCell>
      <button class="!font-extrabold text-red-600" @click="() => del(entry)">
        <i class="codicon codicon-trash" aria-hidden="true"></i>
      </button>
      <button class="!font-extrabold text-red-600 ml-3" @click="() => rename(entry)">
        <i class="codicon codicon-edit" aria-hidden="true"></i>
      </button>
    </TableCell>
  </SortableTable>
  <CreationForm url="/api/tags" :fields="fields" title="Преименование тега" ref="form" button-text="Rename"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'TagsPage',
    components: {
      SortableTable,
      TableCell,
      CreationForm,
    },
    data() {
      return {
        columns: [
          {name: 'Name', sort: 'name'},
          {name: 'Created At', sort: 'created_at'},
          {name: 'Used', sort: 'tags_count'},
        ],
        fields: [
          {name: 'Old name', sort: 'old_name', type: String, readonly: true, value: '', required: true},
          {name: 'Name', sort: 'name', type: String, required: true},
        ],
        is_deleted: {},
      };
    },
    methods: {
      del(entry) {
        this.is_deleted[entry.id] = true;
        this.$http.delete(`/api/tags/${entry.id}`);
      },
      rename(entry) {
        this.fields[0].value = entry.name;
        this.$refs.form.updateValue();
        this.$refs.form.show();
      },
    },
  }
</script>
