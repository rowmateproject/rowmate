<template>
  <poll-overview />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['notAuthenticated']
}
</script>
