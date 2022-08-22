<template>
  <SortableTable :columns="columns" url="/api/projects" v-slot="{ entry }">
    <!-- Project Name -->
    <td class="border-t">
      <p class="px-6 py-4 flex items-center focus:text-indigo-500">
        {{ entry.name }}
      </p>
    </td>

    <!-- Project Client -->
    <td class="border-t">
      <p class="px-6 py-4 flex items-center focus:text-indigo-500">
        {{ entry.client }}
      </p>
    </td>

    <!-- Project Company -->
    <td class="border-t">
      <p class="px-6 py-4 flex items-center focus:text-indigo-500">
        {{ entry.company }}
      </p>
    </td>

    <!-- Entry Date -->
    <td class="border-t">
      <p class="px-6 py-4 flex items-center" tabindex="-1">
        {{ new Date(entry.created_at).toLocaleString("ru-RU") }}
      </p>
    </td>

    <!-- Task Count -->
    <td class="border-t">
      <p class="px-6 py-4 flex items-center" tabindex="-1">
        {{ entry.tasks_count }}
      </p>
    </td>
  </SortableTable>
</template>

<script>
  import SortableTable from '@/components/SortableTable'

  export default {
    name: 'ProjectsPage',
    components: {
      SortableTable,
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
