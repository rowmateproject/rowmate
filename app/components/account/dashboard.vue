<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Dashboard</h3>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-6 mt-3 lg:mt-8 mb-12">
    <div>
      <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-color-form">
        <div class="flex items-center justify-center rounded-full bg-red-600 bg-opacity-75 w-16 h-16">
          <fa :icon="['fas', 'users']" class="text-color-nav text-3xl" />
        </div>

        <div class="mx-5">
          <h4 class="text-2xl font-semibold text-color-page">{{ stats.users }}</h4>
          <div class="text-color-title">Registrierte Nutzer</div>
        </div>
      </div>
    </div>

    <div>
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

    <div>
      <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-color-form">
        <div class="flex items-center justify-center rounded-full bg-green-600 bg-opacity-75 w-16 h-16">
          <fa :icon="['fas', 'calendar-alt']" class="text-color-nav text-3xl" />
        </div>

        <div class="mx-5">
          <h4 class="text-2xl font-semibold text-color-page">{{ stats.events }}</h4>
          <div class="text-color-title">Anstehende Events</div>
        </div>
      </div>
    </div>
  </div>

  <h3 class="text-3xl font-medium text-color-title">Umfragen</h3>
  <vote-results class="mb-12" />

  <h3 class="text-3xl font-medium text-color-title">Events</h3>

  <div class="mt-3 lg:mt-4 p-3 lg:px-6 lg:pb-6 lg:pt-4 bg-svg-image bg-blue-500 rounded-md shadow">
    <h4 class="text-color-nav">Event Filter</h4>
    <event-filter @resultObject="handleResult" @resetFilter="handleReset" :eventSubscriptions="true" />
  </div>

  <event-cards :eventFilter="events" :resetFilter="reset" :eventSubscriptions="true" />
</div>
</template>

<script>
export default {
  data() {
    return {
      stats: {
        users: 0,
        events: 0
      },
      events: [],
      reset: true
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
