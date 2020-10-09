<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Umfagen</h3>

  <div class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow">
    <question-filter @resultObject="handleFilterObject" @resetFilter="handleResetValue" />
  </div>

  <form @submit.prevent="submitForm" class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
    <question-form v-if="questions.length > 0" v-for="value, index in questions" :key="value._id" @resultObject="handleFormObject($event, index)" :formObject="value" class="mb-6" />

    <div class="flex justify-end">
      <button @click="addPollForm" class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2">
        Frage hinzufügen
      </button>
      <button v-if="questions.length > 0" class="bg-color-button text-color-button rounded focus:outline-none px-4 py-2 ml-4">
        {{ $t('save') }}
      </button>
    </div>
  </form>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      questions: []
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    handleResetValue(value) {
      if (value === true) {
        this.questions = []
      }
    },
    handleFilterObject(value) {
      this.questions = [value]
    },
    handleFormObject(value, index) {
      this.questions[index] = value
    },
    addPollForm(value) {
      this.questions.push({
        question: null,
        type: 'select',
        forms: [{
          id: 'option0',
          value: null
        }]
      })
    },
    buf2hex(buffer) {
      const byteArray = new Uint8Array(buffer)
      const hexParts = []

      for (let i = 0; i < byteArray.length; i++) {
        const hex = byteArray[i].toString(16)
        const paddedHex = ('00' + hex).slice(-2)
        hexParts.push(paddedHex)
      }

      return hexParts.join('')
    },
    submitForm() {
      try {
        const uuid = this.buf2hex(uuidParse(this._id))

        this.$axios({
          method: 'PATCH',
          url: `${process.env.API_URL}/poll/${uuid}`,
          data: {
            questions: this.questions,
            translation: this.currentLocale
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.uuid = res.data
          }
        })
      } catch {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/poll`,
          data: {
            questions: this.questions,
            translation: this.currentLocale
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status !== 200) {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
