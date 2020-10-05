<template>
<div class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow">
  <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
    <label class="text-color-form" for="eventFilter">Umfrage Filter</label>

    <div class="flex flex-wrap items-stretch w-full relative mt-2">
      <input v-model="searchTerm" @input="lookupEvent" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border rounded-l focus:outline-none p-2">
      <div class="flex">
        <button @click="clearSearchTerm" class="flex items-center leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded-r px-3">Zurücksetzen</button>
      </div>
    </div>

    <ul v-if="polls.length > 0" class="w-full absolute z-30 mt-1">
      <li v-for="value, index in polls" @click="setSerchTerm(value.question, index)" :key="index" class="hover:bg-gray-300 bg-color-form border shadow p-2">
        <span class="text-color-form">{{ value.question }}</span>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      polls: [],
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
      this.polls = []
    },
    clearSearchTerm() {
      this.searchTerm = ''
      this.$emit('resetFilter', true)
    },
    setSerchTerm(value, index) {
      console.log(value)
      this.searchTerm = `${value}`
      this.$emit('resultObject', this.polls[index])
      this.$emit('resetFilter', false)
      this.toggleSearch()
    },
    lookupEvent() {
      if (this.searchTerm.length > 0) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/polls/${this.currentLocale}`,
          data: {
            query: this.searchTerm
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.polls = res.data
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.polls = []
      }
    }
  }
}
</script>
