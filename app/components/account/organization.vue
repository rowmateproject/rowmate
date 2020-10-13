<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Organisation</h3>

  <div class="bg-color-image mt-3 md:mt-6 lg:mt-8 px-3 lg:px-6 pb-3 lg:pb-6 pt-2 lg:pt-4 rounded shadow">
    <h4 class="text-xl mb-1">Hinweis</h4>
    <p>Die Angabe des Landes und der genauen Adresse ist wichtig, damit wir den Datenschutz und rechtliche Bestimmungen für dich erfüllen können.</p>
  </div>

  <div class="mt-3 md:mt-6 lg:mt-8">
    <h4 class="text-lg sm:text-xl lg:text-2xl font-medium text-color-title mb-2">Adresse</h4>
    <address-form @organizationObject="handleOrganizationObject" />
  </div>

  <div v-if="organization._id" class="mt-3 md:mt-6 lg:mt-8">
    <h4 class="text-lg sm:text-xl lg:text-2xl font-medium text-color-title mb-2">Verwaltung</h4>
    <organization-form :organizationObject="organization" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      organization: {
        _id: ''
      }
    }
  },
  methods: {
    handleOrganizationObject(value) {
      this.organization = value
    }
  }
}
</script>
