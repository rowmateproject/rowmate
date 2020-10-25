<template>
  <language />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['isNotSuperuser']
}
</script>
