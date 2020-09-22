const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => {
  return {
    isActive: null,
    isConfirmed: null,
    isSuperuser: null,
    accessToken: null,
    name: null
  }
}

export const mutations = {
  updateAccessToken(state, accessToken) {
    state.accessToken = accessToken
  },
  updateIsConfirmed(state, isConfirmed) {
    state.isConfirmed = isConfirmed
  },
  updateIsSuperuser(state, isSuperuser) {
    state.isSuperuser = isSuperuser
  },
  updateIsActive(state, isActive) {
    state.isActive = isActive
  },
  updateName(state, name) {
    state.name = name
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

    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)

      try {
        accessToken = parsed.accessToken
        isConfirmed = parsed.isConfirmed
        isSuperuser = parsed.isSuperuser
        isActive = parsed.isActive
        name = parsed.name
      } catch (err) {
        // eslint-disable-next-line
        console.log(err)
      }
    }

    commit('updateAccessToken', accessToken)
    commit('updateIsConfirmed', isConfirmed)
    commit('updateIsSuperuser', isSuperuser)
    commit('updateIsActive', isActive)
    commit('updateName', name)
  }
}
