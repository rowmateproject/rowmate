import {
  TokenStorage
} from '@/plugins/tokenStorage'

export default ({
  app,
  store
}) => {
  let accessToken = TokenStorage.getAccessToken()

  if (accessToken !== undefined) {
    app.$axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`
  }

  app.$axios.interceptors.request.use((request) => {
    if (request.config) {
      accessToken = TokenStorage.getAccessToken()

      if (accessToken !== undefined) {
        request.config.config.headers.Authorization = `Bearer ${accessToken}`
      }

      Promise.resolve(request)
    } else {
      accessToken = TokenStorage.getAccessToken()

      if (accessToken !== undefined) {
        request.headers.Authorization = `Bearer ${accessToken}`
      }

      return request
    }
  }, (error) => {
    Promise.reject(error)
  })

  app.$axios.interceptors.response.use((config) => {
    if (config.status === 401) {
      // Try request again with new token
      return TokenStorage.getNewToken().then((token) => {
        // New request with new token
        config.config.headers.Authorization = `Bearer ${token}`

        return new Promise((resolve, reject) => {
          app.$axios.$request(config.config).then((res) => {
            resolve(res)
          }).catch((err) => {
            reject(err)
          })
        })
      }).catch((e) => {
        // Logout user when a new refresh token cant be retrieved
        app.$logout()
      })
    }

    accessToken = TokenStorage.getAccessToken()

    if (accessToken !== undefined) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  }, (error) => {
    // Return any error which is not due to authentication
    // You may see errors when cors allow_origins is empty
    if (error.config.status !== 401) {
      return new Promise((resolve, reject) => {
        reject(error)
      })
    } else {
      // Logout user if token refresh didn't work
      if (error.config.url.includes('/auth/jwt/refresh')) {
        TokenStorage.clear()

        app.$router.push({
          name: 'index___de'
        })

        return new Promise((resolve, reject) => {
          reject(error)
        })
      }

      // Try request again with new token
      return TokenStorage.getNewToken().then((token) => {
        // New request with new token
        error.config.headers.Authorization = `Bearer ${token}`

        return new Promise((resolve, reject) => {
          app.$axios.request(error.config).then((res) => {
            resolve(res)
          }).catch((err) => {
            reject(err)
          })
        })
      }).catch((error) => {
        Promise.reject(error)
      })
    }
  })
}
