<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Dashboard</h3>

  <div class="mt-8">
    <div class="flex flex-wrap -mx-6">
      <div class="w-full px-6 sm:w-1/2 xl:w-1/3">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-color-form">
          <div class="flex items-center justify-center rounded-full bg-red-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'users']" class="text-color-nav text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-color-page">{{ users.length }}</h4>
            <div class="text-color-title">Registrierte Nutzer</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 sm:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-color-form">
          <div class="flex items-center justify-center rounded-full bg-orange-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'network-wired']" class="text-color-nav text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-color-page">2.021</h4>
            <div class="text-color-title">Registrierte Vereine</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 xl:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-color-form">
          <div class="flex items-center justify-center rounded-full bg-green-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'calendar-alt']" class="text-color-nav text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-color-page">542</h4>
            <div class="text-color-title">Veranstaltungen</div>
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
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/manage/users/list`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.users = res.data.users
      } else {
        console.debug(res.data)
      }
    })
  }
}
</script>
