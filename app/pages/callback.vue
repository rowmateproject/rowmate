<template>
<h1>Callback from google signin, {{ $auth.loggedIn }}</h1>
</template>

<script>
import Cookies from 'js-cookie'

export default {
  async mounted() {
    await this.$auth.fetchUser().then((res) => {
      const user = this.$auth.user
      const state = this.$auth.$storage._state

      this.$store.commit('updateName', user.name)
      this.$store.commit('updateIsActive', user.is_active)
      this.$store.commit('updateIsConfirmed', user.is_confirmed)
      this.$store.commit('updateIsSuperuser', user.is_superuser)
      this.$store.commit('updateRefreshToken', state['_refresh_token.google'])
      this.$store.commit('updateAccessToken', state['_token.google'].replace('Bearer ', ''))

      this.$store.commit('updateAccessoriesType', user.avatar.accessoriesType)
      this.$store.commit('updateFacialHairColor', user.avatar.facialHairColor)
      this.$store.commit('updateFacialHairType', user.avatar.facialHairType)
      this.$store.commit('updateGraphicType', user.avatar.graphicType)
      this.$store.commit('updateClotheColor', user.avatar.clotheColor)
      this.$store.commit('updateEyebrowType', user.avatar.eyebrowType)
      this.$store.commit('updateCircleColor', user.avatar.circleColor)
      this.$store.commit('updateClotheType', user.avatar.clotheType)
      this.$store.commit('updateHairColor', user.avatar.hairColor)
      this.$store.commit('updateMouthType', user.avatar.mouthType)
      this.$store.commit('updateSkinColor', user.avatar.skinColor)
      this.$store.commit('updateTopColor', user.avatar.topColor)
      this.$store.commit('updateEyeType', user.avatar.eyeType)
      this.$store.commit('updateTopType', user.avatar.topType)

      Cookies.set('refreshToken', state['_refresh_token.google'], {
        samesite: 'Lax',
        expires: 50000,
        secure: true
      })

      Cookies.set('accessToken', state['_token.google'].replace('Bearer ', ''), {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('isActive', user.is_active, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('isConfirmed', user.is_confirmed, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('isSuperuser', user.is_superuser, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('name', user.name, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('accessoriesType', user.avatar.accessoriesType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('facialHairColor', user.avatar.facialHairColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('facialHairType', user.avatar.facialHairType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('graphicType', user.avatar.graphicType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('clotheColor', user.avatar.clotheColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('eyebrowType', user.avatar.eyebrowType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('circleColor', user.avatar.circleColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('clotheType', user.avatar.clotheType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('hairColor', user.avatar.hairColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('mouthType', user.avatar.mouthType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('skinColor', user.avatar.skinColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('eyeType', user.avatar.eyeType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('topType', user.avatar.topType, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      Cookies.set('topColor', user.avatar.topColor, {
        samesite: 'Lax',
        expires: 3600,
        secure: true
      })

      this.$router.push(this.localePath({
        name: 'dashboard'
      }))
    })
  }
}
</script>
