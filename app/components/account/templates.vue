<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Vorlagen</h3>

  <div class="mt-3 p-3 lg:p-6 bg-color-form rounded-md shadow">
    <h4 class="text-color-form">Template Filter</h4>
    <template-filter @resultObject="handleTemplateObject" @resetFilter="handleTemplateResetValue" />
  </div>

  <template-form v-if="mailTemplate" @resultObject="handleTemplateObject" :templateObject="mailTemplate" />

  <div v-if="!mailTemplate" class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
    <div class="flex justify-end">
      <button @click="createTemplateForm" class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2">
        Template erstellen
      </button>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      mailTemplate: null
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    createTemplateForm() {
      this.mailTemplate = {
        locale: this.currentLocale,
        subject: '',
        message: '',
        topic: '',
        _id: ''
      }
    },
    handleTemplateResetValue(value) {
      if (value === true) {
        this.mailTemplate = null
      }
    },
    handleTemplateObject(value) {
      this.mailTemplate = value.template
    }
  }
}
</script>
