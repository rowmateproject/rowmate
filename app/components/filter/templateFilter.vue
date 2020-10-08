<template>
<div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
  <div class="flex flex-wrap items-stretch w-full relative mt-2">
    <input v-model="searchTerm" @input="lookupTemplate" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border rounded-l focus:outline-none p-2">
    <div class="flex">
      <button @click="clearSearchTerm" class="flex items-center leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded-r px-3" type="button">Zurücksetzen</button>
    </div>
  </div>

  <div v-if="templates.length > 0" class="w-full absolute z-30">
    <div @click="setSerchTerm(template)" class="hover:bg-gray-300 bg-color-form border shadow p-1" v-for="template in templates">
      <span class="leading-5 font-medium text-gray-900">{{ template.name }}</span>
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
        template: value.name
      })
      this.toggleSearch()
    },
    lookupTemplate() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/templates`,
          data: {
            name: this.searchTerm
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
