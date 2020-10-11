<template>
<header class="sm:flex justify-between items-center pl-3 pr-2 md:px-6 bg-color-form border-b-4 border-blue-550 sm:h-20 py-3 sm:py-0">
  <div class="flex justify-between items-center w-full">
    <div class="w-full md:w-6/12 lg:w-5/12 xl:w-3/12 relative">
      <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
        <input v-model="searchTerm" @input="lookupSearchTerm" type="text" class="w-full rounded border focus:outline-none p-2">

        <div v-if="users.length > 0" class="w-full absolute z-30">
          <div @click="setSerchTerm(user)" class="hover:bg-gray-300 bg-color-form border shadow p-1" v-for="user in users">
            <avatar class="inline mr-2 pr-2" width="75" :avatar="user.avatar" />
            <span class="leading-5 font-medium text-gray-900">{{ user.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="relative ml-2 sm:ml-0">
      <button @click="toggleDropdown" @keydown.esc="toggleDropdown" class="relative z-10 block h-10 w-10 overflow-hidden focus:outline-none">
        <avatar :avatar="avatar" class="h-full w-full object-cover" />
      </button>

      <ul v-click-outside="toggleDropdown" v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-color-nav overflow-hidden rounded shadow z-20">
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
import Cookies from 'js-cookie'

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
    toggleSearch() {
      this.users = []
    },
    setSerchTerm(user) {
      this.searchTerm = user.name
      this.toggleSearch()
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
      this.$store.commit('updateImageBlob', null)
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
