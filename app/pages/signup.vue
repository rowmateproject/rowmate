<template>
<div class="flex items-center justify-center mt-3 mx-3 sm:mt-24 lg:mx-0 lg:mt-48">
  <form @submit.prevent="signupSubmit" class="bg-color-form rounded-lg w-full max-w-md p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-1">{{ $t('signup') }}</h1>
    <p class="text-gray-800 mb-3">{{ $t('rowingTeaser') }}</p>
    <p v-if="showResponse" v-bind:class="classResponse" class="lg:text-lg mb-3">{{ response }}</p>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-color-form text-xs font-bold mb-2" for="name">
        {{ $t('name') }}
      </label>
      <input name="name" v-model="name" v-bind:class="{'border-red-500': errors.name}"
        class="appearance-none block w-full text-color-body border rounded p-3 mb-1 leading-tight focus:outline-none" id="name" type="text" placeholder="Jane Doe">
      <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-color-form text-xs font-bold mb-2" for="email">
        {{ $t('email') }}
      </label>
      <input name="email" v-model="email" v-bind:class="{'border-red-500': errors.email}"
        class="appearance-none block w-full text-color-body border rounded p-3 mb-1 leading-tight focus:outline-none" id="email" type="text" placeholder="me@example.com">
      <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-color-form text-xs font-bold mb-2" for="password">
        {{ $t('password') }}
      </label>
      <input name="password" v-model="password" v-bind:class="{'border-red-500': errors.password}" class="appearance-none block w-full text-color-body border rounded p-3 mb-1 leading-tight focus:outline-none" id="password"
        type="password" placeholder="••••••••">
      <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
    </div>
    <p class="text-right">
      <button class="cursor-pointer bg-color-button focus:outline-none rounded text-color-nav text-sm font-medium tracking-wide p-2" type="submit">{{ $t('signup') }}</button>
    </p>
  </form>
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
  middleware: 'notAuthenticated',
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
