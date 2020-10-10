<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Theme</h3>

  <div class="bg-color-image mt-3 lg:mt-8 px-6 pb-6 pt-4 rounded shadow">
    <h4 class="text-xl mb-1">Hinweis</h4>
    <p>Dein Logo und deine Farben werden auf E-Mails, Newsletter und deiner Profilseite genutzt. Es hilft den Wiedererkennungswert für deine Mitglieder zu steigern.</p>
  </div>

  <image-upload-form />

  <form @submit.prevent="patchTheme">
    <ul class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 mt-8">
      <li v-for="color, key, index in theme" :key="index" class="bg-color-form rounded px-2 pt-1 pb-2">
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
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/theme/default`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.theme = res.data
      } else {
        console.debug(res.data)
      }
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

      element.sheet.insertRule(`.text-color-nav {color: ${this.theme.navText}}`, 0)
      element.sheet.insertRule(`.text-color-link {color: ${this.theme.linkText}}`, 0)
      element.sheet.insertRule(`.text-color-body {color: ${this.theme.bodyText}}`, 0)
      element.sheet.insertRule(`.text-color-sale {color: ${this.theme.saleText}}`, 0)
      element.sheet.insertRule(`.text-color-form {color: ${this.theme.formText}}`, 0)
      element.sheet.insertRule(`.text-color-page {color: ${this.theme.pageText}}`, 0)
      element.sheet.insertRule(`.text-color-image {color: ${this.theme.imageText}}`, 0)
      element.sheet.insertRule(`.text-color-title {color: ${this.theme.titleText}}`, 0)
      element.sheet.insertRule(`.text-color-footer {color: ${this.theme.footerText}}`, 0)
      element.sheet.insertRule(`.text-color-button {color: ${this.theme.buttonText}}`, 0)
      element.sheet.insertRule(`.border-color-form {border-color: ${this.theme.formBorder}}`, 0)
      element.sheet.insertRule(`.bg-color-nav {background-color: ${this.theme.navBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-form {background-color: ${this.theme.formBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-page {background-color: ${this.theme.pageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-image {background-color: ${this.theme.imageBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-header {background-color: ${this.theme.headerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-footer {background-color: ${this.theme.footerBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button {background-color: ${this.theme.buttonBackground}}`, 0)
      element.sheet.insertRule(`.bg-color-button:focus {background-color: ${this.handleColor(this.theme.buttonBackground, -40)}}`, 0)
      element.sheet.insertRule(`.bg-color-button:hover {background-color: ${this.handleColor(this.theme.buttonBackground, -40)}}`, 0)
      element.sheet.insertRule(`.border-color-form:hover {border-color: ${this.handleColor(this.theme.formBorder, -40)}}`, 0)
      element.sheet.insertRule(`.border-color-form:focus {border-color: ${this.handleColor(this.theme.formBorder, -40)}}`, 0)
    },
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
    },
    patchTheme() {
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
        if (res.status === 200) {
          console.debug(res.data)
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
