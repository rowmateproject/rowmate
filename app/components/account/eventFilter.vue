<template>
<div class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow">
  <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
    <label class="text-color-form" for="eventFilter">Event Suche</label>
    <input v-model="searchTerm" @input="lookupEvent" @focus="clearSearchTerm" type="text" class="w-full rounded border focus:outline-none p-2 mt-2">

    <ul v-if="events.length > 0" class="w-full absolute">
      <li v-for="value, index in events" @click="setSerchTerm(value.titles[currentLocale].title, makeEventTime(value.event_time), index)" :key="index" class="hover:bg-gray-300 bg-color-form border shadow p-2">
        <span class="text-color-form">{{ value.titles[currentLocale].title }} ({{ makeEventTime(value.event_time) }})</span>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      events: [],
      searchTerm: null
    }
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    availableLocales() {
      return this.$i18n.locales
    },
  },
  methods: {
    toggleSearch() {
      this.events = []
    },
    clearSearchTerm() {
      this.searchTerm = ''
    },
    setSerchTerm(value, datetime, index) {
      this.searchTerm = `${value}, (${datetime})`
      this.$emit('resultObject', this.events[index])
      this.clearSearchTerm()
      this.toggleSearch()
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
    makeEventTime(eventDate) {
      const [day, month, year, time] = this.makeDateTime(eventDate)
      const dateString = `${day}. ${month}. ${year}, ${time} Uhr`

      return dateString
    },
    lookupEvent() {
      if (this.searchTerm.length > 0) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/events/${this.currentLocale}`,
          data: {
            query: this.searchTerm
          },
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.events = res.data || []
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.events = []
      }
    }
  }
}
</script>
