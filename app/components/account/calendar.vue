<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Kalender</h3>

  <ul>
    <li v-for="value, index in events" :key="index" class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow-md">
      <div class="grid grid-cols-12 gap-x-6">
        <h1 class="col-span-10 text-color-sale font-bold text-4xl mb-8">
          {{ makeStartEndDate(value.start_time, value.end_time)[0] }}
          {{ makeStartEndDate(value.start_time, value.end_time)[1] }}
          {{ makeStartEndDate(value.start_time, value.end_time)[2] }}
          <span class="ml-2">- {{ value.titles[currentLocale].title }}</span>
        </h1>
        <div class="col-span-2 text-right">
          <button class="bg-color-button text-color-button rounded-md focus:outline-none px-4 py-2">Jetzt Anmelden</button>
        </div>
        <ul class="col-span-8 grid grid-cols-10 gap-6 mb-6">
          <li v-if="value.contact_person" class="col-span-4">
            <p class="text-color-header font-medium">Ansprechpartner</p>
            <span class="text-color-title text-xl font-bold">{{ value.contact_person }}</span>
          </li>
          <li v-if="value.modified_at" class="col-span-3">
            <p class="text-color-header font-medium">Geändert am</p>
            <span class="text-color-title text-xl font-bold">{{ makeDateTime(value.modified_at).join(' ') }}</span>
          </li>
          <li v-else class="col-span-3">
            <p class="text-color-header font-medium">Erstellt am</p>
            <span class="text-color-title text-xl font-bold">{{ makeDateTime(value.created_at).join(' ') }}</span>
          </li>
          <li v-if="value.min_participants > 0" class="col-span-3">
            <p class="text-color-header font-medium">Teilnehmeranzahl</p>
            <span class="text-color-title text-xl font-bold">{{ value.min_participants }}</span>
            <span class="text-color-title text-xl font-bold" v-if="value.max_participants > 0"> - {{ value.max_participants }}</span>
            <span class="text-color-title text-xl font-bold"> {{ value.min_participants > 1 ? 'Personen' : 'Person' }}</span>
          </li>
          <li v-if="value.repeat_interval > 0" class="col-span-4">
            <p class="text-color-header font-medium">Wiederholung</p>
            <span class="text-color-title text-xl font-bold">alle {{ value.repeat_interval }} {{ $t(value.repeat_unit) }}</span>
          </li>
          <li class="col-span-6">
            <p class="text-color-header font-medium">Veranstaltungsort</p>
            <span class="text-color-title text-xl font-bold">{{ value.location }}</span>
          </li>
        </ul>
      </div>
      <h2 class="text-color-header font-medium">Beschreibung</h2>
      <p class="text-color-title text-lg">{{ value.descriptions[currentLocale].description }}</p>
    </li>
  </ul>
</div>
</template>

<script>
export default {
  data() {
    return {
      events: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/events/${this.currentLocale}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        console.log(res.data)
        this.events = res.data
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    makeId(value, locale) {
      return `${value}-${locale}`
    },
    makeDateTime(value) {
      const d = new Date(value)

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
        minute: '2-digit',
        hour: 'numeric'
      }).format(d)

      return [day, month, year, time]
    },
    makeStartEndDate(startDate, endDate) {
      const [dayStart, monthStart, yearStart, timeStart] = this.makeDateTime(startDate)
      const [dayEnd, monthEnd, yearEnd, timeEnd] = this.makeDateTime(endDate)

      let daysString = null
      let monthsString = null
      let yearString = null

      if (yearStart === yearEnd && monthStart === monthEnd) {
        daysString = `${dayStart}. bis ${dayEnd}.`
        monthsString = `${monthStart}`
        yearString = `${yearStart}`
      }

      return [daysString, monthsString, yearStart]
    }
  }
}
</script>
