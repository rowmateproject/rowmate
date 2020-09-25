<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Theme</h3>

  <form @submit.prevent="patchTheme">
    <ul class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 mt-8">
      <li v-for="color, key, index in theme" :key="index" class="bg-white px-2 pt-1 pb-2">
        <color @data="updateStyles" :id="index" :name="key" :hex="color" />
      </li>
    </ul>

    <div class="flex justify-end mt-4">
      <button class="px-4 py-2 bg-color-button text-color-button rounded-md focus:outline-none">
        {{ $t('save') }}
      </button>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {
      theme: {}
    }
  },
  mounted() {
    this.$axios.$get(`${process.env.API_URL}/theme/default`).then(res => {
      this.theme = res
    })
  },
  watch: {
    'theme.headerBackground': function() {
      this.$store.commit('updateHeaderBackground', this.theme.headerBackground)
    },
    'theme.footerBackground': function() {
      this.$store.commit('updateFooterBackground', this.theme.footerBackground)
    },
    'theme.buttonBackground': function() {
      this.$store.commit('updateButtonBackground', this.theme.buttonBackground)
    },
    'theme.imageBackground': function() {
      this.$store.commit('updateImageBackground', this.theme.imageBackground)
    },
    'theme.pageBackground': function() {
      this.$store.commit('updatePageBackground', this.theme.pageBackground)
    },
    'theme.formBackground': function() {
      this.$store.commit('updateFormBackground', this.theme.formBackground)
    },
    'theme.navBackground': function() {
      this.$store.commit('updateNavBackground', this.theme.navBackground)
    },
    'theme.footerText': function() {
      this.$store.commit('updateFormBorder', this.theme.footerText)
    },
    'theme.formBorder': function() {
      this.$store.commit('updateFooterText', this.theme.formBorder)
    },
    'theme.buttonText': function() {
      this.$store.commit('updateButtonText', this.theme.buttonText)
    },
    'theme.imageText': function() {
      this.$store.commit('updateImageText', this.theme.imageText)
    },
    'theme.titleText': function() {
      this.$store.commit('updateTitleText', this.theme.titleText)
    },
    'theme.linkText': function() {
      this.$store.commit('updateLinkText', this.theme.linkText)
    },
    'theme.bodyText': function() {
      this.$store.commit('updateBodyText', this.theme.bodyText)
    },
    'theme.saleText': function() {
      this.$store.commit('updateSaleText', this.theme.saleText)
    },
    'theme.formText': function() {
      this.$store.commit('updateFormText', this.theme.formText)
    },
    'theme.pageText': function() {
      this.$store.commit('updatePageText', this.theme.pageText)
    },
    'theme.navText': function() {
      this.$store.commit('updateNavText', this.theme.navText)
    },
  },
  computed: {
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  methods: {
    updateStyles(object) {
      this.theme[object.name] = object.color

      const existingElement = document.querySelector('style#rowmate')
      const styleElement = document.createElement('style')
      styleElement.setAttribute('id', 'rowmate')

      if (existingElement) {
        existingElement.parentNode.removeChild(existingElement)
      }

      const element = document.querySelector('head').appendChild(styleElement)

      element.sheet.insertRule(`.border-color-form-hover:hover {border-color: ${this.handleColor(this.theme.formBorder, -50)}}`, 0)
      element.sheet.insertRule(`.border-color-form-focus:focus {border-color: ${this.handleColor(this.theme.formBorder, -50)}}`, 0)
      element.sheet.insertRule(`.text-color-button {color: ${this.theme.buttonText}}`, 0)
      element.sheet.insertRule(`.text-color-button:hover {color: ${this.handleColor(this.theme.buttonBackground, +150)}}`, 0)
      element.sheet.insertRule(`.text-color-button:focus {color: ${this.handleColor(this.theme.buttonBackground, +150)}}`, 0)
      element.sheet.insertRule(`.text-color-nav {color: ${this.theme.navText}}`, 0)
      element.sheet.insertRule(`.text-color-page {color: ${this.theme.pageText}}`, 0)
      element.sheet.insertRule(`.text-color-link {color: ${this.theme.linkText}}`, 0)
      element.sheet.insertRule(`.text-color-title {color: ${this.theme.titleText}}`, 0)
      element.sheet.insertRule(`.bg-color-nav {background-color: ${this.theme.navBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-form {background-color: ${this.theme.formBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-page {background-color: ${this.theme.pageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-header {background-color: ${this.theme.headerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-footer {background-color: ${this.theme.footerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button {background-color: ${this.theme.buttonBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button:focus {background-color: ${this.handleColor(this.theme.buttonBackground, -50)}}`, 0)
      element.sheet.insertRule(`.bg-color-button:hover {background-color: ${this.handleColor(this.theme.buttonBackground, -50)}}`, 0)
    },
    handleColor(col, amt) {
      let usePound = false

      if (col[0] == '#') {
        col = col.slice(1)
        usePound = true
      }

      let num = parseInt(col, 16)
      let r = (num >> 16) + amt

      if (r > 255) r = 255
      else if (r < 0) r = 0

      let b = ((num >> 8) & 0x00FF) + amt

      if (b > 255) b = 255
      else if (b < 0) b = 0

      let g = (num & 0x0000FF) + amt

      if (g > 255) g = 255
      else if (g < 0) g = 0

      return (usePound ? '#' : '') + (g | (b << 8) | (r << 16)).toString(16)
    },
    patchTheme() {
      this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

      this.$axios({
        method: 'PATCH',
        url: `${process.env.API_URL}/theme/default`,
        data: {
          headerBackground: this.theme.headerBackground,
          footerBackground: this.theme.footerBackground,
          buttonBackground: this.theme.buttonBackground,
          imageBackground: this.theme.imageBackground,
          pageBackground: this.theme.pageBackground,
          formBackground: this.theme.formBackground,
          navBackground: this.theme.navBackground,
          footerText: this.theme.footerText,
          formBorder: this.theme.formBorder,
          buttonText: this.theme.buttonText,
          imageText: this.theme.imageText,
          titleText: this.theme.titleText,
          linkText: this.theme.linkText,
          bodyText: this.theme.bodyText,
          saleText: this.theme.saleText,
          formText: this.theme.formText,
          pageText: this.theme.pageText,
          navText: this.theme.navText
        },
        validateStatus: () => true
      }).then(res => {
        console.log(res.data)
      })
    }
  }
}
</script>
