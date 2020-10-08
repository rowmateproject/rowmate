<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Vorlagen</h3>

  <div class="mt-3 p-3 lg:p-6 bg-color-form rounded-md shadow">
    <h4 class="text-color-form">Template Filter</h4>
    <template-filter @resultObject="handleTemplateFilterResult" @resetFilter="handleTemplateResetValue" />
  </div>

  <template-form v-for="value, index in availableLocales" :code="value.code" :key="index" />
</div>
</template>

<script>
export default {
  data() {
    return {
      mailTemplate: {}
    }
  },
  computed: {
    availableLocales() {
      return this.$i18n.locales
    }
  },
  methods: {
    handleTemplateResetValue(value) {
      if (value === true) {
        this.mailTemplate = {}
      }
    },
    handleTemplateFilterResult(value) {
      this.mailTemplate = value._id
    }
  }
}
</script>
