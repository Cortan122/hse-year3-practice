<template>
  <SortableTable :columns="columns" url="/api/tasks" v-slot="{ entry }" @newbtn="$refs.form.show()" :button="true">
    <TableCell>{{ entry.name }}</TableCell>
    <TableCell>
      <router-link :to="`/project/${entry.project_id}`" class="hover:underline">
        {{ entry.project }}
      </router-link>
    </TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.tasks_count }}</TableCell>
    <td class="border-t w-1/4">
      <TagsEditor :tags="entry.tags" :readonly="true" />
    </td>
    <TableCell>
      <i v-if="entry.completed" class="codicon codicon-check !font-extrabold text-emerald-600" aria-hidden="true"></i>
      <i v-else class="codicon codicon-close !font-extrabold text-red-600" aria-hidden="true"></i>
    </TableCell>
  </SortableTable>
  <CreationForm url="/api/tasks" :fields="fields" title="Создание задачи" ref="form"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'
  import TagsEditor from '@/components/TagsEditor'

  export default {
    name: 'TasksPage',
    components: {
      SortableTable,
      TableCell,
      CreationForm,
      TagsEditor,
    },
    data() {
      return {
        columns: [
          {name: 'Name', sort: 'name'},
          {name: 'Project', sort: 'project'},
          {name: 'Created At', sort: 'created_at'},
          {name: 'Tasks', sort: 'tasks_count'},
          {name: 'Tags', sort: 'tags_count'},
          {name: 'Completed', sort: 'completed'},
        ],
        fields: [
          {name: 'Name', sort: 'name', type: String, required: true},
          {name: 'Description', sort: 'description', type: 'textarea'},
          {name: 'Tags', sort: 'tags', type: 'tags'},
          {name: 'Project', sort: 'project_id', type: 'select', options: 'Project', required: true},
          {name: 'Estimated workload', sort: 'workload', type: 'duration'},
        ],
      };
    },
  }
</script>
