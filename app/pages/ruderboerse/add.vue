<template>
  <ruderboerse-add />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['notAuthenticated']
}
</script>
