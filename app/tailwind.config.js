const plugin = require('tailwindcss/plugin')

const {
  colors
} = require('tailwindcss/defaultTheme')
const {
  fontsize
} = require('tailwindcss/defaultTheme')

module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      fontSize: {
        ...fontsize,
        '10xl': ['8rem', '2rem']
      },
      colors: {
        gray: {
          ...colors.gray,
          250: '#f7f3e8'
        },
        blue: {
          ...colors.blue,
          550: '#0e67b4'
        }
      }
    },
  },
  variants: {
    margin: ['responsive', 'siblings'],
    backgroundColor: ['responsive', 'hover', 'focus', 'even', 'odd']
  },
  plugins: [
    plugin(function({
      addVariant,
      e
    }) {
      addVariant('siblings', ({
        modifySelectors,
        separator
      }) => {
        modifySelectors(({
          className
        }) => {
          return `.${e(`siblings${separator}${className}`)} > * + *`
        })
      })
    })
  ]
}
