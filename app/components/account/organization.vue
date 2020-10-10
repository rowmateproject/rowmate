<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Organisation</h3>

  <div class="bg-color-image mt-3 lg:mt-8 px-6 pb-6 pt-4 rounded shadow">
    <h4 class="text-xl mb-1">Hinweis</h4>
    <p>Die Angabe des Landes und der genauen Adresse ist wichtig, damit wir den Datenschutz und rechtliche Bestimmungen für dich erfüllen können.</p>
  </div>

  <h4 class="mt-3 lg:mt-8 text-color-form text-2xl font-medium mb-4">Adresse</h4>
  <form @submit.prevent="submitOrganizationForm" class="px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md">
    <div class="mb-4">
      <label class="text-color-form">Länderauswahl</label>
      <div class="relative z-0 mb-1">
        <select v-model="organization.countryCode" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
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
      <p v-if="errors.countryCode" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
    </div>
    <div class="mb-4">
      <label class="text-color-form">Organisation</label>
      <input v-model="organization.name" type="text" :class="[errors.name ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
    </div>
    <div class="grid grid-cols-12 gap-6 mb-4">
      <div class="col-span-10">
        <label class="text-color-form">Straße</label>
        <input v-model="organization.streetName" type="text" :class="[errors.streetName ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.streetName" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
      </div>
      <div class="col-span-2">
        <label class="text-color-form">Hausnummer</label>
        <input v-model="organization.houseNumber" type="text" :class="[errors.houseNumber ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.houseNumber" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
      </div>
    </div>
    <div class="grid grid-cols-12 gap-6">
      <div class="col-span-2">
        <label class="text-color-form">Postleitzahl</label>
        <input v-model="organization.zipCode" type="text" :class="[errors.zipCode ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.zipCode" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
      </div>
      <div class="col-span-10">
        <label class="text-color-form">Ort</label>
        <input v-model="organization.location" type="text" :class="[errors.location ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.location" class="text-red-500 text-xs italic">{{ $t('errorsInvalidName') }}</p>
      </div>
    </div>

    <div class="flex justify-end mt-6">
      <button class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2 ml-4">
        Speichern
      </button>
    </div>
  </form>

  <h4 class="mt-3 lg:mt-8 text-color-form text-2xl font-medium mb-4">Verwaltung</h4>
  <form @submit.prevent="submitManagementForm" class="px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md">
    <div class="grid grid-cols-12 gap-6 mb-4">
      <div class="col-span-6">
        <label class="text-color-form">1. Vorsitzender</label>
        <user-filter @resultObject="handleFirstChairman" @resetFilter="handleFirstChairmanReset" :showResetButton="false" />
      </div>
      <div class="col-span-6">
        <label class="text-color-form">2. Vorsitzender</label>
        <user-filter @resultObject="handleSecondChairman" @resetFilter="handleSecondChairmanReset" :showResetButton="false" />
      </div>
    </div>
    <div class="grid grid-cols-12 gap-6 mb-4">
      <div class="col-span-6">
        <label class="text-color-form">Schriftführer</label>
        <user-filter @resultObject="handleSecretary" @resetFilter="handleSecretaryReset" :showResetButton="false" />
      </div>
      <div class="col-span-6">
        <label class="text-color-form">Kassenwart</label>
        <user-filter @resultObject="handleTreasurer" @resetFilter="handleTreasurerReset" :showResetButton="false" />
      </div>
    </div>
    <div class="grid grid-cols-12 gap-6">
      <div class="col-span-6">
        <label class="text-color-form">Beisitzer</label>
        <user-filter @resultObject="handleAssessor" @resetFilter="handleAssessorReset" :showResetButton="false" />
      </div>
      <div class="col-span-6 flex justify-end items-end">
        <button class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2">
          Speichern
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
      organization: {
        name: null,
        location: null,
        houseNumber: null,
        countryCode: null,
        StreetName: null,
        zipCode: null
      },
      errors: {
        name: false,
        location: false,
        houseNumber: false,
        countryCode: false,
        StreetName: false,
        zipCode: false
      }
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    handleFirstChairman() {
      return true
    },
    handleFirstChairmanReset() {
      return true
    },
    handleSecondChairman() {
      return true
    },
    handleSecondChairmanReset() {
      return true
    },
    handleSecretary() {
      return true
    },
    handleSecretaryReset() {
      return true
    },
    handleTreasurer() {
      return true
    },
    handleTreasurerReset() {
      return true
    },
    handleAssessor() {
      return true
    },
    handleAssessorReset() {
      return true
    },
    submitOrganizationForm() {
      return true
    },
    submitManagementForm() {
      return true
    }
  }
}
</script>
