<template>
  <td class="border-t">
    <p class="px-6 py-4 flex items-center">
      <slot></slot>
    </p>
  </td>
</template>

<script>
  export default {
    name: 'TableCell',
  }
</script>
