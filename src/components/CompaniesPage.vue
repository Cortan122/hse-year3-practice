<template>
  <SortableTable :columns="columns" url="/api/companies" v-slot="{ entry }" @newbtn="$refs.form.show()" button="true">
    <TableCell>{{ entry.name }}</TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.clients_count }}</TableCell>
    <TableCell>{{ entry.projects_count }}</TableCell>
    <TableCell>{{ entry.users_count }}</TableCell>
  </SortableTable>
  <CreationForm url="/api/companies" :fields="fields" title="Создание компании" ref="form"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'CompaniesPage',
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
          {name: 'Clients', sort: 'clients_count'},
          {name: 'Projects', sort: 'projects_count'},
          {name: 'Users', sort: 'users_count'},
        ],
        fields: [
          {name: 'Name', sort: 'name', type: String, required: true},
        ],
      };
    },
  }
</script>
