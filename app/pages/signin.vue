<template>
<div class="flex items-center justify-center mt-3 mx-3 lg:mx-0 lg:mt-32">
  <form @submit.prevent="loginSubmit" class="bg-white rounded-lg w-full max-w-md p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-3">{{ $t('signin') }}</h1>
    <p v-if="showResponse" class="text-red-500 lg:text-lg mb-3">{{ response }}</p>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
        {{ $t('email') }}
      </label>
      <input name="email" v-model="email" v-bind:class="{'border-red-500': errors.email}"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="email" type="text" placeholder="me@example.com">
      <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="password">
        {{ $t('password') }}
      </label>
      <input name="password" v-model="password" v-bind:class="{'border-red-500': errors.password}" class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white" id="password"
        type="password" placeholder="••••••••">
      <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
    </div>
    <p class="text-right">
      <nuxt-link to="/reset" class="text-blue-400 hover:text-blue-600 focus:outline-none mr-2">{{ $t('forgotPassword') }}</nuxt-link>
      <button class="cursor-pointer bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2" type="submit">{{ $t('signin') }}</button>
    </p>
  </form>
</div>
</template>

<script>
const Cookie = process.client ? require('js-cookie') : undefined

export default {
  data() {
    return {
      errors: {
        email: false,
        password: false
      },
      email: null,
      password: null,
      response: null,
      showResponse: false,
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  computed: {
    hasAdminRole() {
      const roles = this.$store.state.userRoles
      if (Array.isArray(roles)) {
        return roles.includes('admin')
      }
      return false
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
    },
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length >= 5) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    }
  },
  middleware: 'notAuthenticated',
  methods: {
    loginSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.email) {
        this.errors.email = true
      }
      if (!this.password) {
        this.errors.password = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        const formData = new FormData()

        formData.set('username', this.email.trim())
        formData.set('password', this.password.trim())

        this.$axios.$post(`${process.env.API_URL}/auth/jwt/login`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(res => {
          this.$store.commit('updateIsActive', res.is_active)
          this.$store.commit('updateIsConfirmed', res.is_confirmed)
          this.$store.commit('updateIsSuperuser', res.is_superuser)
          this.$store.commit('updateAccessToken', res.access_token)
          this.$store.commit('updateName', res.name)

          Cookie.set('accessToken', res.access_token, {
            samesite: 'None',
            expires: 3600,
            secure: true
          })

          Cookie.set('isActive', res.is_active, {
            samesite: 'None',
            expires: 3600,
            secure: true
          })

          Cookie.set('isConfirmed', res.is_confirmed, {
            samesite: 'None',
            expires: 3600,
            secure: true
          })

          Cookie.set('isSuperuser', res.is_superuser, {
            samesite: 'None',
            expires: 3600,
            secure: true
          })

          Cookie.set('name', res.name, {
            samesite: 'None',
            expires: 3600,
            secure: true
          })

          this.$router.push(this.localePath({
            name: 'dashboard'
          }))
        }).catch(error => {
          this.showResponse = true

          if (error.hasOwnProperty('response')) {
            this.response = error.response.data.detail
          } else {
            this.response = error.message
          }
        })
      }
    }
  }
}
</script>
