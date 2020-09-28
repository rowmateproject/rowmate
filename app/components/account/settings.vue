<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Profile</h3>

  <form @submit.prevent="saveExtendedUser">
    <div class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
      <div class="grid grid-cols-6 gap-6">
        <div class="col-span-6 sm:col-span-2 sm:pr-6 sm:border-r-2">
          <avatar :avatar="user.avatar" />

          <div class="text-center mt-8">
            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
              <input type="checkbox" name="toggle" id="toggle" class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-color-form border-4 appearance-none cursor-pointer" />
              <label for="toggle" class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
            </div>
            <label for="toggle" class="text-xs text-color-form">Use avatar</label>
          </div>
        </div>

        <ul class="col-span-6 sm:col-span-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <feature @data="updateEyeType" :value="user.avatar.eyeType" param="eyeType" />
          <feature @data="updateEyebrowType" :value="user.avatar.eyebrowType" param="eyebrowType" />
          <feature @data="updateAccessoriesType" :value="user.avatar.accessoriesType" param="accessoriesType" />
          <feature @data="updateMouthType" :value="user.avatar.mouthType" param="mouthType" />
          <feature @data="updateFacialHairType" :value="user.avatar.facialHairType" param="facialHairType" />
          <feature @data="updateFacialHairColor" :value="user.avatar.facialHairColor" param="facialHairColor" />
          <feature @data="updateSkinColor" :value="user.avatar.skinColor" param="skinColor" />
          <feature @data="updateFopType" :value="user.avatar.topType" param="topType" />
          <feature @data="updateHairColor" :value="user.avatar.hairColor" param="hairColor" />
          <feature @data="updateTopColor" :value="user.avatar.topColor" param="topColor" />
          <feature @data="updateClotheType" :value="user.avatar.clotheType" param="clotheType" />
          <feature @data="updateGraphicType" :value="user.avatar.graphicType" param="graphicType" />
          <feature @data="updateClotheColor" :value="user.avatar.clotheColor" param="clotheColor" />
          <feature @data="updateCircleColor" :value="user.avatar.circleColor" param="circleColor" />
        </ul>
      </div>
    </div>

    <div class="mt-3 lg:mt-8 p-6 bg-color-form rounded-md shadow-md">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
        <div>
          <label class="text-color-form" for="username">{{ $t('name') }}</label>
          <input :class="[errors.name ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1" type="text" v-model="user.name">
          <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="birthDate">{{ $t('birthDate') }}</label>
          <div class="grid grid-cols-6 gap-3 w-full mb-1">
            <div class="col-span-1 relative z-0">
              <select :class="[errors.birthDate.day ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2" v-model="user.birthDate.day">
                <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
                <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>
            <div class="col-span-3 relative z-0">
              <select :class="[errors.birthDate.month ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2" v-model="user.birthDate.month">
                <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
                <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>
            <div class="col-span-2 relative z-0">
              <select :class="[errors.birthDate.year ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2" v-model="user.birthDate.year">
                <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
                <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>
          </div>
          <p v-if="errors.birthDate" class="text-red-500 text-xs italic">{{ $t('errorInvalidBirthDate') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="phoneNumber">{{ $t('phoneNumber') }}</label>
          <input :class="[errors.phone ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1" type="tel" v-model="user.phone">
          <p v-if="errors.phone" class="text-red-500 text-xs italic">{{ $t('errorInvalidPhone') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="mailAddress">{{ $t('mailAddress') }}</label>
          <input :class="[errors.email ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1" type="email" v-model="user.email">
          <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="password">{{ $t('password') }}</label>
          <input :class="[errors.password ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.password">
          <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="confirmPassword">{{ $t('confirmPassword') }}</label>
          <input :class="[errors.confirm ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.confirm">
          <p v-if="errors.confirm" class="text-red-500 text-xs italic">{{ $t('errorInvalidConfirmPassword') }}</p>
        </div>

        <div>
          <label class="text-color-form" for="confirmPassword">Sprachauswahl</label>
          <div class="col-span-3 relative z-0">
            <select v-model="user.locale" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
              <option v-for="value, index in availableLocales" :key="index" :value="value.code">{{ value.name }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
              <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
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
      user: {
        avatar: {},
        name: '',
        phone: '',
        email: '',
        locale: '',
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
        birthDate: false,
        password: false,
        confirm: false
      },
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/users/me`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.user.name = res.data.name || ''
        this.user.email = res.data.email || ''
        this.user.phone = res.data.phone || ''
        this.user.avatar = res.data.avatar || {}
        this.user.locale = this.currentLocale || res.data.locale
        this.user.birthDate.day = new Date(Date.parse(res.data.birth)).getDate() || ''
        this.user.birthDate.month = new Date(Date.parse(res.data.birth)).getMonth() + 1 || ''
        this.user.birthDate.year = new Date(Date.parse(res.data.birth)).getFullYear() || ''
      } else {
        console.debug(res.data)
      }
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
      return new Date(Date.UTC(this.user.birthDate.year, this.user.birthDate.month - 1, this.user.birthDate.day, 0, 0, 0))
    },
    currentLocale() {
      return this.$i18n.locale
    },
    availableLocales() {
      return this.$i18n.locales
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
      if (this.user.confirm.trim() !== '') {
        if (this.user.confirm.trim() === this.user.password.trim()) {
          this.errors.confirm = false
        } else {
          this.errors.confirm = true
        }
      }
    },
    'user.confirm': function() {
      if (this.user.confirm.trim() !== '') {
        if (this.user.confirm.trim() === this.user.password.trim()) {
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
    },
    'user.birthDate.day': function() {
      if (this.user.birthDate.day !== null) {
        if (this.user.birthDate.day >= 0 && this.user.birthDate.day <= 31) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    },
    'user.birthDate.month': function() {
      if (this.user.birthDate.month !== null) {
        if (this.user.birthDate.month >= 1 && this.user.birthDate.month <= 12) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    },
    'user.birthDate.year': function() {
      if (this.user.birthDate.year !== null) {
        if (this.user.birthDate.year >= 1940 && this.user.birthDate.year <= 2020) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    }
  },
  methods: {
    updateEyeType(value) {
      this.user.avatar.eyeType = value
    },
    updateEyebrowType(value) {
      this.user.avatar.eyebrowType = value
    },
    updateAccessoriesType(value) {
      this.user.avatar.accessoriesType = value
    },
    updateMouthType(value) {
      this.user.avatar.mouthType = value
    },
    updateSkinColor(value) {
      this.user.avatar.skinColor = value
    },
    updateFacialHairType(value) {
      this.user.avatar.facialHairType = value
    },
    updateFacialHairColor(value) {
      this.user.avatar.facialHairColor = value
    },
    updateFopType(value) {
      this.user.avatar.topType = value
    },
    updateHairColor(value) {
      this.user.avatar.hairColor = value
    },
    updateTopColor(value) {
      this.user.avatar.topColor = value
    },
    updateClotheType(value) {
      this.user.avatar.clotheType = value
    },
    updateGraphicType(value) {
      this.user.avatar.graphicType = value
    },
    updateClotheColor(value) {
      this.user.avatar.clotheColor = value
    },
    updateCircleColor(value) {
      this.user.avatar.circleColor = value
    },
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

      if (this.user.confirm !== this.user.password) {
        this.errors.confirm = true
      }

      if (this.user.birthDate.day <= 0 && this.user.birthDate.day >= 31) {
        this.errors.birthDate = true
      }

      if (this.user.birthDate.month <= 1 && this.user.birthDate.month >= 12) {
        this.errors.birthDate = true
      }

      if (this.user.birthDate.year <= 1940 && this.user.birthDate.year >= 2020) {
        this.errors.birthDate = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios({
          method: 'PATCH',
          url: `${process.env.API_URL}/users/me`,
          data: {
            name: this.user.name.trim(),
            email: this.user.email.trim(),
            password: this.user.password.trim(),
            confirm: this.user.confirm.trim(),
            phone: this.user.phone.trim(),
            locale: this.user.locale,
            avatar: this.user.avatar,
            birth: this.birthDate
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            if (this.currentLocale !== this.user.locale) {
              this.$i18n.setLocale(this.user.locale)
            }

            this.classResponse = 'text-green-500'
            this.showResponse = true
            this.response = 'Einstellungen wurden erfolgreich geändert'
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>

<style>
.toggle-checkbox:checked {
  @apply: right-0 border-green-400;
  border-color: #68D391;
  right: 0;
}

.toggle-checkbox:checked+.toggle-label {
  background-color: #68D391;
  @apply: bg-green-400;
}
</style>
