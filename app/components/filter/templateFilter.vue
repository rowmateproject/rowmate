<template>
<div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
  <div class="flex flex-wrap items-stretch relative w-full mt-2 lg:mt-3">
    <input v-model="searchTerm" @input="lookupTemplate" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border-r-0 rounded md:rounded-r-none md:rounded-l focus:outline-none p-2">
    <button @click="clearSearchTerm" class="w-full md:w-auto leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded md:rounded-l-none md:rounded-r py-2 px-3 mt-2 md:mt-0" type="button">Zurücksetzen</button>
  </div>

  <div v-if="templates.length > 0" class="w-full absolute z-30">
    <div @click="setSerchTerm(template)" v-for="template in templates" class="hover:bg-gray-300 bg-color-form border shadow p-1">
      <span class="leading-5 font-medium text-gray-900">{{ template.subject }}</span>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      templates: [],
      searchTerm: null
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    toggleSearch() {
      this.templates = []
    },
    setSerchTerm(value) {
      this.searchTerm = value.name
      this.$emit('resultObject', {
        template: value
      })
      this.toggleSearch()
    },
    clearSearchTerm() {
      this.searchTerm = ''
      this.$emit('resetFilter', true)
    },
    lookupTemplate() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/template/${this.currentLocale}`,
          data: {
            query: this.searchTerm
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.templates = res.data || []
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.templates = []
      }
    }
  }
}
</script>
