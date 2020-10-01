import jwtDecode from 'jwt-decode'
import {
  TokenStorage
} from '@/plugins/tokenStorage'

export default ({
  app,
  store
}) => {
  let accessToken = TokenStorage.getAccessToken()

  if (accessToken !== undefined) {
    const tokenExpires = new Date(jwtDecode(accessToken).exp * 1000)
    // eslint-disable-next-line
    console.debug({expires: tokenExpires.toUTCString()})
    app.$axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`
  }

  app.$axios.interceptors.request.use((request) => {
    if (request.config) {
      accessToken = TokenStorage.getAccessToken()

      if (accessToken !== undefined) {
        const tokenExpires = new Date(jwtDecode(accessToken).exp * 1000)
        // eslint-disable-next-line
        console.debug({expires: tokenExpires.toUTCString()})
        request.config.config.headers.Authorization = `Bearer ${accessToken}`
      }

      Promise.reject(request)
    } else {
      accessToken = TokenStorage.getAccessToken()

      if (accessToken !== undefined) {
        const tokenExpires = new Date(jwtDecode(accessToken).exp * 1000)
        // eslint-disable-next-line
        console.debug({expires: tokenExpires.toUTCString()})
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
        // eslint-disable-next-line
        console.debug(token)

        // New request with new token
        config.config.headers.Authorization = `Bearer ${token}`

        return new Promise((resolve, reject) => {
          return app.$axios.$request(config.config).then((res) => {
            resolve(res)
          }).catch((err) => {
            reject(err)
          })
        })
      }).catch((e) => {
        Promise.reject(e)
      })
    }

    accessToken = TokenStorage.getAccessToken()

    if (accessToken !== undefined) {
      const tokenExpires = new Date(jwtDecode(accessToken).exp * 1000)
      // eslint-disable-next-line
      console.debug({expires: tokenExpires.toUTCString()})
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  }, (error) => {
    // Return any error which is not due to authentication
    if (error.response.status !== 401) {
      // eslint-disable-next-line
      console.debug(error.response)

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
        // eslint-disable-next-line
        console.debug(token)

        // New request with new token
        error.config.headers.Authorization = `Bearer ${token}`

        return new Promise((resolve, reject) => {
          return app.$axios.request(error.config).then((res) => {
            resolve(res)
          }).catch((err) => {
            // eslint-disable-next-line
            console.debug(err.config)
            reject(err)
          })
        })
      }).catch((error) => {
        // eslint-disable-next-line
        console.debug(error.config)
        Promise.reject(error)
      })
    }
  })
}
