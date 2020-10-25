<template>
  <organization />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['isNotSuperuser']
}
</script>
