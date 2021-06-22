<template>
  <ruderboerse-entry />
</template>

<script>
export default {
  layout: 'admin',
  middleware: ['notAuthenticated']
}
</script>
