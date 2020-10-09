<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Vorlagen</h3>

  <div class="mt-3 p-3 lg:p-6 bg-color-form rounded-md shadow">
    <h4 class="text-color-form">Template Filter</h4>
    <template-filter @resultObject="handleTemplateObject" @resetFilter="handleTemplateResetValue" />
  </div>

  <template-form v-if="editTemplate" @resultObject="handleTemplateObject" :templateObject="editTemplate" />
  <template-cards v-if="templates.length > 0" @deleteResultId="deleteTemplate" @resultObject="handleTemplatesObject" :templates="templates" />

  <div v-if="!editTemplate && templates.length === 0" class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
    <div class="flex justify-end">
      <button @click="showAllTemplates" class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2">
        Alle Templates anzeigen
      </button>
      <button @click="createTemplateForm" class="bg-color-button text-color-button rounded focus:outline-none px-4 py-2 ml-4">
        Template erstellen
      </button>
    </div>
  </div>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      templates: [],
      showTemplateForm: false,
      editTemplate: null
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    createTemplateForm() {
      this.editTemplate = {
        locale: this.currentLocale,
        subject: '',
        message: '',
        topic: '',
        _id: ''
      }
    },
    handleTemplateResetValue(value) {
      if (value === true) {
        this.templates = []
        this.editTemplate = null
      }
    },
    handleTemplateObject(value) {
      this.editTemplate = value.template
    },
    handleTemplatesObject(value) {
      this.editTemplate = value
      this.templates = []
    },
    buf2hex(buffer) {
      const byteArray = new Uint8Array(buffer)
      const hexParts = []

      for (let i = 0; i < byteArray.length; i++) {
        const hex = byteArray[i].toString(16)
        const paddedHex = ('00' + hex).slice(-2)
        hexParts.push(paddedHex)
      }

      return hexParts.join('');
    },
    deleteTemplate(value) {
      let uuid = null

      try {
        uuid = this.buf2hex(uuidParse(value))
      } catch (e) {
        console.debug(e)
      }

      this.$axios({
        method: 'DELETE',
        url: `${process.env.API_URL}/template/${uuid}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200 && res.data === true) {
          this.templates = this.templates.filter(e => e['_id'] !== value)
        } else {
          console.debug(res.data)
        }
      })
    },
    showAllTemplates() {
      this.editTemplate = null

      this.$axios({
        method: 'GET',
        url: `${process.env.API_URL}/templates/`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          this.templates = res.data
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
