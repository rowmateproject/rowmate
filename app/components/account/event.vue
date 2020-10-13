<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Events</h3>

  <div class="bg-svg-image bg-blue-500 rounded shadow p-3 lg:p-6 my-3 lg:my-6 mb-3">
    <h4 class="text-color-nav leading-none">Event Filter</h4>
    <event-filter @resultObject="handleEventFilterResult" @resetFilter="handleEventResetValue" />
  </div>

  <form @submit.prevent="submitForm" class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow">

    <div class="grid grid-cols-12 gap-4">

      <div class="col-span-12 lg:col-span-8">
        <VueTailwindPicker @change="(v) => handleStartDate(v)" :startFromMonday="true">
            <input type="text" v-model="startDateString" />
        </VueTailwindPicker>

        <time-form @minute="handleStartMinute" @hour="handleStartHour" :minute="startDate.minute" :hour="startDate.hour" direction="forward" title="Start"/>
        <p v-if="errors.startDateFull" class="text-red-500 text-xs italic">{{ $t('errorInvalidStartDate') }}</p>
      </div>

      <div class="col-span-12 lg:col-span-4 row-start-3 lg:row-start-1 lg:col-start-9">
        <event-repeat-form @repeatUnitNumber="handleRepeatUnit" @repeatIntervalNumber="handleRepeatInterval" :repeatUnit="repeatUnit" :repeatInterval="repeatInterval" />
      </div>

      <div class="col-span-12 lg:col-span-8">
        <date-form @minute="handleEndMinute" @hour="handleEndHour" @day="handleEndDay" @month="handleEndMonth" @year="handleEndYear" :minute="endDate.minute" :hour="endDate.hour" :day="endDate.day" :month="endDate.month" :year="endDate.year"
          direction="forward" minYear="2020" maxYear="2025" title="Veranstaltungs Ende" v-if="multiday"/>
        <time-form @minute="handleEndMinute" @hour="handleEndHour" :minute="endDate.minute" :hour="endDate.hour" direction="forward" title="Ende" v-else/>
        <p v-if="errors.endDateFull" class="text-red-500 text-xs italic">{{ $t('errorInvalidEndDate') }}</p>
      </div>

      <div class="col-span-12 lg:col-span-4 grid grid-cols-12 gap-3 justify-end">
        <div class="col-span-6 grid grid-cols-12 gap-2">
          <label class="col-span-12 text-color-form leading-none">Min. Teilnehmer</label>
          <input v-model="minParticipants" type="text" class="col-span-12 rounded border border-color-form focus:outline-none p-2">
        </div>
        <div class="col-span-6 grid grid-cols-12 gap-2">
          <label class="col-span-12 text-color-form leading-none">Max. Teilnehmer</label>
          <input v-model="maxParticipants" type="text" class="col-span-12 rounded border border-color-form focus:outline-none p-2">
        </div>
      </div>
    </div>


    <div class="col-span-12 lg:col-span-8">
      <input type="checkbox" v-model="multiday" />
      <label>Event dauert mehrere Tage</label>
    </div>

    <div class="grid grid-cols-12 gap-6 mt-6">
      <div class="col-span-12 lg:col-span-4">
        <h4 class="text-color-form leading-none">Ansprechpartner</h4>
        <user-filter @resultObject="handleUserFilterObject" :showResetButton="false" />
      </div>
      <div class="col-span-12 lg:col-span-8">
        <h4 class="text-color-form leading-none" for="eventFilter">Umfrage hinzufügen (optional)</h4>
        <question-filter @resultObject="handleQuestionFilterResult" @resetFilter="handleQuestionResetValue" />
      </div>
    </div>

    <div class="mt-8">
      <label class="text-color-form leading-none" for="location">Ort</label>
      <input v-model="location" type="text" placeholder="Ort hinzufügen" :class="[errors.location ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
      <p v-if="errors.location" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
    </div>

    <div v-for="value, index in availableLocales" :key="index" class="mt-8">
      <event-form :code="value.code" :title="titles[value.code].title" :description="descriptions[value.code].description" :titleError="errors.titles[value.code].title" :descriptionError="errors.descriptions[value.code].description"
        @titleString="handletitleString" @descriptionString="handleDescriptionString" />
    </div>

    <div class="flex justify-end mt-4">
      <button class="px-4 py-2 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
        {{ $t('save') }}
      </button>
    </div>
  </form>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'
import VueTailwindPicker from 'vue-tailwind-picker'

export default {
  data() {
    return {
      uuid: '',
      titles: {},
      descriptions: {},
      multiday: false,
      contactPerson: '',
      minParticipants: '',
      maxParticipants: '',
      repeatInterval: '',
      repeatUnit: '',
      location: '',
      pollId: '',
      startDateString: '',
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
          if (this.titles[locale.code].title.trim().length >= 3) {
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
          if (this.descriptions[locale.code].description.trim().length >= 3) {
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
    multiday: function() {
      this.multidayDate()
    },
    location: function() {
      if (this.location !== '') {
        if (this.location.trim().length >= 3) {
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
    multidayDate(value,param) {
      if (this.multiday === false) {
        if (value !== undefined && param !== undefined) {
          this.endDate[param] = value
        } else {
          this.endDate.year = this.startDate.year
          this.endDate.month = this.startDate.month
          this.endDate.day = this.startDate.day
        }
      }
    },
    handleStartDate(v) {
      this.startDateString = v
      let startdate = new Date(v)
      this.handleStartYear(startdate.getFullYear())
      this.handleStartMonth(startdate.getMonth())
      this.handleStartDay(startdate.getDay())

    },
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
      this.multidayDate(value,"day")
      this.startDate.day = value
    },
    handleStartMonth(value) {
      this.multidayDate(value,"month")
      this.startDate.month = value
    },
    handleStartYear(value) {
      this.multidayDate(value,"year")
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
    handleRepeatUnit(value) {
      this.repeatUnit = value
    },
    handleRepeatInterval(value) {
      this.repeatInterval = value
    },
    handletitleString(value) {
      this.titles[value.locale].title = value.title
    },
    handleDescriptionString(value) {
      this.descriptions[value.locale].description = value.description
    },
    handleUserFilterObject(value) {
      this.contactPerson = value.user.name
    },
    handleQuestionResetValue(value) {
      if (value === true) {
        this.pollId = ''
      }
    },
    handleQuestionFilterResult(value) {
      this.pollId = value._id
    },
    handleEventResetValue(value) {
      if (value === true) {
        this.availableLocales.forEach((locale) => {
          this.descriptions[locale.code].description = ''
          this.titles[locale.code].title = ''
        })

        this.repeatUnit = ''
        this.repeatInterval = ''
        this.contactPerson = ''
        this.minParticipants = ''
        this.maxParticipants = ''
        this.startDate.day = ''
        this.startDate.hour = ''
        this.startDate.minute = ''
        this.startDate.month = ''
        this.startDate.year = ''
        this.endDate.day = ''
        this.endDate.hour = ''
        this.endDate.minute = ''
        this.endDate.month = ''
        this.endDate.year = ''
        this.location = ''
        this.pollId = ''
        this.uuid = ''
      }
    },
    handleEventFilterResult(value) {
      this.uuid = value._id || ''
      this.titles = value.titles || {}
      this.descriptions = value.descriptions || {}
      this.minParticipants = value.min_participants || ''
      this.maxParticipants = value.max_participants || ''
      this.repeatInterval = value.repeat_interval || ''
      this.contactPerson = value.contact_person || ''
      this.repeatUnit = value.repeat_unit || ''
      this.startDate.day = new Date(Date.parse(value.start_time)).getDate()
      this.startDate.hour = this.zeroPad(new Date(Date.parse(value.start_time)).getHours(), 2)
      this.startDate.minute = this.zeroPad(new Date(Date.parse(value.start_time)).getMinutes(), 2)
      this.startDate.month = new Date(Date.parse(value.start_time)).getMonth() + 1
      this.startDate.year = new Date(Date.parse(value.start_time)).getFullYear()
      this.endDate.day = new Date(Date.parse(value.end_time)).getDate()
      this.endDate.hour = this.zeroPad(new Date(Date.parse(value.end_time)).getHours(), 2)
      this.endDate.minute = this.zeroPad(new Date(Date.parse(value.end_time)).getMinutes(), 2)
      this.endDate.month = new Date(Date.parse(value.end_time)).getMonth() + 1
      this.endDate.year = new Date(Date.parse(value.end_time)).getFullYear()
      this.location = value.location || ''
      this.pollId = value.poll_id || ''
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
        let uuid = null

        try {
          uuid = this.buf2hex(uuidParse(this.uuid))
        } catch (e) {
          console.debug(e.message)
        }

        if (!uuid) {
          this.$axios({
            method: 'POST',
            url: `${process.env.API_URL}/event`,
            data: {
              titles: this.titles,
              poll_id: this.pollId,
              location: this.location,
              repeat_unit: this.repeatUnit,
              descriptions: this.descriptions,
              repeat_interval: this.repeatInterval,
              min_participants: this.minParticipants,
              max_participants: this.maxParticipants,
              contact_person: this.contactPerson,
              start_time: this.startDateFull,
              end_time: this.endDateFull
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              this.uuid = res.data._id || ''
            } else {
              console.debug(res.data)
            }
          })
        } else {
          this.$axios({
            method: 'PATCH',
            url: `${process.env.API_URL}/event/${uuid}`,
            data: {
              titles: this.titles,
              poll_id: this.pollId,
              location: this.location,
              repeat_unit: this.repeatUnit,
              descriptions: this.descriptions,
              repeat_interval: this.repeatInterval,
              min_participants: this.minParticipants,
              max_participants: this.maxParticipants,
              contact_person: this.contactPerson,
              start_time: this.startDateFull,
              end_time: this.endDateFull
            },
            validateStatus: () => true
          }).then(res => {
            if (res.status === 200) {
              console.debug(res.data)
            } else if (res.status === 204) {
              console.debug('Nothing to update already uptodate')
            }
          })
        }
      }
    }
  },
  components: {
    VueTailwindPicker
  }
}
</script>
