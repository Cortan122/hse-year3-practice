<template>
  <SortableTable :columns="columns" url="/api/users" v-slot="{ entry }" @newbtn="$refs.form.show()" :button="true">
    <TableCell>{{ entry.name }}</TableCell>
    <TableCell>{{ entry.email }}</TableCell>
    <TableCell>{{ entry.company }}</TableCell>
    <TableCell>{{ new Date(entry.created_at).toLocaleString("ru-RU") }}</TableCell>
    <TableCell>{{ entry.tasks_count }}</TableCell>
    <TableCell>
      <i v-if="entry.is_admin" class="codicon codicon-check !font-extrabold text-emerald-600" aria-hidden="true"></i>
      <i v-else class="codicon codicon-close !font-extrabold text-red-600" aria-hidden="true"></i>
    </TableCell>
  </SortableTable>
  <CreationForm url="/api/users" :fields="fields" title="Создание пользователя" ref="form"/>
</template>

<script>
  import SortableTable from '@/components/SortableTable'
  import TableCell from '@/components/TableCell'
  import CreationForm from '@/components/CreationForm'

  export default {
    name: 'UsersPage',
    components: {
      SortableTable,
      TableCell,
      CreationForm,
    },
    data() {
      return {
        columns: [
          {name: 'Name', sort: 'first_name'},
          {name: 'Email', sort: 'email'},
          {name: 'Company', sort: 'company'},
          {name: 'Created At', sort: 'created_at'},
          {name: 'Tasks', sort: 'tasks_count'},
          {name: 'Admin', sort: 'is_admin'},
        ],
        fields: [
          {name: 'First name', sort: 'first_name', type: String, required: true, autocomplete: 'given-name'},
          {name: 'Last name', sort: 'last_name', type: String, autocomplete: 'family-name'},
          {name: 'Email', sort: 'email', type: String, required: true, inputtype: 'email', autocomplete: 'email'},
          {name: 'Password', sort: 'password', type: String, required: true, inputtype: 'password', autocomplete: 'current-password'},
          {name: 'Admin?', sort: 'is_admin', type: Boolean},
          {name: 'Company', sort: 'company_id', type: 'select', options: 'Company'},
        ],
      };
    },
  }
</script>
