<template>
<header class="flex justify-between items-center py-3 md:py-4 px-3 md:px-6 bg-color-form border-b-4 border-indigo-500">
  <div class="flex items-center w-full md:w-6/12 lg:w-5/12 xl:w-3/12">
    <div class="w-full relative">
      <span class="absolute inset-y-0 left-0 pl-3 flex items-center">
        <svg class="h-5 w-5 text-color-nav" viewBox="0 0 24 24" fill="none">
          <fa :icon="['fas', 'search']" class="text-color-body" />
        </svg>
      </span>
      <div v-click-outside="hideSearch" @keydown.esc="hideSearch">
        <input class="w-full rounded pl-10 pr-4 py-3 border focus:outline-none border-color-form-focus" type="text" @keyup="findUsers()" @focus="findUsers()" v-model="searchValue" :placeholder="$t('search')">

        <div class="w-full absolute">
          <div class="border p-3 my-1 shadow bg-color-form" v-if="users === false">
            <span class="leading-5 font-medium text-gray-900">No users found</span>
          </div>
          <div class="border p-1 my-1 shadow bg-color-form" v-for="user in users" v-else>
            <avatar class="inline mr-2 pr-2" width="75" :avatar="user.avatar" />
            <span class="leading-5 font-medium text-gray-900">{{ user.name }}</span>
            <span class="ml-auto" <fa :icon="['fas', 'comments']" /></span>
          </div>
        </div>
      </div>
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
      <button @click="toggleDropdown" @keydown.esc="toggleDropdown" class="relative z-10 block h-10 w-10 overflow-hidden focus:outline-none">
        <avatar :avatar="avatar" class="h-full w-full object-cover" />
      </button>

      <ul v-click-outside="toggleDropdown" v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-color-header overflow-hidden rounded shadow z-20">
        <li @click="toggleDropdown">
          <nuxt-link :to="localePath('/settings')" class="block px-4 py-2 text-sm text-color-nav hover:bg-gray-800 border-b border-color-form">Profile</nuxt-link>
        </li>
        <li @click="toggleDropdown">
          <nuxt-link :to="localePath('/#')" class="block px-4 py-2 text-sm text-color-nav hover:bg-gray-800 border-b border-color-form">Verein</nuxt-link>
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
import Cookies from 'js-cookie'

export default {
  data() {
    return {
      showDropdown: false,
      searchValue: '',
      users: []
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
        topColor: this.$store.state.topColor,
        topType: this.$store.state.topType
      }
    },
    availableLocales() {
      return this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
    }
  },
  methods: {
    hideSearch() {
      this.users = []
    },
    toggleDropdown() {
      return this.showDropdown = !this.showDropdown
    },
    findUsers() {
      if (this.searchValue.length > 1) {
        this.$axios.$post(`${process.env.API_URL}/social/users/find`, {
          name: this.searchValue,
          limit: 5
        }).then(res => {
          if (res.users.length === 0) {
            this.users = false
          } else {
            this.users = res.users
          }
        }).catch((error) => {
          console.debug(error)
        })
      }
    },
    logoutUser() {
      Cookies.remove('accessToken', {
        secure: true
      })

      Cookies.remove('refreshToken', {
        secure: true
      })

      Cookies.remove('isActive', {
        secure: true
      })

      Cookies.remove('isConfirmed', {
        secure: true
      })

      Cookies.remove('isSuperuser', {
        secure: true
      })

      Cookies.remove('updateAccessToken', {
        secure: true
      })

      Cookies.remove('name', {
        secure: true
      })

      Cookies.remove('accessoriesType', {
        secure: true
      })

      Cookies.remove('facialHairColor', {
        secure: true
      })

      Cookies.remove('facialHairType', {
        secure: true
      })

      Cookies.remove('graphicType', {
        secure: true
      })

      Cookies.remove('clotheColor', {
        secure: true
      })

      Cookies.remove('eyebrowType', {
        secure: true
      })

      Cookies.remove('circleColor', {
        secure: true
      })

      Cookies.remove('clotheType', {
        secure: true
      })

      Cookies.remove('hairColor', {
        secure: true
      })

      Cookies.remove('mouthType', {
        secure: true
      })

      Cookies.remove('skinColor', {
        secure: true
      })

      Cookies.remove('isCircle', {
        secure: true
      })

      Cookies.remove('eyeType', {
        secure: true
      })

      Cookies.remove('topColor', {
        secure: true
      })

      Cookies.remove('topType', {
        secure: true
      })

      this.$store.commit('updateName', null)
      this.$store.commit('updateIsActive', null)
      this.$store.commit('updateAccessToken', null)
      this.$store.commit('updateRefreshToken', null)
      this.$store.commit('updateIsConfirmed', null)
      this.$store.commit('updateIsSuperuser', null)

      this.$store.commit('updateAccessoriesType', null)
      this.$store.commit('updateFacialHairColor', null)
      this.$store.commit('updateFacialHairType', null)
      this.$store.commit('updateGraphicType', null)
      this.$store.commit('updateClotheColor', null)
      this.$store.commit('updateEyebrowType', null)
      this.$store.commit('updateCircleColor', null)
      this.$store.commit('updateClotheType', null)
      this.$store.commit('updateHairColor', null)
      this.$store.commit('updateMouthType', null)
      this.$store.commit('updateSkinColor', null)
      this.$store.commit('updateIsCircle', null)
      this.$store.commit('updateTopColor', null)
      this.$store.commit('updateEyeType', null)
      this.$store.commit('updateTopType', null)

      this.$router.push(this.localePath({
        name: 'index'
      }))
    }
  }
}
</script>
