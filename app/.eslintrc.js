module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  rules: {
    'space-before-function-paren': ['error', {
      'anonymous': 'ignore',
      'asyncArrow': 'ignore',
      'named': 'ignore'
    }],
  },
  parserOptions: {
    ecmaVersion: 2020,
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: []
}
