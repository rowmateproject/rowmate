<template>
<header class="flex justify-between items-center py-4 px-6 bg-white border-b-4 border-indigo-500">
  <div class="flex w-full md:w-4/12 lg:w-3/12 items-center">
    <div class="w-full relative">
      <span class="absolute inset-y-0 left-0 pl-3 flex items-center">
        <svg class="h-5 w-5 text-gray-500" viewBox="0 0 24 24" fill="none">
          <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>

      <input class="w-full rounded pl-10 pr-4 py-3 border focus:outline-none focus:border-blue-550" type="text" placeholder="Search">
    </div>
  </div>

  <div class="flex items-center">
    <button class="flex mx-4 text-gray-600 focus:outline-none">
      <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M15 17H20L18.5951 15.5951C18.2141 15.2141 18 14.6973 18 14.1585V11C18 8.38757 16.3304 6.16509 14 5.34142V5C14 3.89543 13.1046 3 12 3C10.8954 3 10 3.89543 10 5V5.34142C7.66962 6.16509 6 8.38757 6 11V14.1585C6 14.6973 5.78595 15.2141 5.40493 15.5951L4 17H9M15 17V18C15 19.6569 13.6569 21 12 21C10.3431 21 9 19.6569 9 18V17M15 17H9"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>

    <div class="relative">
      <button @click="dropdownOpen = !dropdownOpen" class="relative z-10 block h-10 w-10 overflow-hidden focus:outline-none">
        <avatar :avatar="avatar" class="h-full w-full object-cover" />
      </button>

      <div v-show="dropdownOpen" @click="dropdownOpen = false" class="fixed inset-0 h-full w-full z-10"></div>

      <div v-show="dropdownOpen" class="absolute right-0 mt-2 py-2 w-48 bg-white rounded-md shadow-xl z-20">
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-550 hover:text-white">Profile</a>
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-550 hover:text-white">Verein</a>
        <a @click="logout" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-550 hover:text-white">Logout</a>
      </div>
    </div>
  </div>
</header>
</template>

<script>
const Cookie = process.client ? require('js-cookie') : undefined

export default {
  data() {
    return {
      dropdownOpen: false
    }
  },
  computed: {
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
        topType: this.$store.state.topType
      }
    },
    availableLocales() {
      return this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
    }
  },
  methods: {
    logout() {
      Cookie.remove('accessToken', {
        secure: true
      })

      Cookie.remove('isActive', {
        secure: true
      })

      Cookie.remove('isConfirmed', {
        secure: true
      })

      Cookie.remove('isSuperuser', {
        secure: true
      })

      Cookie.remove('updateAccessToken', {
        secure: true
      })

      Cookie.remove('name', {
        secure: true
      })

      Cookie.remove('accessoriesType', {
        secure: true
      })

      Cookie.remove('facialHairColor', {
        secure: true
      })

      Cookie.remove('facialHairType', {
        secure: true
      })

      Cookie.remove('graphicType', {
        secure: true
      })

      Cookie.remove('clotheColor', {
        secure: true
      })

      Cookie.remove('eyebrowType', {
        secure: true
      })

      Cookie.remove('circleColor', {
        secure: true
      })

      Cookie.remove('clotheType', {
        secure: true
      })

      Cookie.remove('hairColor', {
        secure: true
      })

      Cookie.remove('mouthType', {
        secure: true
      })

      Cookie.remove('skinColor', {
        secure: true
      })

      Cookie.remove('isCircle', {
        secure: true
      })

      Cookie.remove('eyeType', {
        secure: true
      })

      Cookie.remove('topType', {
        secure: true
      })

      this.$store.commit('updateAccessToken', null)
      this.$store.commit('updateIsConfirmed', null)
      this.$store.commit('updateIsSuperuser', null)
      this.$store.commit('updateIsActive', null)
      this.$store.commit('updateName', null)

      this.$router.push(this.localePath({
        name: 'index'
      }))
    }
  }
}
</script>
