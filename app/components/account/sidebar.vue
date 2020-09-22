<template>
<div class="flex min-h-screen">
  <div :class="isOpen ? 'block' : 'hidden'" @click="isOpen = false" class="fixed z-20 inset-0 bg-black opacity-50 transition-opacity lg:hidden"></div>

  <div :class="isOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in'" class="fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform bg-gray-800 overflow-y-auto lg:translate-x-0 lg:static lg:inset-0">
    <div class="flex items-center justify-center bg-gray-900 pt-6 pb-6">
      <div class="flex items-center">
        <fa :icon="['fas', 'id-card']" class="text-gray-250 text-2xl" />
        <span class="text-white text-2xl mx-2 font-semibold">rowmate.org</span>
      </div>
    </div>

    <nav class="mt-2">
      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'dashboard' ? activeClass : inactiveClass]" :to="localePath('/dashboard')">
        <fa :icon="['fas', 'chart-line']" class="text-gray-250" />

        <span class="mx-4">Dashboard</span>
      </nuxt-link>

      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'UIElements' ? activeClass : inactiveClass]" :to="localePath('/settings')">
        <fa :icon="['fas', 'server']" class="text-gray-250" />

        <span class="mx-4">Einstellungen</span>
      </nuxt-link>

      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'Tables' ? activeClass : inactiveClass]" :to="localePath('#')">
        <fa :icon="['fas', 'table']" class="text-gray-250" />

        <span class="mx-4">Informationen</span>
      </nuxt-link>

      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'Forms' ? activeClass : inactiveClass]" :to="localePath('#')">
        <fa :icon="['fas', 'comment-alt']" class="text-gray-250" />

        <span class="mx-4">Kontakt</span>
      </nuxt-link>

      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'Modal' ? activeClass : inactiveClass]" :to="localePath('#')">
        <fa :icon="['fas', 'calendar-week']" class="text-gray-250" />

        <span class="mx-4">Termine</span>
      </nuxt-link>

      <nuxt-link class="flex items-center mt-2 py-3 px-6" :class="[$route.name === 'Blank' ? activeClass : inactiveClass]" :to="localePath('#')">
        <fa :icon="['fas', 'sticky-note']" class="text-gray-250" />

        <span class="mx-4">Verwaltung</span>
      </nuxt-link>
    </nav>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      isOpen: true,
      activeClass: 'bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100',
      inactiveClass: 'border-gray-900 text-gray-500 hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100'
    }
  },
  computed: {
    pageName() {
      console.log(this.$route.name);
      return this.$route.name
    }
  }
}
</script>
