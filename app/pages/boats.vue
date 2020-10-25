<template>
  <boats />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['isNotSuperuser']
}
</script>
