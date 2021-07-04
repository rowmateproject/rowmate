<template>
<header class="hidden sm:flex justify-between items-center bg-color-form border-b-4 border-blue-550 h-16 lg:h-20 px-3 py-3 lg:px-6">
  <div class="w-full flex justify-between items-center">
    <div class="w-full md:w-6/12 lg:w-5/12 xl:w-3/12 relative">
      <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
        <input v-model="searchTerm" @input="lookupSearchTerm" type="text" class="w-full rounded border focus:outline-none p-2" placeholder="Nutzer suchen">

        <div v-if="users.length > 0" class="w-full absolute z-30">
          <div @click="setSerchTerm(user)" class="hover:bg-gray-300 bg-color-form border shadow p-1" v-for="user in users">
            <avatar class="inline mr-2 pr-2" width="75" :avatar="user.avatar" />
            <span class="leading-5 font-medium text-gray-900">{{ user.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="hidden sm:block relative ml-3">
      <div @click="toggleDropdown" class="focus:outline-none overflow-hidden cursor-pointer h-10 lg:h-12 w-10 lg:w-12">
        <avatar :avatar="avatar" class="h-full w-full object-cover" />
      </div>

      <ul v-click-outside="hideDropdown" v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-color-nav overflow-hidden rounded shadow z-20">
        <li @click="toggleDropdown">
          <nuxt-link :to="localePath('/settings')" class="block px-4 py-2 text-sm text-color-nav hover:bg-gray-800 border-b border-color-form">Profile</nuxt-link>
        </li>
        <li @click="toggleDropdown" v-for="locale in availableLocales">
          <a @click="$i18n.setLocale(locale.code)" class="cursor-pointer block px-4 py-2 text-sm text-color-nav hover:bg-gray-800 border-b border-color-form">{{ locale.name }}</a>
        </li>
        <li @click="toggleDropdown">
          <a @click="logoutUser" class="cursor-pointer block px-4 py-2 text-sm text-color-nav hover:bg-gray-800">Logout</a>
        </li>
      </ul>
    </div>
  </div>
</header>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      searchTerm: '',
      users: []
    }
  },
  computed: {
    avatar() {
      return {
        eyeType: this.$store.state.eyeType,
        clotheType: this.$store.state.clotheType,
        circleColor: this.$store.state.circleColor,
        accessoriesType: this.$store.state.accessoriesType,
        facialHairColor: this.$store.state.facialHairColor,
        facialHairType: this.$store.state.facialHairType,
        clotheColor: this.$store.state.clotheColor,
        eyebrowType: this.$store.state.eyebrowType,
        graphicType: this.$store.state.graphicType,
        hairColor: this.$store.state.hairColor,
        mouthType: this.$store.state.mouthType,
        skinColor: this.$store.state.skinColor,
        topColor: this.$store.state.topColor,
        topType: this.$store.state.topType
      }
    },
    availableLocales() {
      return this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
    }
  },
  methods: {
    toggleSearch() {
      this.users = []
    },
    setSerchTerm(user) {
      this.searchTerm = user.name
      this.toggleSearch()
    },
    hideDropdown() {
      return this.showDropdown = false
    },
    toggleDropdown() {
      return this.showDropdown = !this.showDropdown
    },
    lookupSearchTerm() {
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
    },
    logoutUser() {
      this.$logout()
    }
  }
}
</script>
