<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Dashboard</h3>

  <div class="mt-8">
    <div class="flex flex-wrap -mx-6">
      <div class="w-full px-6 sm:w-1/2 xl:w-1/3">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-red-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'users']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">{{ users.length }}</h4>
            <div class="text-gray-500">Registrierte Nutzer</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 sm:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-orange-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'network-wired']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">2.021</h4>
            <div class="text-gray-500">Registrierte Vereine</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 xl:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-green-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'calendar-alt']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">542</h4>
            <div class="text-gray-500">Veranstaltungen</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="mt-8"></div>
</div>
</template>

<script>
export default {
  data() {
    return {
      users: []
    }
  },
  mounted() {
    this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

    this.$axios.$get(`${process.env.API_URL}/manage/users/list`).then(res => {
      this.users = res.users
    })
  },
  computed: {
    accessToken() {
      return this.$store.state.accessToken
    }
  }
}
</script>
