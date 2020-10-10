<template>
  <boats />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['authenticated', 'isNotSuperuser']
}
</script>
