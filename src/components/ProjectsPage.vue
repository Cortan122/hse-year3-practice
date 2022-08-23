<template>
  <SortableTable :columns="columns" url="/api/projects" v-slot="{ entry }" @newbtn="$refs.form.show()" button="true">
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
  <CreationForm url="/api/projects" :fields="fields" title="Создание проекта" ref="form"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'ProjectsPage',
    components: {
      SortableTable,
      TableCell,
      CreationForm,
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
        fields: [
          {name: 'Name', sort: 'name', type: String, required: true},
          {name: 'Description', sort: 'description', type: 'textarea'},
          {name: 'Client', sort: 'client_id', type: 'select', options: 'Client', required: true},
        ],
      };
    },
  }
</script>
