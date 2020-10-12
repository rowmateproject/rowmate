<template>
<form @submit.prevent="submitForm" class="sm:px-3 lg:px-6 sm:pb-3 lg:pb-6 sm:pt-2 lg:pt-4 sm:bg-white sm:rounded sm:shadow">
  <ul v-if="positions.length > 0">
    <li v-for="position, index in positions" :key="index" class="bg-white sm:bg-transparent rounded sm:rounded-0 p-2 sm:p-0 mb-3">
      <position-form @resultObject="handlePositionResult($event, index)" :positionObject="position" />
    </li>
  </ul>

  <div :class="[positions.length === 0 ? 'mt-2' : 'mt-3 lg:mt-6']" class="flex justify-end">
    <button type="button" @click="addPositionForm" class="bg-color-button text-color-button rounded focus:outline-none px-4 py-2">
      Position hinzufügen
    </button>
    <button v-if="positions.length > 0" class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2 ml-3 lg:ml-4">
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
      positions: [],
      organization: {
        _id: ''
      }
    }
  },
  mounted() {
    this.organization = this.$props.organizationObject
    this.positions = this.$props.organizationObject.positions
  },
  props: ['organizationObject'],
  methods: {
    addPositionForm(value) {
      this.positions.push({
        title: '',
        member: ''
      })
    },
    handlePositionResult(value, index) {
      this.positions[index] = value
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
    submitForm() {
      let uuid = null

      try {
        uuid = this.buf2hex(uuidParse(this.organization._id))
      } catch (e) {
        console.debug(e.message)
      }

      this.$axios({
        method: 'PATCH',
        url: `${process.env.API_URL}/organization/${uuid}/positions`,
        data: {
          positions: this.positions
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
</script>
