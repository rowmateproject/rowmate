const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => {
  return {
    isActive: null,
    isConfirmed: null,
    isSuperuser: null,
    accessToken: null,
    name: null,
    eyeType: null,
    isCircle: null,
    clotheType: null,
    circleColor: null,
    accessoriesType: null,
    facialHairColor: null,
    facialHairType: null,
    clotheColor: null,
    eyebrowType: null,
    graphicType: null,
    hairColor: null,
    mouthType: null,
    skinColor: null,
    topType: null
  }
}

export const mutations = {
  updateName(state, name) {
    state.name = name
  },
  updateIsActive(state, isActive) {
    state.isActive = isActive
  },
  updateAccessToken(state, accessToken) {
    state.accessToken = accessToken
  },
  updateIsConfirmed(state, isConfirmed) {
    state.isConfirmed = isConfirmed
  },
  updateIsSuperuser(state, isSuperuser) {
    state.isSuperuser = isSuperuser
  },
  updateAccessoriesType(state, accessoriesType) {
    state.accessoriesType = accessoriesType
  },
  updateFacialHairColor(state, facialHairColor) {
    state.facialHairColor = facialHairColor
  },
  updateFacialHairType(state, facialHairType) {
    state.facialHairType = facialHairType
  },
  updateGraphicType(state, graphicType) {
    state.graphicType = graphicType
  },
  updateClotheColor(state, clotheColor) {
    state.clotheColor = clotheColor
  },
  updateEyebrowType(state, eyebrowType) {
    state.eyebrowType = eyebrowType
  },
  updateCircleColor(state, circleColor) {
    state.circleColor = circleColor
  },
  updateClotheType(state, clotheType) {
    state.clotheType = clotheType
  },
  updateHairColor(state, hairColor) {
    state.hairColor = hairColor
  },
  updateMouthType(state, mouthType) {
    state.mouthType = mouthType
  },
  updateSkinColor(state, skinColor) {
    state.skinColor = skinColor
  },
  updateIsCircle(state, isCircle) {
    state.isCircle = isCircle
  },
  updateEyeType(state, eyeType) {
    state.eyeType = eyeType
  },
  updateTopType(state, topType) {
    state.topType = topType
  }
}

export const actions = {
  nuxtServerInit({
    commit
  }, {
    req
  }) {
    let name = null
    let isActive = null
    let isConfirmed = null
    let isSuperuser = null
    let accessToken = null
    let eyeType = null
    let isCircle = null
    let clotheType = null
    let circleColor = null
    let accessoriesType = null
    let facialHairColor = null
    let facialHairType = null
    let clotheColor = null
    let eyebrowType = null
    let graphicType = null
    let hairColor = null
    let mouthType = null
    let skinColor = null
    let topType = null

    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)

      try {
        name = parsed.name
        isActive = parsed.isActive
        accessToken = parsed.accessToken
        isConfirmed = parsed.isConfirmed
        isSuperuser = parsed.isSuperuser
        accessoriesType = parsed.accessoriesType
        facialHairColor = parsed.facialHairColor
        facialHairType = parsed.facialHairType
        clotheColor = parsed.clotheColor
        eyebrowType = parsed.eyebrowType
        graphicType = parsed.graphicType
        circleColor = parsed.circleColor
        clotheType = parsed.clotheType
        hairColor = parsed.hairColor
        mouthType = parsed.mouthType
        skinColor = parsed.skinColor
        isCircle = parsed.isCircle
        eyeType = parsed.eyeType
        topType = parsed.topType
      } catch (err) {
        // eslint-disable-next-line
        console.log(err)
      }
    }

    commit('updateName', name)
    commit('updateIsActive', isActive)
    commit('updateAccessToken', accessToken)
    commit('updateIsConfirmed', isConfirmed)
    commit('updateIsSuperuser', isSuperuser)
    commit('updateAccessoriesType', accessoriesType)
    commit('updateFacialHairColor', facialHairColor)
    commit('updateFacialHairType', facialHairType)
    commit('updateGraphicType', graphicType)
    commit('updateClotheColor', clotheColor)
    commit('updateEyebrowType', eyebrowType)
    commit('updateCircleColor', circleColor)
    commit('updateClotheType', clotheType)
    commit('updateHairColor', hairColor)
    commit('updateMouthType', mouthType)
    commit('updateSkinColor', skinColor)
    commit('updateIsCircle', isCircle)
    commit('updateEyeType', eyeType)
    commit('updateTopType', topType)
  }
}
