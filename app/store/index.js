const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => {
  return {
    auth: null,
    userId: null,
    loading: false,
    userRoles: null,
    accessToken: null,
    userAvatarUrl: null,
    userAvatar: null,
    userName: null
  }
}

export const mutations = {
  setAuth(state, auth) {
    state.auth = auth
  },
  updateUserId(state, userId) {
    state.userId = userId
  },
  updateUserRoles(state, userRoles) {
    state.userRoles = userRoles
  },
  updateAccessToken(state, accessToken) {
    state.accessToken = accessToken
  },
  updateUserAvatarUrl(state, avatarUrl) {
    state.userAvatarUrl = avatarUrl
  },
  updateUserAvatar(state, avatar) {
    state.userAvatar = avatar
  },
  updateLoadingIndicator(state, loading) {
    state.loading = loading
  },
  updateUserName(state, name) {
    state.userName = name
  }
}

export const actions = {
  nuxtServerInit({
    commit
  }, {
    req
  }) {
    let accessToken = null

    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)

      try {
        accessToken = parsed.accessToken
      } catch (err) {
        // eslint-disable-next-line
        console.log(err)
      }
    }

    commit('updateAccessToken', accessToken)
  }
}
