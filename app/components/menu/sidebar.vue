<template>
<div class="flex min-h-screen">
  <div class="bg-color-nav fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform -translate-x-full ease-in overflow-y-auto lg:translate-x-0 lg:static lg:inset-0">
    <div class="bg-color-footer text-center py-1">
      <img v-if="imgageBlob" :src="imgageBlob" class="w-full object-cover px-4 py-1">
      <logo v-else class="px-4 py-1" />
    </div>

    <nav class="mt-8">
      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" :to="localePath('/dashboard')">
        <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
        <span class="col-span-5">Dashboard</span>
      </nuxt-link>

      <nuxt-link class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('calendar') ? activeClass : inactiveClass]" :to="localePath('/calendar')">
        <fa :icon="['fas', 'calendar-week']" class="col-span-1 mt-1" />
        <span class="col-span-5">Kalender</span>
      </nuxt-link>

      <nuxt-link class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('poll') ? activeClass : inactiveClass]" :to="localePath('/poll')">
        <fa :icon="['fas', 'poll']" class="col-span-1 mt-1" />
        <span class="col-span-5">Umfragen</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('language') ? activeClass : inactiveClass]" :to="localePath('/language')">
        <fa :icon="['fas', 'font']" class="col-span-1 mt-1" />
        <span class="col-span-5">Sprache</span>
      </nuxt-link>

      <nuxt-link class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('settings') ? activeClass : inactiveClass]" :to="localePath('/settings')">
        <fa :icon="['fas', 'user-cog']" class="col-span-1 mt-1" />
        <span class="col-span-5">Profile</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('users') ? activeClass : inactiveClass]" :to="localePath('/users')">
        <fa :icon="['fas', 'users']" class="col-span-1 mt-1" />
        <span class="col-span-5">Nutzer</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('theme') ? activeClass : inactiveClass]" :to="localePath('/theme')">
        <fa :icon="['fas', 'comment-alt']" class="col-span-1 mt-1" />
        <span class="col-span-5">Theme</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('event') ? activeClass : inactiveClass]" :to="localePath('/event')">
        <fa :icon="['fas', 'sticky-note']" class="col-span-1 mt-1" />
        <span class="col-span-5">Events</span>
      </nuxt-link>

      <nuxt-link v-if="isSuperuser === 'true' || isSuperuser === true" class="text-color-nav focus:outline-none grid grid-cols-6 mt-1 py-3 px-6" :class="[comparePageName('mail') ? activeClass : inactiveClass]" :to="localePath('/mail')">
        <fa :icon="['fas', 'mail-bulk']" class="col-span-1 mt-1" />
        <span class="col-span-5">Vorlagen</span>
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
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/theme/default/image`,
      responseType: 'blob',
      validateStatus: () => true
    }).then(res => {
      if (res.status === 200) {
        this.$store.commit('updateImageBlob', this.createObjectURL(res.data))
      }
    })
  },
  computed: {
    pageName() {
      return this.$route.name
    },
    imgageBlob() {
      return this.$store.state.imageBlob
    },
    isSuperuser() {
      return this.$store.state.isSuperuser
    }
  },
  methods: {
    createObjectURL(blob) {
      return URL.createObjectURL(blob)
    },
    comparePageName(value) {
      return this.pageName === `${value}___${this.$i18n.locale}`
    }
  }
}
</script>
