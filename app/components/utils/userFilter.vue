<template>
<div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
  <input v-model="searchTerm" @input="lookupUser" type="text" class="w-full rounded border focus:outline-none p-2 mt-2">

  <div v-if="users.length > 0" class="w-full absolute z-30">
    <div @click="setSerchTerm(user)" class="hover:bg-gray-300 bg-color-form border shadow p-1" v-for="user in users">
      <avatar class="inline mr-2 pr-2" width="75" :avatar="user.avatar" />
      <span class="leading-5 font-medium text-gray-900">{{ user.name }}</span>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
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
      this.users = []
    },
    setSerchTerm(value) {
      this.searchTerm = value.name
      this.$emit('resultObject', {
        user: value.name
      })
      this.toggleSearch()
    },
    lookupUser() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/users`,
          data: {
            name: this.searchTerm
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.users = res.data || []
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.users = []
      }
    }
  }
}
</script>
