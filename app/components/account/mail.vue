<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">{{ $t('mail') }}</h3>

  <form @submit.prevent="submitForm">
    <div v-for="value, index in availableLocales" :key="index" class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
      <div class="mb-6">
        <label class="flex justify-start items-center text-color-form" for="subject">
          <img :src="makePath(value.code)" :alt="value.name" class="h-4 mr-1">
          <span>{{ $t('subject') }}</span>
        </label>
        <input id="subject" type="text" v-model="mail.subject" :class="[errors.subject ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.subject" class="text-red-500 text-xs italic">{{ $t('errorInvalidSubject') }}</p>
      </div>

      <div>
        <label class="flex text-color-form" for="message">{{ $t('message') }}</label>
        <textarea id="message" type="text" v-model="mail.message" :class="[errors.message ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="h-64 w-full rounded border focus:outline-none p-2 mt-2 mb-1"></textarea>
        <p v-if="errors.message" class="text-red-500 text-xs italic">{{ $t('errorInvalidMessage') }}</p>
      </div>

      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-color-button text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
          {{ $t('save') }}
        </button>
      </div>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {
      mail: {
        subject: null,
        message: null
      },
      errors: {
        subject: false,
        message: false
      },
      showResponse: false,
      response: null
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/mail/confirm`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.mail.subject = res.data.subject || ''
        this.mail.message = res.data.message || ''
      } else {
        console.debug(res.data)
      }
    })
  },
  watch: {
    'mail.subject': function() {
      if (this.mail.subject.trim() !== '') {
        if (this.mail.subject.trim().length > 7) {
          this.errors.subject = false
        } else {
          this.errors.subject = true
        }
      }
    },
    'mail.message': function() {
      if (this.mail.message.trim() !== '') {
        if (this.mail.message.trim().length > 7) {
          this.errors.message = false
        } else {
          this.errors.message = true
        }
      }
    }
  },
  computed: {
    availableLocales() {
      return this.$i18n.locales
    }
  },
  methods: {
    makePath(value) {
      return `/flags/${value}.svg`
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
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/mail/confirm $t('mail') `,
          data: {
            subject: this.mail.subject.trim(),
            message: this.mail.message.trim()
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.showResponse = true
            this.classResponse = 'text-green-500'
            this.response = 'Mail Templaste wurden geändert'
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
