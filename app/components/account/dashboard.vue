<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Dashboard</h3>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 lg:gap-6 my-3 lg:my-6">
    <div class="grid grid-cols-12 gap-3 bg-color-form shadow rounded p-3 lg:p-4">
      <div class="col-span-12 flex items-center">
        <div class="mr-3 lg:mr-4">
          <div class="flex items-center justify-center rounded-full bg-red-600 w-16 h-16">
            <fa :icon="['fas', 'users']" class="text-color-nav text-3xl" />
          </div>
        </div>

        <div class="flex flex-col justify-center">
          <h4 class="text-2xl font-semibold leading-tight text-color-page">{{ stats.users }}</h4>
          <div class="text-color-title leading-tight">Registrierte Nutzer</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-3 bg-color-form shadow rounded p-3 lg:p-4">
      <div class="col-span-12 flex items-center">
        <div class="mr-3 lg:mr-4">
          <div class="flex items-center justify-center rounded-full bg-indigo-600 w-16 h-16">
            <fa :icon="['fas', 'network-wired']" class="text-color-nav text-3xl" />
          </div>
        </div>

        <div class="flex flex-col justify-center">
          <h4 class="text-2xl font-semibold leading-tight text-color-page">2.021</h4>
          <div class="text-color-title leading-tight">Registrierte Vereine</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-3 bg-color-form shadow rounded p-3 lg:p-4">
      <div class="col-span-12 flex items-center">
        <div class="mr-3 lg:mr-4">
          <div class="flex items-center justify-center rounded-full bg-green-600 w-16 h-16">
            <fa :icon="['fas', 'calendar-alt']" class="text-color-nav text-3xl" />
          </div>
        </div>

        <div class="flex flex-col justify-center">
          <h4 class="text-2xl font-semibold leading-tight text-color-page">{{ stats.events }}</h4>
          <div class="text-color-title leading-tight">Anstehende Events</div>
        </div>
      </div>
    </div>
  </div>

  <h3 class="text-lg sm:text-xl lg:text-2xl font-medium text-color-title mb-2">Umfragen</h3>
  <vote-results class="mb-3 sm:mb-8" />

  <h3 class="text-lg sm:text-xl lg:text-2xl font-medium text-color-title mb-2">Events</h3>
  <div class="p-3 lg:px-6 lg:pb-6 lg:pt-4 bg-svg-image bg-blue-500 rounded-md shadow mb-3 sm:mb-6">
    <h4 class="text-color-nav leading-none">Event Filter</h4>
    <event-filter @resultObject="handleResult" @resetFilter="handleReset" :eventSubscriptions="true" :borderSettings="false" />
  </div>

  <event-cards :eventFilter="events" :resetFilter="reset" :eventSubscriptions="true" />
</div>
</template>

<script>
import VueTailwindPicker from 'vue-tailwind-picker'
export default {
  components: {
    VueTailwindPicker
  },
  data() {
    return {
      stats: {
        users: 0,
        events: 0
      },
      events: [],
      reset: true,
      checkin: ''
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/stats/dashboard`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.stats.users = res.data.users
        this.stats.events = res.data.events
      } else {
        console.debug(res.data)
      }
    })
  },
  methods: {
    handleReset(value) {
      this.reset = value
    },
    handleResult(value) {
      this.events = [value]
    },
    makeDateTime(value) {
      const d = new Date(Date.parse(value))

      const day = new Intl.DateTimeFormat(this.currentLocale, {
        day: 'numeric'
      }).format(d)

      const month = new Intl.DateTimeFormat(this.currentLocale, {
        month: 'short'
      }).format(d)

      const year = new Intl.DateTimeFormat(this.currentLocale, {
        year: 'numeric'
      }).format(d)

      const time = new Intl.DateTimeFormat(this.currentLocale, {
        minute: 'numeric',
        hour: 'numeric'
      }).format(d)

      return [day, month, year, time]
    },
    makeStartEndDate(eventDate) {
      const [day, month, year, time] = this.makeDateTime(eventDate)
      const dateString = `${day}. ${month}. ${year}, ${time} Uhr`

      return dateString
    }
  }
}
</script>
