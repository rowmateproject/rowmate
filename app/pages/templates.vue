<template>
  <templates />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['isNotSuperuser']
}
</script>
