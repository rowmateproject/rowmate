import Cookies from 'js-cookie'

export default (context, inject) => {
  const logout = arg => {
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

    context.store.commit('updateName', null)
    context.store.commit('updateIsActive', null)
    context.store.commit('updateImageBlob', null)
    context.store.commit('updateAccessToken', null)
    context.store.commit('updateRefreshToken', null)
    context.store.commit('updateIsConfirmed', null)
    context.store.commit('updateIsSuperuser', null)
    context.store.commit('updateAccessoriesType', null)
    context.store.commit('updateFacialHairColor', null)
    context.store.commit('updateFacialHairType', null)
    context.store.commit('updateGraphicType', null)
    context.store.commit('updateClotheColor', null)
    context.store.commit('updateEyebrowType', null)
    context.store.commit('updateCircleColor', null)
    context.store.commit('updateClotheType', null)
    context.store.commit('updateHairColor', null)
    context.store.commit('updateMouthType', null)
    context.store.commit('updateSkinColor', null)
    context.store.commit('updateIsCircle', null)
    context.store.commit('updateTopColor', null)
    context.store.commit('updateEyeType', null)
    context.store.commit('updateTopType', null)

    context.$auth.logout()
    context.redirect('/');
  }

  inject('logout', logout)
}
