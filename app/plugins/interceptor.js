import {
  TokenStorage
} from '@/plugins/tokenStorage'

export default ({
  app,
  store
}) => {
  app.$axios.defaults.headers.common.Authorization = `Bearer ${TokenStorage.getAccessToken()}`

  app.$axios.interceptors.request.use((request) => {
    if (request.config) {
      request.config.config.headers.Authorization = `Bearer ${TokenStorage.getAccessToken()}`
      Promise.reject(request)
    }

    return request
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
        Promise.reject(e)
      })
    }

    config.headers.Authorization = `Bearer ${TokenStorage.getAccessToken()}`
    return config
  }, (error) => {
    // Return any error which is not due to authentication
    if (error.response.status !== 401) {
      // eslint-disable-next-line
      console.log(error)

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
            // eslint-disable-next-line
            console.log(err)
            reject(err)
          })
        })
      }).catch((error) => {
        // eslint-disable-next-line
        console.log(error)
        Promise.reject(error)
      })
    }
  })
}
