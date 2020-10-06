<template>
<div v-if="polls">
  <div v-for="outerValue, outerIndex in polls" :key="outerIndex" class="mt-3 px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md mb-8">
    <div v-for="value, index in outerValue" :class="{'mb-6': outerValue.length - index - 1 != 0}" :key="index">
      <h3 class="text-color-form">{{ value.question }}</h3>

      <div v-if="value.type === 'text'">
        <input v-model="polls[outerIndex][index].reply" @input="submitResponse(value._id, outerIndex, index)" type="text"
          class="appearance-none block w-full bg-white text-gray-700 border border-gray-500 rounded p-3 mt-2 leading-tight focus:outline-none">
      </div>

      <div v-if="value.type == 'checkbox'">
        <div v-for="option, i in value.forms" :key="i" class="flex my-2">
          <fa @click="toggleCheckbox(value._id, outerIndex, index, i)" :class="[setCheckboxClass(index, outerIndex, i) ? 'text-green-500' : 'text-gray-500']" :icon="['fas', 'check-square']"
            class="cursor-pointer inline-block text-xl lg:text-2xl w-5 mr-2" />
          <span>{{ option.value }}</span>
        </div>
      </div>

      <div v-if="value.type == 'select'">
        <div class="relative z-0">
          <select v-model="polls[outerIndex][index].reply" @change="submitResponse(value._id, outerIndex, index)" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
            <option v-for="option in value.forms" :value="option.id">{{ option.value }}</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1">
            <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
            </svg>
          </div>
        </div>
      </div>

      <question-charts :values="value.forms" :target="makeId('svg-select', outerIndex, index)" />
    </div>
  </div>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      polls: [],
      stats: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/polls/${this.currentLocale}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        res.data.forEach((values) => {
          const v = values.map((val) => {
            // console.log(formsArray)

            return {
              _id: val._id,
              question: val.question,
              forms: val.forms.map((v) => v),
              reply: val.type !== 'checkbox' && val.reply !== undefined ? val.reply[0] : val.reply,
              type: val.type
            }
          })

          this.polls.push(v)
        })
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    makeId(value, outerIndex, index) {
      return `${value}-${outerIndex}-${index}`
    },
    setCheckboxClass(index, outerIndex, checkboxIndex) {
      const elementId = `option${checkboxIndex}`
      let elementMatch = false

      if (!Array.isArray(this.polls[outerIndex][index].reply)) {
        this.polls[outerIndex][index].reply = []
      }

      if (this.polls[outerIndex][index].reply.includes(elementId)) {
        elementMatch = true
      }

      return elementMatch
    },
    toggleCheckbox(formId, outerIndex, index, checkboxIndex) {
      const elementId = `option${checkboxIndex}`
      let elementMatch = false

      if (this.polls[outerIndex][index].reply.includes(elementId)) {
        elementMatch = true
      }

      if (elementMatch) {
        const elementIndex = this.polls[outerIndex][index].reply.findIndex(e => e === elementId)
        this.polls[outerIndex][index].reply.splice(elementIndex, 1)
        this.submitResponse(formId, outerIndex, index)
      } else {
        this.polls[outerIndex][index].reply.push(elementId)
        this.submitResponse(formId, outerIndex, index)
      }
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
    submitResponse(formId, outerIndex, index) {
      let v = []

      if (Array.isArray(this.polls[outerIndex][index].reply)) {
        v = this.polls[outerIndex][index].reply
      } else {
        v = [this.polls[outerIndex][index].reply]
      }

      const uuid = this.buf2hex(uuidParse(formId))

      this.$axios.$patch(`${process.env.API_URL}/vote/${uuid}`, {
        reply: v
      }).then(res => {
        console.debug(res)
        this.polls[outerIndex][index].reply = res
      }).catch(error => {
        console.debug(error)
      })
    }
  }
}
</script>
