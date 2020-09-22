<template>
<div v-click-outside="hideNav" class="fixed z-50 w-full bg-gray-900 mb-3 lg:mb-8">
  <div class="container mx-auto">
    <header class="flex flex-wrap items-center">
      <div class="flex-1 flex justify-between items-center py-2 pl-3 lg:pl-0">
        <nuxt-link v-if="!userId" :to="localePath('/')" class="flex justify-between focus:outline-none text-lg font-bold">
          <span class="text-2xl text-gray-300 hover:text-white font-light">rowmate.org</span>
        </nuxt-link>
      </div>

      <label @click="toggleNav" class="cursor-pointer lg:hidden block py-2 pr-4">
        <svg class="w-5 h-5 text-gray-500 hover:text-white focus:outline-none fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path>
        </svg>
      </label>

      <div v-bind:class="[showNav ? 'block z-50' : 'hidden']" class="w-full border-t lg:border-0 border-gray-800 mt-2 lg:mt-0 lg:flex lg:items-center lg:w-auto">
        <ul class="lg:flex items-center justify-between text-base text-white pt-0 lg:pt-0">
          <li v-if="!userId" @click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link :to="localePath('/signin')" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">{{ $t('signin') }}</nuxt-link>
          </li>
          <li v-if="!userId" @click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link :to="localePath('/signup')" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">{{ $t('signup') }}</nuxt-link>
          </li>

          <li v-click-outside="hideDropdown" v-if="userId" class="relative border-b lg:border-b-2 border-gray-800">
            <button @click="toggleDropdown" class="hidden lg:flex items-center cursor-pointer block py-3 px-3 lg:py-4 lg:pl-4 lg:pr-0 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">
              <span class="pr-1 flex-1">{{ $t('more') }}</span>
              <svg class="fill-current h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
              </svg>
            </button>
            <ul v-bind:class="[showDropdown ? 'block z-50' : 'lg:hidden']" class="relative lg:absolute top right-0 lg:bg-gray-700 shadow w-full lg:w-48">
              <!--<li @click="toggleNav" v-for="locale in availableLocales" class="border-b lg:border-b-0 border-gray-800 lg:border-transparent lg:hover:border-white">
                <a @click="$i18n.setLocale(locale.code)" class="cursor-pointer block py-3 px-3 lg:p-3 focus:outline-none hover:bg-gray-800 lg:hover:bg-gray-200 lg:hover:text-gray-700">{{ locale.name }}</a>
              </li>-->
              <li v-if="userId && hasAdminRole" @click="toggleDropdown" class="border-b lg:border-b-0 border-gray-800 lg:border-transparent lg:hover:border-white">
                <nuxt-link :to="localePath('/admin/templates')" class="block py-3 px-3 lg:p-3 focus:outline-none hover:bg-gray-800 lg:hover:bg-gray-200 lg:hover:text-gray-700">Templates</nuxt-link>
              </li>
              <li v-if="userId && hasAdminRole" @click="toggleDropdown" class="border-b lg:border-b-0 border-gray-800 lg:border-transparent lg:hover:border-white">
                <nuxt-link :to="localePath('/admin/users')" class="block py-3 px-3 lg:p-3 focus:outline-none hover:bg-gray-800 lg:hover:bg-gray-200 lg:hover:text-gray-700">Nutzerverwaltung</nuxt-link>
              </li>
              <li v-if="userId" @click="toggleDropdown" class="border-b lg:border-b-0 border-gray-800 lg:border-transparent lg:hover:border-white">
                <nuxt-link :to="localePath('/account/settings')" class="block py-3 px-3 lg:p-3 focus:outline-none hover:bg-gray-800 lg:hover:bg-gray-200 lg:hover:text-gray-700">Einstellungen</nuxt-link>
              </li>
              <li v-if="userId" @click="toggleDropdown" class="border-b lg:border-b-0 border-gray-800 lg:border-transparent lg:hover:border-white">
                <a @click="logoutSubmit" class="cursor-pointer block py-3 px-3 lg:p-3 focus:outline-none hover:bg-gray-800 lg:hover:bg-gray-200 lg:hover:text-gray-700">{{ $t('logout')}}</a>
              </li>
            </ul>
          </li>

        </ul>
      </div>
    </header>
  </div>
</div>
</template>

<script>
const Cookie = require('js-cookie')

export default {
  data() {
    return {
      showNav: false,
      showDropdown: false
    }
  },
  computed: {
    userId() {
      return this.$store.state.userId
    },
    hasAdminRole() {
      const roles = this.$store.state.userRoles

      if (Array.isArray(roles)) {
        return roles.includes('admin')
      }

      return false
    },
    hasUserRole() {
      const roles = this.$store.state.userRoles

      if (Array.isArray(roles)) {
        return roles.includes('user')
      }

      return false
    },
    availableLocales() {
      return this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
    }
  },
  methods: {
    hideNav() {
      return this.showNav = false
    },
    hideDropdown() {
      return this.showDropdown = false
    },
    toggleNav() {
      return this.showNav = !this.showNav
    },
    toggleDropdown() {
      this.toggleNav()
      return this.showDropdown = !this.showDropdown
    },
  }
}
</script>
