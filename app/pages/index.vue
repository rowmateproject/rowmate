<template>
<div class="container mx-auto text-gray-250">
  <logo />
  <div v-if="$store.state.accessToken">
    <p class="mb-3">You are authenticated</p>
    <button @click="logout" class="bg-gray-800 rounded px-3 py-2 mb-4">Logout</button>
    <p class="mb-3">You can see the secret page</p>
    <nuxt-link to="/secret" class="bg-gradient-to-r from-purple-800 to-red-600 hover:to-gray-600 rounded px-3 py-2 font-medium">Secret</nuxt-link>
  </div>
  <div v-else>
    <p class="mb-3">You are not authenticated</p>
    <nuxt-link to="/signin" class="bg-purple-600 rounded px-3 py-2">Login</nuxt-link>
  </div>
</div>
</template>

<script>
const Cookie = process.client ? require('js-cookie') : undefined

export default {
  methods: {
    logout() {
      Cookie.remove('userAccessToken')
      this.$store.commit('updateAccessToken', null)
    }
  }
}
</script>
