<template>
<div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
  <input v-if="!resetButton" v-model="searchTerm" @input="lookupBoat" type="text" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2">
  <div v-else class="flex flex-wrap items-stretch w-full relative mt-2">
    <input v-model="searchTerm" @input="lookupBoat" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border-l border-t border-b border-color-form rounded-l focus:outline-none p-2">
    <div class="flex">
      <button @click="clearSearchTerm" class="flex items-center leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded-r px-3" type="button">Zurücksetzen</button>
    </div>
  </div>

  <div v-if="boats.length > 0" class="w-full absolute z-30">
    <div @click="setSerchTerm(boat)" class="hover:bg-gray-300 bg-color-form border shadow p-1" v-for="boat in boats">
      <span class="leading-5 font-medium text-gray-900">{{ boat.name }}</span>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      boats: [],
      searchTerm: ''
    }
  },
  mounted() {
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    availableLocales() {
      return this.$i18n.locales
    },
    resetButton() {
      return this.$props.showResetButton
    }
  },
  watch: {
    searchQuery: function(value) {
      this.searchTerm = value
    }
  },
  props: ['searchQuery', 'showResetButton'],
  methods: {
    toggleSearch() {
      this.boats = []
    },
    clearSearchTerm() {
      this.searchTerm = ''
      this.$emit('resetFilter', true)
    },
    setSerchTerm(value) {
      if (this.searchQueryTerm) {
        this.searchTerm = this.searchQueryTerm
      } else {
        this.searchTerm = value.name
      }

      this.$emit('resultObject', {
        boat: value
      })

      this.toggleSearch()
    },
    lookupBoat() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/boats`,
          data: {
            name: this.searchTerm
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.boats = res.data || []
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.boats = []
      }
    }
  }
}
</script>
