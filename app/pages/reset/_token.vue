<template>
<div class="flex flex-col min-h-screen">
  <div class="flex-grow flex flex-col items-center justify-center p-3 lg:p-0">
    <img src="/rowmate_without_margins.png" class="w-full max-w-md px-3 pb-3 lg:px-6 lg:pb-6" />
    <form @submit.prevent="submitForm" class="bg-color-form rounded-lg w-full max-w-md p-3 lg:p-6">
      <h1 class="text-2xl lg:text-4xl leading-none font-medium mb-3">Passwort ändern</h1>
      <p v-if="showResponse" :class="classResponse" class="lg:text-lg mb-3">{{ response }}</p>
      <p class="text-lg w-full lg:w-11/12">Um Dein aktuelles Passwort zurückzusetzen, gebe ein starkes Passwort ein und bestätige das Passwort nochmals. Anschließend wirst Du zur <nuxt-link to="/signin" class="text-blue-600 hover:text-blue-800">
          Anmeldeseite</nuxt-link> weitergeleitet.</p>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="password">
          {{ $t('password') }}
        </label>
        <input name="password" v-model="password" :class="[errors.password ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="password"
          type="text" placeholder="••••••••">
        <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
      </div>
      <p class="text-right">
        <button class="cursor-pointer bg-color-button text-color-button rounded focus:outline-none px-4 py-2" type="submit">Passwort ändern</button>
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
        password: false
      },
      password: null,
      response: null,
      showResponse: false,
      classResponse: null
    }
  },
  watch: {
    password: function() {
      if (this.password.trim() !== '') {
        if (this.xxx.test(this.password.trim())) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    }
  },
  middleware: 'notAuthenticated',
  methods: {
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.password) {
        this.errors.password = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$post(`${process.env.API_URL}/auth/reset-password`, {
          password: this.password.trim()
        }).then((res) => {
          this.classResponse = 'text-green-500'
          this.showResponse = true
          this.response = res.message
        }).catch((error) => {
          console.debug(error)
        })
      }
    }
  }
}
</script>
