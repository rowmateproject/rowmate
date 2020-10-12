<template>
<form @submit.prevent="submitForm" class="px-3 lg:px-6 pb-3 lg:pb-6 pt-2 lg:pt-4 bg-color-form rounded shadow">
  <div class="mb-4">
    <label class="text-color-form">Länderauswahl</label>
    <div class="relative z-0 mb-1">
      <select v-model="address.countryCode" :class="[errors.countryCode ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2 mt-2">
        <option value="ch">Schweiz</option>
        <option value="de">Deutschland</option>
        <option value="li">Lichtenstein</option>
        <option value="at">Östereich</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
    <p v-if="errors.countryCode" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
  <div class="mb-4">
    <label class="text-color-form">Organisation</label>
    <input v-model="address.name" type="text" :class="[errors.name ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
    <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
  <div class="grid grid-cols-12 gap-3 lg:gap-6 mb-4">
    <div class="col-span-8 sm:col-span-10">
      <label class="text-color-form">Straße</label>
      <input v-model="address.streetName" type="text" :class="[errors.streetName ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.streetName" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>
    <div class="col-span-4 sm:col-span-2">
      <label class="text-color-form">Haus Nr.</label>
      <input v-model="address.houseNumber" type="text" :class="[errors.houseNumber ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.houseNumber" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>
  </div>
  <div class="grid grid-cols-12 gap-3 lg:gap-6">
    <div class="col-span-4 sm:col-span-2">
      <label class="text-color-form">Postleitzahl</label>
      <input v-model="address.zipCode" type="text" :class="[errors.zipCode ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.zipCode" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>
    <div class="col-span-8 sm:col-span-10">
      <label class="text-color-form">Ort</label>
      <input v-model="address.location" type="text" :class="[errors.location ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.location" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>
  </div>

  <div class="flex justify-end mt-4">
    <button class="bg-blue-600 text-color-nav rounded focus:outline-none px-4 py-2 ml-4">
      {{ $t('save') }}
    </button>
  </div>
</form>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      address: {
        _id: '',
        name: '',
        location: '',
        houseNumber: '',
        countryCode: '',
        streetName: '',
        zipCode: ''
      },
      errors: {
        name: false,
        location: false,
        houseNumber: false,
        countryCode: false,
        streetName: false,
        zipCode: false
      }
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/organization`,
      validateStatus: () => true
    }).then(res => {
      if (res.status === 200) {
        this.address._id = res.data._id || ''
        this.address.zipCode = res.data.zip_code || ''
        this.address.streetName = res.data.street_name || ''
        this.address.houseNumber = res.data.house_number || ''
        this.address.countryCode = res.data.country_code || ''
        this.address.location = res.data.location || ''
        this.address.name = res.data.name || ''

        this.$emit('organizationObject', res.data)
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  watch: {
    'address.location': function() {
      if (this.address.location !== '') {
        if (this.address.location.trim().length >= 2) {
          this.errors.location = false
        } else {
          this.errors.location = true
        }
      } else {
        this.errors.location = false
      }
    },
    'address.name': function() {
      if (this.address.name !== '') {
        if (this.address.name.trim().length >= 2) {
          this.errors.name = false
        } else {
          this.errors.name = true
        }
      } else {
        this.errors.name = false
      }
    },
    'address.houseNumber': function() {
      if (this.address.houseNumber !== '') {
        if (this.address.houseNumber.trim().length >= 1) {
          this.errors.houseNumber = false
        } else {
          this.errors.houseNumber = true
        }
      } else {
        this.errors.houseNumber = false
      }
    },
    'address.countryCode': function() {
      if (this.address.countryCode !== '') {
        if (this.address.countryCode.trim().length >= 1) {
          this.errors.countryCode = false
        } else {
          this.errors.countryCode = true
        }
      } else {
        this.errors.countryCode = false
      }
    },
    'address.streetName': function() {
      if (this.address.streetName !== '') {
        if (this.address.streetName.trim().length >= 1) {
          this.errors.streetName = false
        } else {
          this.errors.streetName = true
        }
      } else {
        this.errors.streetName = false
      }
    },
    'address.zipCode': function() {
      if (this.address.zipCode !== '') {
        if (this.address.zipCode.trim().length >= 4) {
          this.errors.zipCode = false
        } else {
          this.errors.zipCode = true
        }
      } else {
        this.errors.zipCode = false
      }
    }
  },
  methods: {
    buf2hex(buffer) {
      const byteArray = new Uint8Array(buffer)
      const hexParts = []

      for (let i = 0; i < byteArray.length; i++) {
        const hex = byteArray[i].toString(16)
        const paddedHex = ('00' + hex).slice(-2)
        hexParts.push(paddedHex)
      }

      return hexParts.join('')
    },
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.address.name) {
        this.errors.name = true
      }

      if (!this.address.zipCode) {
        this.errors.zipCode = true
      }

      if (!this.address.houseNumber) {
        this.errors.houseNumber = true
      }

      if (!this.address.countryCode) {
        this.errors.countryCode = true
      }

      if (!this.address.streetName) {
        this.errors.streetName = true
      }

      if (!this.address.location) {
        this.errors.location = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        let uuid = null

        try {
          uuid = this.buf2hex(uuidParse(this.address._id))
        } catch (e) {
          console.debug(e.message)
        }

        if (!uuid) {
          this.$axios({
            method: 'POST',
            url: `${process.env.API_URL}/organization`,
            data: {
              name: this.address.name,
              zip_code: this.address.zipCode,
              street_name: this.address.streetName,
              house_number: this.address.houseNumber,
              country_code: this.address.countryCode,
              location: this.address.location
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              this.address._id = res.data || ''
            } else {
              console.debug(res.data)
            }
          })
        } else {
          this.$axios({
            method: 'PATCH',
            url: `${process.env.API_URL}/organization/${uuid}`,
            data: {
              name: this.address.name,
              zip_code: this.address.zipCode,
              street_name: this.address.streetName,
              house_number: this.address.houseNumber,
              country_code: this.address.countryCode,
              location: this.address.location
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status !== 200) {
              console.debug(res.data)
            }
          })
        }
      }
    }
  }
}
</script>
