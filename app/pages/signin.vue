<template>
<div class="flex flex-col min-h-screen">
  <div class="flex-grow flex flex-col items-center justify-center p-3 lg:p-0">
    <img src="/rowmate_without_margins.png" class="w-full max-w-md px-3 pb-3 lg:px-6 lg:pb-6" />
    <form @submit.prevent="loginSubmit" class="bg-color-form rounded-lg w-full max-w-md p-3 lg:p-6">
      <h1 class="text-2xl lg:text-4xl leading-none font-medium mb-3">{{ $t('signin') }}</h1>
      <p class="text-gray-800 text-lg">Melde dich an um dein Dashboard zu sehen und um Dich in anstehende Events zu einzutragen.</p>
      <p v-if="showResponse" class="text-red-500 lg:text-lg my-3">{{ response }}</p>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="email">
          {{ $t('email') }}
        </label>
        <input name="email" v-model="email" :class="[errors.email ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="email" type="text"
          placeholder="me@example.com">
        <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
      </div>
      <div class="w-full my-3 lg:my-6">
        <label class="block text-color-form font-semibold mb-2" for="password">
          {{ $t('password') }}
        </label>
        <input name="password" v-model="password" :class="[errors.password ? 'border-red-500' : 'border-color-form']" class="appearance-none block w-full bg-gray-100 text-color-title border rounded focus:outline-none px-3 py-2" id="password" type="password"
          placeholder="••••••••">
        <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
        <small>
          <nuxt-link to="/forgot" class="text-color-link focus:outline-none mr-2">{{ $t('forgotPassword') }}</nuxt-link>
        </small>
      </div>
      <p class="flex justify-end">
        <google-button />
        <button class="cursor-pointer bg-color-button text-color-button rounded focus:outline-none px-4 py-2" type="submit">{{ $t('signin') }}</button>
      </p>
    </form>
  </div>
</div>
</template>

<script>
import Cookies from 'js-cookie'

export default {
  data() {
    return {
      errors: {
        email: false,
        password: false
      },
      email: null,
      password: null,
      response: null,
      showResponse: false,
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  watch: {
    email: function() {
      if (this.email.trim() !== '') {
        if (this.emailRegex.test(this.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length >= 5) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    }
  },
  middleware: 'authenticated',
  methods: {
    loginSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.email) {
        this.errors.email = true
      }
      if (!this.password) {
        this.errors.password = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        const formData = new FormData()

        formData.set('username', this.email.trim())
        formData.set('password', this.password.trim())

        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/auth/jwt/login`,
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.$store.commit('updateName', res.data.name)
            this.$store.commit('updateIsActive', res.data.is_active)
            this.$store.commit('updateIsConfirmed', res.data.is_confirmed)
            this.$store.commit('updateIsSuperuser', res.data.is_superuser)
            this.$store.commit('updateRefreshToken', res.data.refresh_token)
            this.$store.commit('updateAccessToken', res.data.access_token)

            this.$store.commit('updateAccessoriesType', res.data.avatar.accessoriesType)
            this.$store.commit('updateFacialHairColor', res.data.avatar.facialHairColor)
            this.$store.commit('updateFacialHairType', res.data.avatar.facialHairType)
            this.$store.commit('updateGraphicType', res.data.avatar.graphicType)
            this.$store.commit('updateClotheColor', res.data.avatar.clotheColor)
            this.$store.commit('updateEyebrowType', res.data.avatar.eyebrowType)
            this.$store.commit('updateCircleColor', res.data.avatar.circleColor)
            this.$store.commit('updateClotheType', res.data.avatar.clotheType)
            this.$store.commit('updateHairColor', res.data.avatar.hairColor)
            this.$store.commit('updateMouthType', res.data.avatar.mouthType)
            this.$store.commit('updateSkinColor', res.data.avatar.skinColor)
            this.$store.commit('updateTopColor', res.data.avatar.topColor)
            this.$store.commit('updateEyeType', res.data.avatar.eyeType)
            this.$store.commit('updateTopType', res.data.avatar.topType)

            Cookies.set('refreshToken', res.data.refresh_token, {
              samesite: 'Lax',
              expires: 50000,
              secure: true
            })

            Cookies.set('accessToken', res.data.access_token, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('isActive', res.data.is_active, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('isConfirmed', res.data.is_confirmed, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('isSuperuser', res.data.is_superuser, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('name', res.data.name, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('accessoriesType', res.data.avatar.accessoriesType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('facialHairColor', res.data.avatar.facialHairColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('facialHairType', res.data.avatar.facialHairType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('graphicType', res.data.avatar.graphicType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('clotheColor', res.data.avatar.clotheColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('eyebrowType', res.data.avatar.eyebrowType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('circleColor', res.data.avatar.circleColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('clotheType', res.data.avatar.clotheType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('hairColor', res.data.avatar.hairColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('mouthType', res.data.avatar.mouthType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('skinColor', res.data.avatar.skinColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('eyeType', res.data.avatar.eyeType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('topType', res.data.avatar.topType, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })

            Cookies.set('topColor', res.data.avatar.topColor, {
              samesite: 'Lax',
              expires: 3600,
              secure: true
            })
            let standardAvatar = {
                  'isCircle': true,
                  'mouthType': 'Smile',
                  'accessoriesType': 'Blank',
                  'graphicType': 'Bat',
                  'topType': 'Hat',
                  'topColor': 'Gray02',
                  'clotheType': 'CollarSweater',
                  'clotheColor': 'Black',
                  'eyeType': 'Wink',
                  'eyebrowType': 'Default',
                  'facialHairType': 'Blank',
                  'facialHairColor': 'Auburn',
                  'hairColor': 'Brown',
                  'skinColor': 'Yellow',
                  'circleColor': '#87CEEB'
              }

            let AvatarNotChanged = true
            for (const [key, value] of Object.entries(res.data.avatar)) {
              if (standardAvatar[key] !== value) {
                AvatarNotChanged = false
              }
            }
            if (AvatarNotChanged) {
              this.$router.push(this.localePath({
                name: 'settings'
              }))
            } else {
            this.$router.push(this.localePath({
              name: 'dashboard'
            }))
          }
          } else {
            this.showResponse = true
            this.response = res.data.detail
          }
        })
      }
    }
  }
}
</script>
