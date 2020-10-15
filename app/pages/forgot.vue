<template>
<div class="flex flex-col min-h-screen">
  <div class="flex-grow flex flex-col items-center justify-center p-3 lg:p-0">
    <img src="/rowmate_without_margins.png" class="w-full max-w-md px-3 pb-3 lg:px-6 lg:pb-6" />
    <form @submit.prevent="forgotPasswordSubmit" class="bg-color-form rounded-lg w-full max-w-md p-3 lg:p-6">
      <h1 class="text-2xl lg:text-4xl leading-none font-medium mb-3">{{ $t('forgotPassword' )}}</h1>
      <p class="text-gray-800 text-lg">Wenn du dein Passwort vergessen hast, schreibe Deine E-Mail Adresse in das folgende Feld. Wir senden dir dann eine E‑Mail mit einem Link zum Zurücksetzen des Passworts.</p>
      <p v-if="showResponse" :class="classResponse" class="lg:text-lg my-3">{{ response }}</p>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="email">
          {{ $t('email') }}
        </label>
        <input name="email" v-model="email" :class="[errors.email ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="email" type="text"
          placeholder="me@example.com">
        <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
      </div>
      <p class="text-right">
        <button class="cursor-pointer bg-color-button text-color-button rounded focus:outline-none px-4 py-2" type="submit">{{ $t('forgotPassword') }}</button>
      </p>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      errors: {
        email: false
      },
      email: null,
      response: null,
      showResponse: false,
      classResponse: null,
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  watch: {
    email: function() {
      if (this.email.trim() !== '') {
        if (this.emailRegex.test(this.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    }
  },
  middleware: 'notAuthenticated',
  methods: {
    forgotPasswordSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.email) {
        this.errors.email = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$post(`${process.env.API_URL}/auth/forgot-password`, {
          email: this.email.trim()
        }).then(res => {
          this.classResponse = 'text-green-500'
          this.showResponse = true
          this.response = res.message
        }).catch(error => {
          this.classResponse = 'text-red-500'
          this.showResponse = true

          if (error.hasOwnProperty('response')) {
            this.response = error.response.data.message
          } else {
            this.response = error.message
          }
        })
      }
    }
  }
}
</script>
