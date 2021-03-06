<template>
<ul v-if="events.length > 0" class="siblings:mt-3 md:siblings:mt-5 lg:siblings:mt-8">
  <li v-for="value, index in events" :key="index" class="bg-color-form rounded shadow p-3 lg:p-6">
    <div class="grid grid-cols-12 gap-3 lg:gap-6">
      <div class="col-span-12 grid grid-cols-12 gap-3 lg:gap-6">
        <h1 class="col-span-6 md:col-span-9 xl:col-span-10 text-color-sale font-bold leading-none text-xl sm:text-2xl md:text-3xl xl:text-4xl">
          {{ value.title }}
        </h1>
        <div class="col-span-6 md:col-span-3 xl:col-span-2 text-right">
          <button @click="subscribeEvent(value._id, index)" :class="[value.subscribed ? 'bg-color-header text-color-nav' : 'bg-color-button text-color-button']"
            class="rounded focus:outline-none px-4 py-2">{{ value.subscribed ? 'Zugesagt' : 'Jetzt Anmelden' }}</button>
        </div>
      </div>
      <ul class="col-span-12 xl:col-span-9 grid grid-cols-12 gap-3 lg:gap-6 mb-3 lg:mb-6">
        <li class="col-span-12">
          <p class="text-color-header font-medium">Zeitpunkt</p>
          <span class="text-color-title text-md sm:col-span-6 lg:text-lg md:text-xl md:font-bold">{{ makeStartEndDate(value.start_time) }}</span>
        </li>
        <li v-if="value.contact_person" class="col-span-12 sm:col-span-6 xl:col-span-4">
          <p class="text-color-header font-medium">Ansprechpartner</p>
          <span class="text-color-title text-md sm:col-span-6 lg:text-lg md:text-xl md:font-bold">{{ value.contact_person }}</span>
        </li>
        <li v-if="value.modified_at" class="col-span-12 sm:col-span-6 xl:col-span-4">
          <p class="text-color-header font-medium">Geändert am</p>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold">{{ makeDateTime(value.modified_at).join(' ') }}</span>
        </li>
        <li v-if="value.created_at && !value.modified_at" class="col-span-12 sm:col-span-6 xl:col-span-4">
          <p class="text-color-header font-medium">Erstellt am</p>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold">{{ makeDateTime(value.created_at).join(' ') }}</span>
        </li>
        <li v-if="value.min_participants > 0" class="col-span-12 sm:col-span-6 xl:col-span-4">
          <p class="text-color-header font-medium">Teilnehmeranzahl</p>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold">{{ value.min_participants }}</span>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold" v-if="value.max_participants > 0"> - {{ value.max_participants }}</span>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold"> {{ value.min_participants > 1 ? 'Personen' : 'Person' }}</span>
        </li>
        <li v-if="value.repeat_interval > 0" class="col-span-12 sm:col-span-6 xl:col-span-4">
          <p class="text-color-header font-medium">Wiederholung</p>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold">alle {{ value.repeat_interval }} {{ $t(value.repeat_unit) }}</span>
        </li>
        <li class="col-span-12">
          <p class="text-color-header font-medium">Veranstaltungsort</p>
          <span class="text-color-title text-md sm:text-lg md:text-xl md:font-bold">{{ value.location }}</span>
        </li>
      </ul>
    </div>
    <h2 class="text-color-header font-medium">Beschreibung</h2>
    <p class="text-color-title text-md sm:text-lg">{{ value.description }}</p>
  </li>
</ul>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      eventItems: [],
      eventItemsBackup: []
    }
  },
  mounted() {
    let requestUrl = `${process.env.API_URL}/events/`

    if (this.$props.eventSubscriptions === true) {
      requestUrl = `${process.env.API_URL}/subscription/events/`
    }

    this.$axios({
      method: 'GET',
      url: requestUrl,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.events = res.data
        this.eventItemsBackup = res.data
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    events: {
      get() {
        return this.eventItems
      },
      set(value) {
        this.eventItems = value
      }
    }
  },
  watch: {
    resetFilter: function(value) {
      if (value === true) {
        this.events = this.eventItemsBackup
      }
    },
    eventFilter: function(value) {
      if (value.length > 0) {
        this.events = value
      }
    }
  },
  props: ['eventFilter', 'resetFilter', 'eventSubscriptions'],
  methods: {
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    makeId(value, locale) {
      return `${value}-${locale}`
    },
    buf2hex(buffer) {
      const byteArray = new Uint8Array(buffer)
      const hexParts = []

      for (let i = 0; i < byteArray.length; i++) {
        const hex = byteArray[i].toString(16)
        const paddedHex = ('00' + hex).slice(-2)
        hexParts.push(paddedHex)
      }

      return hexParts.join('')
    },
    subscribeEvent(value, index) {
      let uuid = null

      try {
        uuid = this.buf2hex(uuidParse(value))
      } catch (e) {
        return e.message
      }

      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/subscription/event/${uuid}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          this.events[index]['subscribed'] = res.data
        } else {
          console.debug(res.data)
        }
      })
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
