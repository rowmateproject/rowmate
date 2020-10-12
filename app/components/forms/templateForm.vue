<template>
<form @submit.prevent="submitForm" class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-6 bg-color-form rounded shadow">
  <div class="grid grid-cols-4 gap-6 mb-6">
    <div class="col-span-2">
      <label class="flex justify-start items-center text-color-form" :for="makeId('locale', mailTemplate.locale)">
        <img v-if="mailTemplate.locale !== 'undefined'" :src="makePath(mailTemplate.locale)" :alt="mailTemplate.locale" class="h-4 mr-1">
        <span>Sprachauswahl</span>
      </label>
      <div class="col-span-3 relative z-0">
        <select v-model="mailTemplate.locale" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
          <option v-for="value, index in availableLocales" :key="index" :value="value.code">{{ value.name }}</option>
        </select>

        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
          <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>
    </div>
    <div class="col-span-2">
      <label class="flex justify-start items-center text-color-form" :for="makeId('topic', mailTemplate.locale)">
        Themenauswahl
      </label>
      <div class="col-span-3 relative z-0">
        <select v-model="mailTemplate.topic" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
          <option v-for="value, index in topics" :key="index" :value="value.id">{{ value.name }}</option>
        </select>

        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
          <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>
    </div>
  </div>

  <div class="mb-6">
    <label class="flex justify-start items-center text-color-form" :for="makeId('subject', mailTemplate.locale)">
      {{ $t('subject') }}
    </label>

    <input :id="makeId('subject', mailTemplate.locale)" type="text" v-model="mailTemplate.subject" :class="[errors.subject ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
    <p v-if="errors.subject" class="text-red-500 text-xs italic">{{ $t('errorInvalidSubject') }}</p>
  </div>

  <div>
    <label class="flex text-color-form" :for="makeId('message', mailTemplate.locale)">{{ $t('message') }}</label>
    <textarea :id="makeId('message', mailTemplate.locale)" type="text" v-model="mailTemplate.message" :class="[errors.message ? 'border-red-500 focus:border-red-500' : 'border-color-form']"
      class="h-64 w-full rounded border focus:outline-none p-2 mt-2 mb-1"></textarea>
    <p v-if="errors.message" class="text-red-500 text-xs italic">{{ $t('errorInvalidMessage') }}</p>
  </div>

  <div class="flex justify-end mt-4">
    <button class="px-4 py-2 bg-color-button text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
      {{ $t('save') }}
    </button>
  </div>
</form>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      mailTemplate: {},
      errors: {
        subject: false,
        message: false
      },
      topics: [{
        id: 'confirm',
        name: 'Anmeldebestätigung'
      }, {
        id: 'reset',
        name: 'Passwort zurücksetzen'
      }]
    }
  },
  mounted() {
    this.watchMe
  },
  computed: {
    watchMe: {
      get() {
        const data = {
          _id: this.$props.templateObject._id,
          topic: this.$props.templateObject.topic,
          subject: this.$props.templateObject.subject,
          message: this.$props.templateObject.message,
          locale: this.$props.templateObject.locale
        }

        this.mailTemplate = data
        return data
      },
      set(value) {
        this.$emit('resultObject', {
          template: value
        })

        this.mailTemplate = value
        console.log(value)
        return value
      }
    },
    availableLocales() {
      return this.$i18n.locales
    }
  },
  props: ['templateObject'],
  watch: {
    'mailTemplate.subject': function() {
      if (this.mailTemplate.subject !== '') {
        if (this.mailTemplate.subject.trim().length >= 3) {
          this.errors.subject = false
        } else {
          this.errors.subject = true
        }
      } else {
        this.errors.subject = false
      }
    },
    'mailTemplate.message': function() {
      if (this.mailTemplate.message !== '') {
        if (this.mailTemplate.message.trim().length >= 7) {
          this.errors.message = false
        } else {
          this.errors.message = true
        }
      } else {
        this.errors.message = false
      }
    }
  },
  methods: {
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    makeId(value, locale) {
      return `${value}-${locale}`
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
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.mailTemplate.subject) {
        this.errors.subject = true
      }

      if (!this.mailTemplate.message) {
        this.errors.message = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        let uuid = null

        try {
          uuid = this.buf2hex(uuidParse(this.mailTemplate._id))
        } catch (e) {
          console.debug(e.message)
        }

        if (!uuid) {
          this.$axios({
            method: 'POST',
            url: `${process.env.API_URL}/template/${this.mailTemplate.locale}/${this.mailTemplate.topic}`,
            data: {
              subject: this.mailTemplate.subject.trim(),
              message: this.mailTemplate.message.trim()
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              this.uuid = res.data || ''
            } else {
              console.debug(res.data)
            }
          })
        } else {
          this.$axios({
            method: 'PATCH',
            url: `${process.env.API_URL}/template/${uuid}`,
            data: {
              topic: this.mailTemplate.topic,
              locale: this.mailTemplate.locale,
              subject: this.mailTemplate.subject,
              message: this.mailTemplate.message
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              this.uuid = res.data || ''
            } else {
              console.debug(res.data)
            }
          })
        }
      }
    }
  }
}
</script>
