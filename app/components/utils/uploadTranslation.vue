<template>
<div class="bg-color-form mt-3 lg:mt-8 rounded shadow">
  <div class="grid grid-cols-2 gap-3 sm:gap-6 p-3 sm:p-6">
    <form enctype="multipart/form-data">
      <label class="flex justify-center items-center bg-color-header text-color-button cursor-pointer rounded px-4 py-2">
        <span class="leading-normal">Import Übersetzungen</span>
        <input type="file" @input="uploadTranslation($event.target.files)" class="hidden">
      </label>
    </form>
    <button @click="exportTranslation" class="px-4 py-2 bg-color-button text-color-button rounded hover:bg-gray-700 focus:outline-none focus:bg-gray-700">Export Übersetzungen</button>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {}
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    uploadTranslation(file) {
      const formData = new FormData()
      formData.append('file', file[0])

      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/lang/import/${this.currentLocale}`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        validateStatus: () => true
      }).then(res => {
        if (res.status === 200) {
          this.$emit('importedTranslation', res.data)
        } else {
          console.debug(res.data)
        }
      })
    },
    exportTranslation(file) {
      this.$axios({
        method: 'GET',
        url: `${process.env.API_URL}/lang/export/${this.currentLocale}`,
        resType: 'blob',
        validateStatus: () => true
      }).then(res => {
        if (res.status === 200) {
          const url = window.URL.createObjectURL(new Blob([res.data]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', `export.${this.currentLocale}.po`)
          document.body.appendChild(link)
          link.click()
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
