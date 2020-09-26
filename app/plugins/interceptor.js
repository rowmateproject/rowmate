import {
  TokenStorage
} from '@/plugins/tokenStorage.js'

export default ({
  app,
  store
}) => {
  app.$axios.interceptors.request.use((request) => {
    if (request.config) {
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

    return config
  }, (error) => {
    // Return any error which is not due to authentication back to the calling service
    if (error.response.status !== 401) {
      Promise.reject(error)
    }

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
  })
}
