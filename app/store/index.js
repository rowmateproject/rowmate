const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => {
  return {
    isConfirmed: null,
    isSuperuser: null,
    refreshToken: null,
    accessToken: null,
    isActive: null,

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
    topColor: null,
    topType: null,

    headerBackground: null,
    footerBackground: null,
    buttonBackground: null,
    imageBackground: null,
    pageBackground: null,
    formBackground: null,
    navBackground: null,
    formBorder: null,
    footerText: null,
    buttonText: null,
    imageText: null,
    titleText: null,
    linkText: null,
    bodyText: null,
    saleText: null,
    formText: null,
    pageText: null,
    navText: null
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
  updateRefreshToken(state, refreshToken) {
    state.refreshToken = refreshToken
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
  updateTopColor(state, topColor) {
    state.topColor = topColor
  },
  updateTopType(state, topType) {
    state.topType = topType
  },
  updateHeaderBackground(state, headerBackground) {
    state.headerBackground = headerBackground
  },
  updateFooterBackground(state, footerBackground) {
    state.footerBackground = footerBackground
  },
  updateButtonBackground(state, buttonBackground) {
    state.buttonBackground = buttonBackground
  },
  updateImageBackground(state, imageBackground) {
    state.imageBackground = imageBackground
  },
  updatePageBackground(state, pageBackground) {
    state.pageBackground = pageBackground
  },
  updateFormBackground(state, formBackground) {
    state.formBackground = formBackground
  },
  updateNavBackground(state, navBackground) {
    state.navBackground = navBackground
  },
  updateFormBorder(state, formBorder) {
    state.formBorder = formBorder
  },
  updateFooterText(state, footerText) {
    state.footerText = footerText
  },
  updateButtonText(state, buttonText) {
    state.buttonText = buttonText
  },
  updateImageText(state, imageText) {
    state.imageText = imageText
  },
  updateTitleText(state, titleText) {
    state.titleText = titleText
  },
  updateLinkText(state, linkText) {
    state.linkText = linkText
  },
  updateBodyText(state, bodyText) {
    state.bodyText = bodyText
  },
  updateSaleText(state, saleText) {
    state.saleText = saleText
  },
  updateFormText(state, formText) {
    state.formText = formText
  },
  updatePageText(state, pageText) {
    state.pageText = pageText
  },
  updateNavText(state, navText) {
    state.navText = navText
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
    let refreshToken = null
    let accessToken = null
    let isSuperuser = null

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
    let topColor = null
    let topType = null

    let headerBackground = null
    let footerBackground = null
    let buttonBackground = null
    let imageBackground = null
    let pageBackground = null
    let formBackground = null
    let navBackground = null
    let formBorder = null
    let footerText = null
    let buttonText = null
    let imageText = null
    let titleText = null
    let linkText = null
    let bodyText = null
    let saleText = null
    let formText = null
    let pageText = null
    let navText = null

    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)

      try {
        name = parsed.name
        isActive = parsed.isActive
        accessToken = parsed.accessToken
        refreshToken = parsed.refreshToken
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
        topColor = parsed.topColor
        eyeType = parsed.eyeType
        topType = parsed.topType

        headerBackground = parsed.headerBackground
        footerBackground = parsed.footerBackground
        buttonBackground = parsed.buttonBackground
        imageBackground = parsed.imageBackground
        pageBackground = parsed.pageBackground
        formBackground = parsed.formBackground
        navBackground = parsed.navBackground
        formBorder = parsed.formBorder
        footerText = parsed.footerText
        buttonText = parsed.buttonText
        imageText = parsed.imageText
        titleText = parsed.titleText
        linkText = parsed.linkText
        bodyText = parsed.bodyText
        saleText = parsed.saleText
        formText = parsed.formText
        pageText = parsed.pageText
        navText = parsed.navText
      } catch (err) {
        // eslint-disable-next-line
        console.log(err)
      }
    }

    commit('updateName', name)
    commit('updateIsActive', isActive)
    commit('updateAccessToken', accessToken)
    commit('updateRefreshToken', refreshToken)
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
    commit('updateTopColor', topColor)
    commit('updateTopType', topType)
    commit('updateEyeType', eyeType)

    commit('updateHeaderBackground', headerBackground)
    commit('updateFooterBackground', footerBackground)
    commit('updateButtonBackground', buttonBackground)
    commit('updateImageBackground', imageBackground)
    commit('updatePageBackground', pageBackground)
    commit('updateFormBackground', formBackground)
    commit('updateNavBackground', navBackground)
    commit('updateFormBorder', formBorder)
    commit('updateFooterText', footerText)
    commit('updateButtonText', buttonText)
    commit('updateImageText', imageText)
    commit('updateTitleText', titleText)
    commit('updateLinkText', linkText)
    commit('updateBodyText', bodyText)
    commit('updateSaleText', saleText)
    commit('updateFormText', formText)
    commit('updatePageText', pageText)
    commit('updateNavText', navText)
  }
}
