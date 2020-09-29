<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">{{ $t('mail') }}</h3>
  <mail-form v-for="value, index in availableLocales" :code="value.code" :key="index" />
</div>
</template>

<script>
export default {
  computed: {
    availableLocales() {
      return this.$i18n.locales
    }
  },
  methods: {}
}
</script>
