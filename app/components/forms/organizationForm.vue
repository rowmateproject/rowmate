<template>
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
        {{ $t('save') }}
      </button>
    </div>
  </div>
</form>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {}
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
    submitManagementForm() {
      return true
    }
  }
}
</script>
