<template>
<div class="flex min-h-screen bg-color-page font-roboto">
  <sidebar />

  <div class="flex-1 flex flex-col overflow-hidden">
    <searchbar />

    <main class="flex-1 overflow-x-hidden overflow-y-auto">
      <div class="container mx-auto px-6 py-8">
        <nuxt />
      </div>
    </main>
  </div>
</div>
</template>

<script>
export default {
  async mounted() {
    await this.$axios.$get(`${process.env.API_URL}/theme/default`).then(res => {
      this.$store.commit('updateHeaderBackground', res.headerBackground)
      this.$store.commit('updateFooterBackground', res.footerBackground)
      this.$store.commit('updateButtonBackground', res.buttonBackground)
      this.$store.commit('updateImageBackground', res.imageBackground)
      this.$store.commit('updatePageBackground', res.pageBackground)
      this.$store.commit('updateFormBackground', res.formBackground)
      this.$store.commit('updateNavBackground', res.navBackground)
      this.$store.commit('updateFormBorder', res.formBorder)
      this.$store.commit('updateFooterText', res.footerText)
      this.$store.commit('updateButtonText', res.buttonText)
      this.$store.commit('updateImageText', res.imageText)
      this.$store.commit('updateTitleText', res.titleText)
      this.$store.commit('updateLinkText', res.linkText)
      this.$store.commit('updateBodyText', res.bodyText)
      this.$store.commit('updateSaleText', res.saleText)
      this.$store.commit('updateFormText', res.formText)
      this.$store.commit('updatePageText', res.pageText)
      this.$store.commit('updateNavText', res.navText)

      const existingElement = document.querySelector('style#rowmate')
      const styleElement = document.createElement('style')
      styleElement.setAttribute('id', 'rowmate')

      if (existingElement) {
        existingElement.parentNode.removeChild(existingElement)
      }

      const element = document.querySelector('head').appendChild(styleElement)

      element.sheet.insertRule(`.border-color-form-hover:hover {border-color: ${this.handleColor(res.formBorder, -50)}}`, 0)
      element.sheet.insertRule(`.border-color-form-focus:focus {border-color: ${this.handleColor(res.formBorder, -50)}}`, 0)
      element.sheet.insertRule(`.text-color-button {color: ${res.buttonText}}`, 0)
      element.sheet.insertRule(`.text-color-button:hover {color: ${this.handleColor(res.buttonBackground, +150)}}`, 0)
      element.sheet.insertRule(`.text-color-button:focus {color: ${this.handleColor(res.buttonBackground, +150)}}`, 0)
      element.sheet.insertRule(`.text-color-nav {color: ${res.navText}}`, 0)
      element.sheet.insertRule(`.text-color-page {color: ${res.pageText}}`, 0)
      element.sheet.insertRule(`.text-color-link {color: ${res.linkText}}`, 0)
      element.sheet.insertRule(`.text-color-title {color: ${res.titleText}}`, 0)
      element.sheet.insertRule(`.bg-color-nav {background-color: ${res.navBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-form {background-color: ${res.formBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-page {background-color: ${res.pageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-header {background-color: ${res.headerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-footer {background-color: ${res.footerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button {background-color: ${res.buttonBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button:focus {background-color: ${this.handleColor(res.buttonBackground, -50)}}`, 0)
      element.sheet.insertRule(`.bg-color-button:hover {background-color: ${this.handleColor(res.buttonBackground, -50)}}`, 0)
    })
  },
  methods: {
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
    }
  }
}
</script>
