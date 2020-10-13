<template>
<div v-click-outside="hideNav" class="sm:flex sm:min-h-screen h-12 sm:h-auto">
  <div class="fixed w-full top-0 left-0 sm:w-64 overflow-y-auto transition duration-300 transform ease-in overflow-y-auto sm:translate-x-0 sm:static sm:inset-0 z-50 sm:z-0 bg-color-nav">
    <div class="flex justify-between items-center bg-color-image sm:border-b-4 sm:border-gray-900 h-12 sm:h-16 lg:h-20">
      <div>
        <img v-if="imageBlobFile" :src="imageBlobFile" class="w-48 sm:w-full sm:object-cover px-2 sm:px-4">
        <img v-else src="/rowmate.png" class="w-48 sm:w-full sm:object-cover px-2 sm:px-4">
      </div>

      <div @click="toggleNav" class="block sm:focus:outline-none hidden overflow-hidden cursor-pointer h-12 w-12 pr-3">
        <avatar :avatar="avatar" class="h-full w-full object-cover" />
      </div>
    </div>

    <ul :class="[showNav ? 'block z-50' : 'hidden']" class="sm:block sm:mt-8">
      <li @click="toggleNav" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/dashboard')">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">Dashboard</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('organization') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/organization')">
          <fa :icon="['fas', 'columns']" class="col-span-1 mt-1" />
          <span class="col-span-5">Organisation</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('poll') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none  sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/poll')">
          <fa :icon="['fas', 'poll']" class="col-span-1 mt-1" />
          <span class="col-span-5">Umfragen</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('templates') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/templates')">
          <fa :icon="['fas', 'mail-bulk']" class="col-span-1 mt-1" />
          <span class="col-span-5">Vorlagen</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('calendar') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/calendar')">
          <fa :icon="['fas', 'calendar-week']" class="col-span-1 mt-1" />
          <span class="col-span-5">Kalender</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('language') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/language')">
          <fa :icon="['fas', 'font']" class="col-span-1 mt-1" />
          <span class="col-span-5">Sprache</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('settings') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 sm:focus:outline-none mt-1 py-3 px-3 sm:px-6" :to="localePath('/settings')">
          <fa :icon="['fas', 'user-cog']" class="col-span-1 mt-1" />
          <span class="col-span-5">Profile</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('users') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/users')">
          <fa :icon="['fas', 'users']" class="col-span-1 mt-1" />
          <span class="col-span-5">Nutzer</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('boats') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/boats')">
          <fa :icon="['fas', 'ship']" class="col-span-1 mt-1" />
          <span class="col-span-5">Boote</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('theme') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/theme')">
          <fa :icon="['fas', 'paint-brush']" class="col-span-1 mt-1" />
          <span class="col-span-5">Theme</span>
        </nuxt-link>
      </li>
      <li v-if="isSuperuser === 'true' || isSuperuser === true" @click="toggleNav" :class="[comparePageName('event') ? activeClass : inactiveClass]" class="text-color-nav">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" :to="localePath('/event')">
          <fa :icon="['fas', 'sticky-note']" class="col-span-1 mt-1" />
          <span class="col-span-5">Events</span>
        </nuxt-link>
      </li>
      <li @click="logoutUser" class="sm:hidden text-color-nav border-gray-900 text-color-nav hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100">
        <a class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6">
          <fa :icon="['fas', 'sign-out-alt']" class="col-span-1 mt-1" />
          <span class="col-span-5">Logout</span>
        </a>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      showNav: false,
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
    imageBlobFile() {
      return this.$store.state.imageBlob
    },
    isSuperuser() {
      return this.$store.state.isSuperuser
    },
    avatar() {
      return {
        eyeType: this.$store.state.eyeType,
        isCircle: Boolean(this.$store.state.isCircle),
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
    }
  },
  methods: {
    hideNav() {
      return this.showNav = false
    },
    toggleNav() {
      return this.showNav = !this.showNav
    },
    createObjectURL(blob) {
      return URL.createObjectURL(blob)
    },
    comparePageName(value) {
      return this.pageName === `${value}___${this.$i18n.locale}`
    },
    logoutUser() {
      this.toggleNav()
      this.$logout()
    }
  }
}
</script>
