<template>
<div class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
  <form @submit.prevent="submitForm">
    <div class="mb-6">
      <label class="flex justify-start items-center text-color-form" :for="makeId('subject', locale)">
        <img :src="makePath(locale)" :alt="locale" class="h-4 mr-1">
        <span>{{ $t('subject') }}</span>
      </label>
      <input :id="makeId('subject', locale)" type="text" v-model="mail.subject" :class="[errors.subject ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.subject" class="text-red-500 text-xs italic">{{ $t('errorInvalidSubject') }}</p>
    </div>

    <div>
      <label class="flex text-color-form" :for="makeId('message', locale)">{{ $t('message') }}</label>
      <textarea :id="makeId('message', locale)" type="text" v-model="mail.message" :class="[errors.message ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="h-64 w-full rounded border focus:outline-none p-2 mt-2 mb-1"></textarea>
      <p v-if="errors.message" class="text-red-500 text-xs italic">{{ $t('errorInvalidMessage') }}</p>
    </div>

    <div class="flex justify-end mt-4">
      <button class="px-4 py-2 bg-color-button text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
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
      mail: {
        uuid: '',
        subject: '',
        message: ''
      },
      errors: {
        subject: false,
        message: false
      }
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/mail/${this.locale}/confirm`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.mail.uuid = res.data.id || ''
        this.mail.subject = res.data.subject || ''
        this.mail.message = res.data.message || ''
      } else if (res.status === 404) {
        console.log(res.data)
      }
    })
  },
  watch: {
    'mail.subject': function() {
      if (this.mail.subject.trim() !== '') {
        if (this.mail.subject.trim().length >= 7) {
          this.errors.subject = false
        } else {
          this.errors.subject = true
        }
      }
    },
    'mail.message': function() {
      if (this.mail.message.trim() !== '') {
        if (this.mail.message.trim().length >= 7) {
          this.errors.message = false
        } else {
          this.errors.message = true
        }
      }
    }
  },
  computed: {
    locale() {
      return this.$props.code
    }
  },
  props: ['code'],
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

      return hexParts.join('');
    },
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.mail.subject) {
        this.errors.subject = true
      }

      if (!this.mail.message) {
        this.errors.message = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        let uuid = null

        try {
          uuid = this.buf2hex(uuidParse(this.mail.uuid))
        } catch (e) {
          console.debug(e.message)
        }

        if (!uuid) {
          this.$axios({
            method: 'POST',
            url: `${process.env.API_URL}/mail/${this.locale}/confirm`,
            data: {
              subject: this.mail.subject.trim(),
              message: this.mail.message.trim()
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              this.mail.uuid = res.data.id || ''
              console.debug(res.data)
            } else {
              console.debug(res.data)
            }
          })
        } else {
          this.$axios({
            method: 'PATCH',
            url: `${process.env.API_URL}/mail/${uuid}`,
            data: {
              subject: this.mail.subject.trim(),
              message: this.mail.message.trim()
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              console.debug(res.data)
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
