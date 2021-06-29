<template>
  <boats />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['notAuthenticated']
}
</script>
