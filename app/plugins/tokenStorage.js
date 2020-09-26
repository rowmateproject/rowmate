import axios from 'axios'
import Cookies from 'js-cookie'

class TokenStorage {
  static getNewToken() {
    return new Promise((resolve, reject) => {
      axios.config.headers.Authorization = `Bearer ${this.getRefreshToken()}`

      axios.post(`${process.env.API_URL}/auth/jwt/refresh`).then((response) => {
        const accessToken = response.data.access_token
        this.storeAccessToken(accessToken)
        resolve(accessToken)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  static storeAccessToken(accessToken) {
    Cookies.set('accessToken', accessToken, {
      samesite: 'Lax',
      expires: 3600,
      secure: true
    })
  }

  static storeRefreshToken(refreshToken) {
    Cookies.set('refreshToken', refreshToken, {
      samesite: 'Lax',
      expires: 3600,
      secure: true
    })
  }

  static clear() {
    Cookies.remove('refreshToken', {
      secure: true
    })
    Cookies.remove('accessToken', {
      secure: true
    })
  }

  static getRefreshToken() {
    return Cookies.get('refreshToken')
  }

  static getAccessToken() {
    return Cookies.get('accessToken')
  }
}

export {
  TokenStorage
}
