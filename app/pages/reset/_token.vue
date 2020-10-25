<template>
<div class="flex flex-col min-h-screen">
  <div class="flex-grow flex flex-col items-center justify-center p-3 lg:p-0">
    <img src="/rowmate_without_margins.png" class="w-full max-w-md px-3 pb-3 lg:px-6 lg:pb-6" />
    <form @submit.prevent="submitForm" class="bg-color-form rounded-lg w-full max-w-md p-3 lg:p-6">
      <h1 class="text-2xl lg:text-4xl leading-none font-medium mb-3">Passwort ändern</h1>
      <p class="text-lg w-full lg:w-11/12">Um Dein aktuelles Passwort zurückzusetzen, gebe ein starkes Passwort ein und bestätige das Passwort nochmals. Anschließend wirst Du zur <nuxt-link to="/signin" class="text-blue-600 hover:text-blue-800">
          Anmeldeseite</nuxt-link> weitergeleitet.</p>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="password">
          {{ $t('password') }}
        </label>
        <input name="password" v-model="password" :class="[errors.password ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="password"
          type="password" placeholder="••••••••">
        <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
      </div>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="confirm">
          {{ $t('confirmPassword') }}
        </label>
        <input name="confirm" v-model="confirm" :class="[errors.confirm ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="confirm"
          type="password" placeholder="••••••••">
        <p v-if="errors.confirm" class="text-red-500 text-xs italic">{{ $t('errorInvalidConfirmPassword') }}</p>
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
      confirm: '',
      password: '',
      errors: {
        confirm: false,
        password: false
      }
    }
  },
  watch: {
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length >= 5) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }

      if (this.confirm.trim() !== '') {
        if (this.confirm.trim() === this.password.trim()) {
          this.errors.confirm = false
        } else {
          this.errors.confirm = true
        }
      }
    },
    confirm: function() {
      if (this.confirm.trim() !== '') {
        if (this.confirm.trim() === this.password.trim()) {
          this.errors.confirm = false
        } else {
          this.errors.confirm = true
        }
      }
    }
  },
  middleware: 'authenticated',
  methods: {
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.confirm) {
        this.errors.confirm = true
      }

      if (!this.password) {
        this.errors.password = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/auth/reset-password`,
          data: {
            token: this.$route.params.token,
            password: this.password.trim()
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.$router.push(this.localePath({
              name: 'signin'
            }))
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
