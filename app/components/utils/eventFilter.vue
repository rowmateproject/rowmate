<template>
<div class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow">
  <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
    <label class="text-color-form" for="eventFilter">Event Filter</label>

    <div class="flex flex-wrap items-stretch w-full relative mt-2">
      <input v-model="searchTerm" @input="lookupEvent" type="text" class="flex-shrink flex-grow flex-auto leading-normal flex-1 border rounded-l focus:outline-none p-2">
      <div class="flex">
        <button @click="clearSearchTerm" class="flex items-center leading-normal bg-gray-400 text-gray-800 focus:outline-none rounded-r px-3">Zurücksetzen</button>
      </div>
    </div>

    <ul v-if="events.length > 0" class="w-full absolute z-30 mt-1">
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
    }
  },
  props: ['eventSubscriptions'],
  methods: {
    toggleSearch() {
      this.events = []
    },
    clearSearchTerm() {
      this.searchTerm = ''
      this.$emit('resetFilter', true)
    },
    setSerchTerm(value, datetime, index) {
      this.searchTerm = `${value}, (${datetime})`
      this.$emit('resultObject', this.events[index])
      this.$emit('resetFilter', false)
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
        let requestUrl = `${process.env.API_URL}/lookup/events/${this.currentLocale}`

        if (this.$props.eventSubscriptions === true) {
          requestUrl = `${process.env.API_URL}/lookup/subscriptions/${this.currentLocale}`
        }

        this.$axios({
          method: 'POST',
          url: requestUrl,
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
