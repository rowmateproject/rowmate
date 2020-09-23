<template>
<div>
  <h3 class="text-gray-700 text-3xl font-semibold">{{ $t('settings') }}</h3>

  <div class="mt-8 p-6 bg-white rounded-md shadow-md">
    <form @submit.prevent="saveExtendedUser">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
        <div>
          <label class="text-gray-700" for="username">{{ $t('name') }}</label>
          <input :class="[errors.name ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="text" v-model="user.name">
          <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="birthDate">{{ $t('birthDate') }}</label>
          {{ user.birthDate.day }}  {{ user.birthDate.month }}  {{ user.birthDate.year }}
          <div class="grid grid-cols-6 gap-3 w-full mb-1">
            <select :class="[errors.birthDate.day ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-1 rounded border focus:outline-none p-2 mt-2" type="text" v-model="user.birthDate.day">
              <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
            </select>
            <select :class="[errors.birthDate.month ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-3 rounded border focus:outline-none p-2 mt-2" type="text" v-model="user.birthDate.month">
              <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
            </select>
            <select :class="[errors.birthDate.year ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-2 rounded border focus:outline-none p-2 mt-2" type="text" v-model="user.birthDate.year">
              <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
            </select>
          </div>
          <p v-if="errors.birthDate" class="text-red-500 text-xs italic">{{ $t('errorInvalidBirthDate') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="phoneNumber">{{ $t('phoneNumber') }}</label>
          <input :class="[errors.phone ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="tel" v-model="user.phone">
          <p v-if="errors.phone" class="text-red-500 text-xs italic">{{ $t('errorInvalidPhone') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="mailAddress">{{ $t('mailAddress') }}</label>
          <input :class="[errors.email ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="email" v-model="user.email">
          <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="password">{{ $t('password') }}</label>
          <input :class="[errors.password ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.password">
          <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="confirmPassword">{{ $t('confirmPassword') }}</label>
          <input :class="[errors.confirm ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.confirm">
          <p v-if="errors.confirm" class="text-red-500 text-xs italic">{{ $t('errorInvalidConfirmPassword') }}</p>
        </div>
      </div>

      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-gray-800 text-gray-200 rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
          {{ $t('save') }}
        </button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: '',
        phone: '',
        email: '',
        birthDate: {
          day: null,
          month: null,
          year: null
        },
        password: '',
        confirm: ''
      },
      errors: {
        name: false,
        phone: false,
        email: false,
        birthDate: {
          day: false,
          month: false,
          year: false
        },
        password: false,
        confirm: false
      },
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  mounted() {
    this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

    this.$axios.$get(`${process.env.API_URL}/users/me`).then(res => {
      console.log(res)
      this.user.name = res['name'] || ''
      this.user.phone = res['phone'] || ''
      this.user.email = res['email'] || ''
      this.user.birthDate.day = res['day'] || ''
      this.user.birthDate.month = res['month'] || ''
      this.user.birthDate.year = res['year'] || ''
    }).catch((error) => {
      console.log(error)
    })
  },
  computed: {
    days() {
      return Array(Math.abs(1 - 31) + 1).fill(1).map((v, i) => v + i * (1 > 31 ? -1 : 1))
    },
    months() {
      return ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    },
    years() {
      return Array(Math.abs(1940 - 2020) + 1).fill(1940).map((v, i) => v + i * (1940 > 2020 ? -1 : 1)).reverse()
    },
    birthDate() {
      const d = new Date(this.user.birthDate.year, this.user.birthDate.month - 1, this.user.birthDate.day)
      console.log(d)
      return d
    },
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  watch: {
    'user.email': function() {
      if (this.user.email.trim() !== '') {
        if (this.emailRegex.test(this.user.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    'user.password': function() {
      if (this.user.password.trim() !== '') {
        if (this.user.password.trim().length >= 5) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    },
    'user.confirm': function() {
      if (this.user.confirm.trim() !== '') {
        if (this.user.confirm.trim().length >= 5) {
          this.errors.confirm = false
        } else {
          this.errors.confirm = true
        }
      }
    },
    'user.phone': function() {
      if (this.user.phone.trim() !== '') {
        if (this.user.phone.trim().length >= 7) {
          this.errors.phone = false
        } else {
          this.errors.phone = true
        }
      }
    },
    'user.name': function() {
      if (this.user.name.trim() !== '') {
        if (this.user.name.trim().length >= 2) {
          this.errors.name = false
        } else {
          this.errors.name = true
        }
      }
    }
  },
  methods: {
    saveExtendedUser() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.user.name) {
        this.errors.name = true
      }

      if (!this.user.email) {
        this.errors.email = true
      }

      if (!this.user.phone) {
        this.errors.phone = true
      }

      if (!this.user.password) {
        this.errors.password = true
      }

      if (!this.user.confirm) {
        this.errors.confirm = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

        this.$axios({
          method: 'PATCH',
          url: `${process.env.API_URL}/users/me`,
          data: {
            name: this.user.name.trim(),
            email: this.user.email.trim(),
            password: this.user.password.trim(),
            confirm: this.user.confirm.trim(),
            phone: this.user.phone.trim(),
            birth: this.birthDate
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.classResponse = 'text-green-500'
            this.showResponse = true
            this.response = 'Nutzerkonto wurde erfolgreich angelegt'
          } else if (res.status === 400) {
            this.classResponse = 'text-red-500'
            this.showResponse = true
            this.response = 'Konto mit dieser Email existiert bereits'
          } else if (res.status === 500) {
            this.classResponse = 'text-red-500'
            this.showResponse = true
            this.response = 'Konto mit dieser Email existiert bereits'
          }
        })
      }
    }
  }
}
</script>
