<template>
<ul v-if="polls">
  <li v-for="value, index in polls" :class="{'mb-6': polls.length - index - 1 != 0}" :key="index" class="mt-3 px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md mb-8">
    <h3 class="text-color-form">{{ value.question }}</h3>

    <div v-if="value.type === 'text'">
      <input v-model="polls[index].reply" @input="submitResponse(value._id, index)" type="text" class="appearance-none block w-full bg-white text-gray-700 border border-gray-500 rounded p-3 mt-2 leading-tight focus:outline-none">
    </div>

    <div v-if="value.type == 'checkbox'">
      <div v-for="option, idx in value.forms" :key="idx" class="flex my-2">
        <fa @click="toggleCheckbox(value._id, option.id, index)" :class="[setCheckboxClass(option.id, index) ? 'text-green-500' : 'text-gray-500']" :icon="['fas', 'check-square']" class="cursor-pointer inline-block text-xl lg:text-2xl w-5 mr-2" />
        <span>{{ option.value }}</span>
      </div>
    </div>

    <div v-if="value.type == 'select'">
      <div class="relative z-0">
        <select v-model="polls[index].reply" @change="submitResponse(value._id, index)" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
          <option v-for="option in value.forms" :value="option.id">{{ option.value }}</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1">
          <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>
    </div>
  </li>
</ul>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      polls: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/polls/${this.currentLocale}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.polls = res.data
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    makeId(value, index) {
      return `${value}-$-${index}`
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
    setCheckboxClass(optionId, index) {
      return this.polls[index].reply.includes(optionId)
    },
    toggleCheckbox(formId, optionId, index) {
      if (this.polls[index].reply.includes(optionId)) {
        const elementIndex = this.polls[index].reply.findIndex(e => e === optionId)
        this.polls[index].reply.splice(elementIndex, 1)
      } else {
        this.polls[index].reply.push(optionId)
      }

      this.submitResponse(formId, index)
    },
    submitResponse(formId, index) {
      let v = []

      if (Array.isArray(this.polls[index].reply)) {
        v = this.polls[index].reply
      } else {
        v = [this.polls[index].reply]
      }

      const uuid = this.buf2hex(uuidParse(formId))

      this.$axios.$patch(`${process.env.API_URL}/vote/${uuid}`, {
        reply: v
      }).then(res => {
        if (Array.isArray(res)) {
          this.polls[index].reply = res
        } else {
          this.polls[index].reply = [res]
        }

        console.log(this.polls[index].reply)
      }).catch(error => {
        console.debug(error)
      })
    }
  }
}
</script>
