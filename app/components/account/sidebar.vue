<template>
<div class="flex min-h-screen">
  <div class="bg-color-nav fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform -translate-x-full ease-in overflow-y-auto lg:translate-x-0 lg:static lg:inset-0">
    <div class="bg-color-header text-center py-5">
      <span class="text-color-nav text-3xl mx-2 font-semibold">rowmate.org</span>
    </div>

    <nav class="mt-8">
      <nuxt-link v-if="isSuperuser === 'true'" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" :to="localePath('/dashboard')">
        <fa :icon="['fas', 'chart-line']" class="col-span-1" />
        <span class="col-span-5">Dashboard</span>
      </nuxt-link>

      <nuxt-link class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('settings') ? activeClass : inactiveClass]" :to="localePath('/settings')">
        <fa :icon="['fas', 'user-cog']" class="col-span-1" />
        <span class="col-span-5">Profile</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true'" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('users') ? activeClass : inactiveClass]" :to="localePath('/users')">
        <fa :icon="['fas', 'users']" class="col-span-1" />
        <span class="col-span-5">Nutzer</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true'" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('theme') ? activeClass : inactiveClass]" :to="localePath('/theme')">
        <fa :icon="['fas', 'comment-alt']" class="col-span-1" />
        <span class="col-span-5">Theme</span>
      </nuxt-link>

      <nuxt-link class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('xxx') ? activeClass : inactiveClass]" :to="localePath('/#')">
        <fa :icon="['fas', 'calendar-week']" class="col-span-1" />
        <span class="col-span-5">Termine</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true'" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('event') ? activeClass : inactiveClass]" :to="localePath('/event')">
        <fa :icon="['fas', 'sticky-note']" class="col-span-1" />
        <span class="col-span-5">Event</span>
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
      inactiveClass: 'border-gray-900 text-color-nav hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100'
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
