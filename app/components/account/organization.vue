<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Organisation</h3>

  <div class="bg-color-image mt-3 lg:mt-8 px-6 pb-6 pt-4 rounded shadow">
    <h4 class="text-xl mb-1">Hinweis</h4>
    <p>Die Angabe des Landes und der genauen Adresse ist wichtig, damit wir den Datenschutz und rechtliche Bestimmungen für dich erfüllen können.</p>
  </div>

  <h4 class="mt-3 lg:mt-8 text-color-form text-2xl font-medium mb-4">Adresse</h4>
  <address-form />

  <h4 class="mt-3 lg:mt-8 text-color-form text-2xl font-medium mb-4">Verwaltung</h4>
  <organization-form />
</div>
</template>

<script>
export default {
  data() {
    return {
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
  }
}
</script>
