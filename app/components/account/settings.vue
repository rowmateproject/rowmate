<template>
<div>
  <h3 class="text-gray-700 text-3xl font-semibold">{{ $t('settings') }}</h3>

  <div class="mt-8 p-6 bg-white rounded-md shadow-md">
    <form @submit.prevent="saveExtendedUser">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
        <div>
          <label class="text-gray-700" for="username">{{ $t('name') }}</label>
          <input class="w-full mt-2 rounded border focus:border-blue-550 p-2" type="text" v-model="user.name" />
        </div>

        <div>
          <label class="text-gray-700" for="birthDate">{{ $t('birthDate') }}</label>
          <div class="grid grid-cols-6 gap-3 w-full">
            <select class="col-span-1 mt-2 rounded border focus:border-blue-550 p-2" type="text" v-model="user.birthDate.day">
              <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
            </select>
            <select class="col-span-3 mt-2 rounded border focus:border-blue-550 p-2" type="text" v-model="user.birthDate.month">
              <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
            </select>
            <select class="col-span-2 mt-2 rounded border focus:border-blue-550 p-2" type="text" v-model="user.birthDate.year">
              <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="text-gray-700" for="phoneNumber">{{ $t('phoneNumber') }}</label>
          <input class="w-full mt-2 rounded border focus:border-blue-550 p-2" type="tel" v-model="user.phone" />
        </div>

        <div>
          <label class="text-gray-700" for="mailAddress">{{ $t('mailAddress') }}</label>
          <input class="w-full mt-2 rounded border focus:border-blue-550 p-2" type="email" v-model="user.email" />
        </div>

        <div>
          <label class="text-gray-700" for="password">{{ $t('password') }}</label>
          <input class="w-full mt-2 rounded border focus:border-blue-550 p-2" type="password" v-model="user.password" />
        </div>

        <div>
          <label class="text-gray-700" for="confirmPassword">{{ $t('confirmPassword') }}</label>
          <input class="w-full mt-2 rounded border focus:border-blue-550 p-2" type="password" v-model="user.confirm" />
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
      }
    }
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
    }
  },
  methods: {
    saveExtendedUser() {
      console.log('wurde gepeichert')
    }
  }
}
</script>
