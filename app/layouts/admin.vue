<template>
<div class="flex min-h-screen bg-color-page font-roboto">
  <sidebar />

  <div class="flex-1 flex flex-col overflow-hidden">
    <searchbar />

    <main class="flex-1 overflow-x-hidden overflow-y-auto">
      <div class="lg:container mx-auto px-3 md:px-6 py-3 md:py-8">
        <nuxt />
      </div>
    </main>
  </div>
</div>
</template>

<style>
.bg-svg-image {
  background-image: url('/image.svg');
  background-repeat: no-repeat;
}
</style>

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

      element.sheet.insertRule(`.text-color-nav {color: ${res.navText}}`, 0)
      element.sheet.insertRule(`.text-color-link {color: ${res.linkText}}`, 0)
      element.sheet.insertRule(`.text-color-body {color: ${res.bodyText}}`, 0)
      element.sheet.insertRule(`.text-color-sale {color: ${res.saleText}}`, 0)
      element.sheet.insertRule(`.text-color-form {color: ${res.formText}}`, 0)
      element.sheet.insertRule(`.text-color-page {color: ${res.pageText}}`, 0)
      element.sheet.insertRule(`.text-color-image {color: ${res.imageText}}`, 0)
      element.sheet.insertRule(`.text-color-title {color: ${res.titleText}}`, 0)
      element.sheet.insertRule(`.text-color-footer {color: ${res.footerText}}`, 0)
      element.sheet.insertRule(`.text-color-button {color: ${res.buttonText}}`, 0)
      element.sheet.insertRule(`.bg-color-nav {background-color: ${res.navBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-form {background-color: ${res.formBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-page {background-color: ${res.pageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-image {background-color: ${res.imageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-header {background-color: ${res.headerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-footer {background-color: ${res.footerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button {background-color: ${res.buttonBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button:focus {background-color: ${this.handleColor(res.buttonBackground, -40)}}`, 0)
      element.sheet.insertRule(`.bg-color-button:hover {background-color: ${this.handleColor(res.buttonBackground, -40)}}`, 0)
      element.sheet.insertRule(`.border-color-form {border-color: ${res.formBorder}}`, 0)
      element.sheet.insertRule(`.border-color-form:hover {border-color: ${this.handleColor(res.formBorder, -40)}}`, 0)
      element.sheet.insertRule(`.border-color-form:focus {border-color: ${this.handleColor(res.formBorder, -40)}}`, 0)
    })
  },
  methods: {
    handleColor(col, amt) {
      col = col.replace(/^#/, '')
      if (col.length === 3) col = col[0] + col[0] + col[1] + col[1] + col[2] + col[2]

      let [r, g, b] = col.match(/.{2}/g);
      ([r, g, b] = [parseInt(r, 16) + amt, parseInt(g, 16) + amt, parseInt(b, 16) + amt])

      r = Math.max(Math.min(255, r), 0).toString(16)
      g = Math.max(Math.min(255, g), 0).toString(16)
      b = Math.max(Math.min(255, b), 0).toString(16)

      const rr = (r.length < 2 ? '0' : '') + r
      const gg = (g.length < 2 ? '0' : '') + g
      const bb = (b.length < 2 ? '0' : '') + b

      return `#${rr}${gg}${bb}`
    }
  }
}
</script>
