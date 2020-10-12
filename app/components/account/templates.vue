<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium text-color-title">Vorlagen</h3>

  <div class="bg-svg-image bg-blue-500 rounded shadow p-3 lg:px-6 lg:pb-6 lg:pt-4 mt-1 sm:mt-3 md:mt-5 lg:mt-8 mb-3 md:mb-5 lg:mb-8">
    <h4 class="text-color-nav">Template Filter</h4>
    <template-filter @resultObject="handleTemplateObject" @resetFilter="handleTemplateResetValue" />
  </div>

  <div class="bg-color-image rounded px-3 lg:px-6 pb-3 lg:pb-6 pt-2 lg:pt-4 mt-8">
    <h4 class="text-xl mb-1">Hinweis</h4>
    <p class="mb-2">Es können folgende Template Variablen im Style von <code v-html="variableExample" class="font-mono"></code> in den verwendet werden.</p>
    <ul class="grid grid-cols-12 gap-x-6 list-inside list-disc">
      <li v-for="value, index in templateVariables" :key="index" class="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3 font-mono">{{ value }}</li>
    </ul>
  </div>

  <template-form v-if="editTemplate" @resultObject="handleTemplateObject" :templateObject="editTemplate" />
  <template-cards v-if="templates.length > 0" @deleteResultId="deleteTemplate" @resultObject="handleTemplatesObject" :templates="templates" />

  <div v-if="!editTemplate && templates.length === 0" class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-6 bg-color-form rounded shadow">
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
      variableExample: '{{ variablen_name }}',
      templateVariables: [
        'author_name',
        'author_phone',
        'author_mail',
        'user_name',
        'user_phone',
        'user_mail',
        'org_name',
        'org_logo',
        'org_mail',
        'org_phone',
        'org_street',
        'org_zip_code',
        'org_house_number',
        'org_location',
        'org_address',
        'event_date',
        'event_title',
        'event_contact',
        'event_attendees',
        'event_description',
        'event_location',
        'current_date',
        'current_time',
        'action_title',
        'action_url'
      ],
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
        url: `${process.env.API_URL}/templates`,
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
