<template>
  <poll-form />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['authenticated']
}
</script>
