<template>
<div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
  <div class="flex flex-wrap items-stretch w-full relative mt-2">
    <input v-model="searchTerm" @input="lookupQuestion" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border rounded-l focus:outline-none p-2">
    <div class="flex">
      <button @click="clearSearchTerm" class="flex items-center leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded-r px-3" type="button">Zurücksetzen</button>
    </div>
  </div>

  <ul v-if="questions.length > 0" class="w-full absolute z-30 mt-1">
    <li v-for="value, index in questions" @click="setSerchTerm(value)" :key="index" class="hover:bg-gray-300 bg-color-form border shadow p-2">
      <span class="text-color-form">{{ value.question }}</span>
    </li>
  </ul>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      questions: [],
      searchTerm: null
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    availableLocales() {
      return this.$i18n.locales
    }
  },
  props: ['eventSubscriptions'],
  methods: {
    toggleSearch() {
      this.questions = []
    },
    clearSearchTerm() {
      this.searchTerm = ''
      this.$emit('resetFilter', true)
    },
    setSerchTerm(value) {
      try {
        this.searchTerm = value.question
        this.$emit('resultObject', {
          _id: this.buf2hex(uuidParse(value._id)),
          question: value.question,
          forms: value.forms,
          type: value.type
        })
        this.$emit('resetFilter', false)
        this.toggleSearch()
      } catch (e) {
        console.debug(e.message)
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
    lookupQuestion() {
      if (this.searchTerm.length > 0) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/question/${this.currentLocale}`,
          data: {
            query: this.searchTerm
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.questions = res.data
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.questions = []
      }
    }
  }
}
</script>
