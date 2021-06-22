<template>
  <ruderboerse />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['notAuthenticated']
}
</script>
