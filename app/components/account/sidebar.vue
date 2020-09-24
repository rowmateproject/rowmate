<template>
<div class="flex min-h-screen">
  <div class="fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform -translate-x-full ease-in bg-gray-800 overflow-y-auto lg:translate-x-0 lg:static lg:inset-0">
    <div :class="isSuperuser ? 'bg-blue-550' : 'bg-gray-900'" class="text-center py-5">
        <span class="text-white text-3xl mx-2 font-semibold">rowmate.org</span>
    </div>

    <nav class="mt-2">
      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" :to="localePath('/dashboard')" v-if="isSuperuser">
        <fa :icon="['fas', 'chart-line']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Dashboard</span>
      </nuxt-link>

      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('settings') ? activeClass : inactiveClass]" :to="localePath('/settings')">
        <fa :icon="['fas', 'user-cog']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Einstellungen</span>
      </nuxt-link>

      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('users') ? activeClass : inactiveClass]" :to="localePath('/users')">
        <fa :icon="['fas', 'users']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Nutzer</span>
      </nuxt-link>

      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('xxx') ? activeClass : inactiveClass]" :to="localePath('/#')">
        <fa :icon="['fas', 'comment-alt']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Kontakt</span>
      </nuxt-link>

      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('xxx') ? activeClass : inactiveClass]" :to="localePath('/#')">
        <fa :icon="['fas', 'calendar-week']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Termine</span>
      </nuxt-link>

      <nuxt-link class="grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('xxx') ? activeClass : inactiveClass]" :to="localePath('/#')">
        <fa :icon="['fas', 'sticky-note']" class="col-span-1 text-gray-250" />
        <span class="col-span-5">Verwaltung</span>
      </nuxt-link>
    </nav>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      activeClass: 'bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100',
      inactiveClass: 'border-gray-900 text-gray-500 hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100'
    }
  },
  computed: {
    pageName() {
      return this.$route.name
    },
    isSuperuser() {
      return this.$store.state.isSuperuser
    }
  },
  methods: {
    comparePageName(value) {
      return this.pageName === `${value}___${this.$i18n.locale}`
    }
  }
}
</script>
