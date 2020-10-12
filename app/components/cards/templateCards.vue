<template>
<ul>
  <li v-for="value, index in templateItems" :key="index" class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow-md grid grid-cols-12 gap-x-6">
    <div class="col-span-8">
      <h2 class="flex justify-start items-center text-color-header font-medium" :for="makeId('locale', value.locale)">
        <img v-if="value.locale !== 'undefined'" :src="makePath(value.locale)" :alt="value.locale" class="h-4 mr-1">
        <span>Betreff</span>
      </h2>
      <h1 class="text-color-sale font-bold text-2xl mb-4">{{ value.subject }}</h1>
    </div>

    <div class="col-span-4 text-right">
      <button @click="deleteTemplate(index)" class="bg-red-600 text-white rounded focus:outline-none px-4 py-2 mr-2">Löschen</button>
      <button @click="editTemplate(index)" class="bg-color-nav text-color-nav rounded focus:outline-none px-4 py-2">Bearbeiten</button>
    </div>

    <div class="col-span-12">
      <h2 class="text-color-header font-medium">Nachricht</h2>
      <p class="text-color-title text-lg">{{ value.message }}</p>
    </div>
  </li>
</ul>
</template>

<script>
export default {
  computed: {
    templateItems() {
      return this.$props.templates
    },
    currentLocale() {
      return this.$i18n.locale
    }
  },
  props: ['templates'],
  methods: {
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    makeId(value, locale) {
      return `${value}-${locale}`
    },
    editTemplate(index) {
      this.$emit('resultObject', this.templateItems[index])
    },
    deleteTemplate(index) {
      this.$emit('deleteResultId', this.templateItems[index]._id)
    }
  }
}
</script>
