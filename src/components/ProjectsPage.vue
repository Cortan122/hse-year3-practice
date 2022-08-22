<template>
  <SortableTable :columns="columns" url="/api/projects" v-slot="{ entry }">
    <TableCell>
      <router-link :to="`/project/${entry.id}`" class="hover:underline">
        {{ entry.name }}
      </router-link>
    </TableCell>
    <TableCell>{{ entry.client }}</TableCell>
    <TableCell>{{ entry.company }}</TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.tasks_count }}</TableCell>
  </SortableTable>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'

  export default {
    name: 'ProjectsPage',
    components: {
      SortableTable,
      TableCell,
    },
    data() {
      return {
        columns: [
          {name: 'Name', sort: 'name'},
          {name: 'Client', sort: 'client'},
          {name: 'Company', sort: 'company'},
          {name: 'Created At', sort: 'created_at'},
          {name: 'Tasks', sort: 'tasks_count'},
        ],
      };
    },
  }
</script>
