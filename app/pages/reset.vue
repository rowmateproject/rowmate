<template>
<div class="flex items-center justify-center mt-3 mx-3 lg:mx-0 lg:mt-32">
  <form @submit.prevent="resetPasswordSubmit" class="bg-white rounded-lg w-full max-w-md p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-3">{{ $t('resetPassword' )}}</h1>
    <p v-if="showResponse" v-bind:class="classResponse" class="lg:text-lg mb-3">{{ response }}</p>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
        {{ $t('email') }}
      </label>
      <input name="email" v-model="email" v-bind:class="{'border-red-500': errors.email}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="email" type="text" placeholder="me@example.com">
      <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
    </div>
    <p class="text-right">
      <button class="cursor-pointer bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2" type="submit">{{ $t('resetPassword') }}</button>
    </p>
  </form>
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
    resetPasswordSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.email) {
        this.errors.email = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$post(`${process.env.API_URL}/auth/reset`, {
          'email': this.email.trim()
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
