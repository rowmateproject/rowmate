<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Sprache</h3>

  <upload-translation @importedTranslation="handleImportedTranslation" />

  <form @submit.prevent="submitForm" class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow-md">
    <h2 class="mb-6 flex justify-start items-center text-color-form text-xl">
      <img :src="makePath(currentLocale)" :alt="currentLocale" class="h-5 mr-1">
      <span>Übersetzungen</span>
    </h2>

    <ul v-if="translations" class="grid grid-cols-6 gap-6">
      <li v-if="translations.input" v-for="(value, key) in translations.input" class="col-span-6 sm:col-span-3">
        <label class="text-color-form" :for="makeId('title', currentLocale)">
          {{ key }}
        </label>
        <input v-model="translations.input[key]" type="text" placeholder="Übersetzung eingeben" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      </li>
      <li v-if="translations.textarea" v-for="(value, key) in translations.textarea" class="col-span-6">
        <label class="text-color-form" :for="makeId('title', currentLocale)">
          {{ key }}
        </label>
        <textarea v-model="translations.textarea[key]" type="text" placeholder="Übersetzung eingeben" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1"></textarea>
      </li>
    </ul>

    <div class="flex justify-end mt-4">
      <button class="px-4 py-2 bg-color-button text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
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
      translations: {}
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/lang/${this.currentLocale}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.translations = res.data
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    makeId(value, locale) {
      return `${value}-${locale}`
    },
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    handleImportedTranslation(value) {
      this.translations = value
    },
    submitForm() {
      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/lang/${this.currentLocale}`,
        data: {
          input: this.translations.input,
          textarea: this.translations.textarea
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
