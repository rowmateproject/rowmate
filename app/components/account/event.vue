<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">{{ $t('createEvent') }}</h3>

  <form @submit.prevent="submitForm" class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow-md">
    <div class="flex mb-8">
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'glass-cheers']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Was ist der Anlass?</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'calendar-alt']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Wann ist der Termin?</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'question-circle']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Umfrage erstellen</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'clipboard-check']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Event anlegen</h2>
        </div>
      </div>
    </div>

    <div>
      <div class="grid grid-cols-6 gap-4 mb-8">
        <div class="col-span-4">
          <date-form @minute="handleStartMinute" @hour="handleStartHour" @day="handleStartDay" @month="handleStartMonth" @year="handleStartYear" :minute="startDate.minute" :hour="startDate.hour" :day="startDate.day" :month="startDate.month"
            :year="startDate.year" direction="forward" minYear="2020" maxYear="2025" title="Beginn" />
          <p v-if="errors.startDateFull" class="text-red-500 text-xs italic">{{ $t('errorInvalidStartDate') }}</p>
        </div>
        <div class="col-span-4">
          <date-form @minute="handleEndMinute" @hour="handleEndHour" @day="handleEndDay" @month="handleEndMonth" @year="handleEndYear" :minute="endDate.minute" :hour="endDate.hour" :day="endDate.day" :month="endDate.month" :year="endDate.year"
            direction="forward" minYear="2020" maxYear="2025" title="Ende" />
          <p v-if="errors.endDateFull" class="text-red-500 text-xs italic">{{ $t('errorInvalidEndDate') }}</p>
        </div>
      </div>

      <div>
        <label class="text-color-form" for="location">Ort</label>
        <input v-model="location" type="text" placeholder="Ort hinzufügen" :class="[errors.location ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.location" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
      </div>

      <div v-for="value, index in availableLocales" :key="index" class="mt-8">
        <!-- {{ titles[value.code].title }} && {{ descriptions[value.code].description }} -->
        <event-form :code="value.code" :title="titles[value.code].title" :description="descriptions[value.code].description" :titleError="errors.titles[value.code].title" :descriptionError="errors.descriptions[value.code].description"
          @titleString="handleTitleString" @descriptionString="handleDescriptionString" />
      </div>

      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
          {{ $t('save') }}
        </button>
      </div>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {
      titles: {},
      descriptions: {},
      location: '',
      endDate: {
        day: null,
        hour: null,
        minute: null,
        month: null,
        year: null
      },
      startDate: {
        day: null,
        hour: null,
        minute: null,
        month: null,
        year: null
      },
      errors: {
        titles: {},
        descriptions: {},
        startDateFull: false,
        endDateFull: false
      }
    }
  },
  created() {
    this.availableLocales.forEach((locale) => {
      this.$set(this.titles, locale.code, {
        title: ''
      })

      this.$set(this.descriptions, locale.code, {
        description: ''
      })

      this.$set(this.errors.titles, locale.code, {
        title: false
      })

      this.$set(this.errors.descriptions, locale.code, {
        description: false
      })

      this.$watch(`titles.${locale.code}.title`, function() {
        if (this.titles[locale.code].title !== '') {
          if (this.titles[locale.code].title.trim().length >= 7) {
            this.errors.titles[locale.code].title = false
          } else {
            this.errors.titles[locale.code].title = true
          }
        } else {
          this.errors.titles[locale.code].title = false
        }
      }, {
        deep: true
      })

      this.$watch(`descriptions.${locale.code}.description`, function() {
        if (this.descriptions[locale.code].description.trim() !== '') {
          if (this.descriptions[locale.code].description.trim().length >= 7) {
            this.errors.descriptions[locale.code].description = false
          } else {
            this.errors.descriptions[locale.code].description = true
          }
        } else {
          this.errors.descriptions[locale.code].description = false
        }
      }, {
        deep: true
      })
    })
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/event/latest`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.titles = res.data.titles || {}
        this.descriptions = res.data.descriptions || {}
        this.startDate.day = new Date(Date.parse(res.data.start_time)).getDate()
        this.startDate.hour = this.zeroPad(new Date(Date.parse(res.data.start_time)).getHours(), 2)
        this.startDate.minute = this.zeroPad(new Date(Date.parse(res.data.start_time)).getMinutes(), 2)
        this.startDate.month = new Date(Date.parse(res.data.start_time)).getMonth() + 1
        this.startDate.year = new Date(Date.parse(res.data.start_time)).getFullYear()
        this.endDate.day = new Date(Date.parse(res.data.end_time)).getDate()
        this.endDate.hour = this.zeroPad(new Date(Date.parse(res.data.end_time)).getHours(), 2)
        this.endDate.minute = this.zeroPad(new Date(Date.parse(res.data.end_time)).getMinutes(), 2)
        this.endDate.month = new Date(Date.parse(res.data.end_time)).getMonth() + 1
        this.endDate.year = new Date(Date.parse(res.data.end_time)).getFullYear()
        this.location = res.data.location || ''
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    availableLocales() {
      return this.$i18n.locales
    },
    startDateFull() {
      if (this.startDate.year !== null && this.startDate.month !== null && this.startDate.day !== null) {
        return new Date(Date.UTC(this.startDate.year, this.startDate.month - 1, this.startDate.day, this.startDate.hour, this.startDate.minute, 0))
      } else {
        return null
      }
    },
    endDateFull() {
      if (this.endDate.year !== null && this.endDate.month !== null && this.endDate.day !== null) {
        return new Date(Date.UTC(this.endDate.year, this.endDate.month - 1, this.endDate.day, this.endDate.hour, this.endDate.minute, 0))
      } else {
        return null
      }
    }
  },
  watch: {
    location: function() {
      if (this.location !== '') {
        if (this.location.trim().length >= 7) {
          this.errors.location = false
        } else {
          this.errors.location = true
        }
      } else {
        this.errors.location = false
      }
    },
    startDateFull: function() {
      if (this.startDateFull !== null) {
        this.errors.startDateFull = false
      } else {
        this.errors.startDateFull = true
      }

      if (this.endDateFull !== null && this.startDateFull > this.endDateFull) {
        this.errors.endDateFull = false
      } else {
        this.errors.endDateFull = true
      }
    },
    endDateFull: function() {
      if (this.endDateFull !== null && this.startDateFull < this.endDateFull) {
        this.errors.endDateFull = false
      } else {
        this.errors.endDateFull = true
      }
    }
  },
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

      return hexParts.join('');
    },
    zeroPad(num, places) {
      return String(num).padStart(places, '0')
    },
    handleStartMinute(value) {
      this.startDate.minute = value
    },
    handleStartHour(value) {
      this.startDate.hour = value
    },
    handleStartDay(value) {
      this.startDate.day = value
    },
    handleStartMonth(value) {
      this.startDate.month = value
    },
    handleStartYear(value) {
      this.startDate.year = value
    },
    handleEndMinute(value) {
      this.endDate.minute = value
    },
    handleEndHour(value) {
      this.endDate.hour = value
    },
    handleEndDay(value) {
      this.endDate.day = value
    },
    handleEndMonth(value) {
      this.endDate.month = value
    },
    handleEndYear(value) {
      this.endDate.year = value
    },
    handleTitleString(value) {
      this.titles[value.locale].title = value.title
      // console.log(value)
    },
    handleDescriptionString(value) {
      this.descriptions[value.locale].description = value.description
      // console.log(value)
    },
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      this.availableLocales.forEach((locale) => {
        if (!this.titles[locale.code].title) {
          this.errors.titles[locale.code].title = true
        }

        if (!this.descriptions[locale.code].description) {
          this.errors.descriptions[locale.code].description = true
        }
      })

      if (!this.location) {
        this.errors.location = true
      }

      if (!this.startDateFull) {
        this.errors.startDateFull = true
      }

      if (!this.endDateFull) {
        this.errors.endDateFull = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/event`,
          data: {
            titles: this.titles,
            location: this.location,
            descriptions: this.descriptions,
            start_time: this.startDateFull,
            end_time: this.endDateFull
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            console.debug(res.data)
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
