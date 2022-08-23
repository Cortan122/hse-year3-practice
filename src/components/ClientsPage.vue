<template>
  <SortableTable :columns="columns" url="/api/clients" v-slot="{ entry }" @newbtn="$refs.form.show()" button="true">
    <TableCell>{{ entry.name }}</TableCell>
    <TableCell>{{ entry.company }}</TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.projects_count }}</TableCell>
  </SortableTable>
  <CreationForm url="/api/clients" :fields="fields" title="Создание клиента" ref="form"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'ClientsPage',
    components: {
      SortableTable,
      TableCell,
      CreationForm,
    },
    data() {
      return {
        columns: [
          {name: 'Name', sort: 'name'},
          {name: 'Company', sort: 'company'},
          {name: 'Created At', sort: 'created_at'},
          {name: 'Projects', sort: 'projects_count'},
        ],
        fields: [
          {name: 'Name', sort: 'name', type: String, required: true},
          {name: 'Company', sort: 'company_id', type: 'select', options: 'Company', required: true},
        ],
      };
    },
  }
</script>
