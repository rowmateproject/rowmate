<template>
<div class="flex flex-col min-h-screen">
  <div class="flex-grow flex flex-col items-center justify-center p-3 lg:p-0">
    <img src="/rowmate_without_margins.png" class="w-full max-w-md px-3 pb-3 lg:px-6 lg:pb-6" />
    <form @submit.prevent="signupSubmit" class="bg-color-form rounded-lg w-full max-w-md p-3 lg:p-6">
      <h1 class="text-2xl lg:text-4xl font-medium mb-1">{{ $t('signup') }}</h1>
      <p class="text-gray-800 text-lg mb-3">{{ $t('rowingTeaser') }}</p>
      <p v-if="showResponse" :class="classResponse" class="lg:text-lg mb-3">{{ response }}</p>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="name">
          {{ $t('name') }}
        </label>
        <input name="name" v-model="name" :class="[errors.name ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="name" type="text"
          placeholder="Jane Doe">
        <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
      </div>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="email">
          {{ $t('email') }}
        </label>
        <input name="email" v-model="email" :class="[errors.email ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="email" type="text"
          placeholder="me@example.com">
        <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
      </div>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="password">
          {{ $t('password') }}
        </label>
        <input name="password" v-model="password" :class="[errors.password ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="password"
          type="password" placeholder="••••••••">
        <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
      </div>
      <p class="flex justify-end">
        <google-button />
        <button class="cursor-pointer bg-color-button text-color-button rounded focus:outline-none px-4 py-2" type="submit">{{ $t('signup') }}</button>
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
        name: false,
        email: false,
        password: false
      },
      name: null,
      email: null,
      password: null,
      response: null,
      showResponse: false,
      classResponse: null,
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  watch: {
    name: function() {
      if (this.name.trim() !== '') {
        if (this.name.trim().length > 2) {
          this.errors.name = false
        } else {
          this.errors.name = true
        }
      }
    },
    email: function() {
      if (this.email.trim() !== '') {
        if (this.emailRegex.test(this.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length > 2) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    }
  },
  middleware: 'authenticated',
  methods: {
    signupSubmit() {
      const isValidForm = (currentValue) => currentValue !== true
      if (!this.name) {
        this.errors.name = true
      }
      if (!this.email) {
        this.errors.email = true
      }
      if (!this.password) {
        this.errors.password = true
      }
      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/auth/register`,
          data: {
            name: this.name.trim(),
            email: this.email.trim(),
            password: this.password.trim()
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 201) {
            this.classResponse = 'text-green-500'
            this.showResponse = true
            this.response = 'Nutzerkonto wurde erfolgreich angelegt'
          } else if (res.status === 400) {
            this.classResponse = 'text-red-500'
            this.showResponse = true
            this.response = 'Konto mit dieser Email existiert bereits'
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
