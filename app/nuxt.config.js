export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'rowmate.org',
    meta: [{
        charset: 'utf-8'
      },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: ''
      }
    ],
    link: [{
      rel: 'icon',
      type: 'image/x-icon',
      href: '/favicon.ico'
    }, {
      rel: 'mask-icon',
      href: '/safari-pinned-tab.svg',
      color: '#3182ce'
    }, {
      rel: 'manifest',
      href: '/site.webmanifest'
    }, {
      rel: 'icon',
      type: 'image/png',
      sizes: '16x16',
      href: '/favicon-16x16.png'
    }, {
      rel: 'apple-touch-icon',
      sizes: '180x180',
      href: '/apple-touch-icon.png'
    }, {
      rel: 'icon',
      type: 'image/png',
      sizes: '32x32',
      href: '/favicon-32x32.png'
    }],
    script: [{
      src: "https://code.jquery.com/jquery-3.5.1.min.js",
      type: "text/javascript"
    }]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [{
    src: '@/plugins/vClickOutside',
    ssr: false
  }, {
    src: '@/plugins/handleLogout',
    ssr: false
  }, {
    src: '@/plugins/interceptor',
    ssr: true
  }],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/eslint-module',
    ['@nuxtjs/fontawesome', {
      component: 'fa',
      suffix: false,
      icons: {
        brands: true,
        solid: true
      }
    }]
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/dotenv',
    ['nuxt-i18n', {
      locales: [{
          name: 'Deutsch',
          code: 'de',
          iso: 'de-CH',
          file: 'de-CH.js'
        },
        {
          name: 'English',
          code: 'en',
          iso: 'en-GB',
          file: 'en-GB.js'
        },
        {
          name: 'Français',
          code: 'fr',
          iso: 'fr-CH',
          file: 'fr-CH.js'
        },
      ],
      langDir: 'lang/',
      lazy: true,
      defaultLocale: 'de',
      detectBrowserLanguage: {
        useCookie: true,
        cookieKey: 'i18n_redirected'
      }
    }]
  ],

  auth: {
    redirect: {
      login: '/signin',
      logout: '/',
      callback: '/callback',
      home: false
    },
    cookie: false,
    vuex: {
      namespace: ''
    },
    localStorage: {
      prefix: ''
    },
    strategies: {
      google: {
        accessType: 'offline',
        grantType: 'authorization_code',
        codeChallengeMethod: 'S256',
        responseType: 'code',
        scope: ['openid', 'profile', 'email'],
        clientSecret: process.env.CLIENT_SECRET,
        clientId: process.env.CLIENT_ID,
        autoFetchUser: false,
        endpoints: {
          token: `${process.env.API_URL}/auth/google/callback`,
          userInfo: `${process.env.API_URL}/users/me`
        }
      }
    }
  },

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {},

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {}
}
