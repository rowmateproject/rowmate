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
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-4">
        <date @dateObject="handleStartDate" :day="startDate.day" :month="startDate.month" :year="startDate.year" direction="forward" minYear="2020" maxYear="2025" title="Startzeit" />
        <date @dateObject="handleEndDate" :day="endDate.day" :month="endDate.month" :year="endDate.year" direction="forward" minYear="2020" maxYear="2025" title="Endzeit" />
      </div>

      <div class="mb-4">
        <label class="text-color-form" for="title">Titel</label>
        <input type="text" placeholder="Titel eingeben" maxlength="64" autocomplete="off" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.title" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
      </div>
      <div class="mb-4">
        <label class="text-color-form" for="location">Ort</label>
        <input type="text" placeholder="Ort hinzufügen" maxlength="256" autocomplete="off" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1">
        <p v-if="errors.location" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
      </div>
      <div>
        <label class="text-color-form" for="hint">Notiz</label>
        <textarea rows="1" placeholder="Notiz hinzufügen" maxlength="3000" class="h-32 w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1"></textarea>
        <p v-if="errors.description" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
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
      title: '',
      description: '',
      location: '',
      locale: '',
      endDate: {
        day: null,
        month: null,
        year: null
      },
      startDate: {
        day: null,
        month: null,
        year: null
      },
      errors: {
        title: false,
        description: false,
        location: false
      }
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/events/uuid`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.title = res.data.title || ''
        this.description = res.data.description || ''
        this.location = res.data.location || ''
        this.locale = this.currentLocale || res.data.locale
        this.startDate.day = new Date(Date.parse(res.data.start_date)).getDate() || null
        this.startDate.month = new Date(Date.parse(res.data.start_date)).getMonth() + 1 || null
        this.startDate.year = new Date(Date.parse(res.data.start_date)).getFullYear() || null
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
    }
  },
  watch: {
    title: function() {
      if (this.title.trim() !== '') {
        if (this.title.trim().length >= 7) {
          this.errors.title = false
        } else {
          this.errors.title = true
        }
      }
    },
    description: function() {
      if (this.description.trim() !== '') {
        if (this.description.trim().length >= 7) {
          this.errors.description = false
        } else {
          this.errors.description = true
        }
      }
    },
    location: function() {
      if (this.location.trim() !== '') {
        if (this.location.trim().length >= 7) {
          this.errors.location = false
        } else {
          this.errors.location = true
        }
      }
    }
  },
  methods: {
    handleStartDate(value) {
      console.log(value)
    },
    handleEndDate(value) {
      console.log(value)
    },
    submitForm() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.title) {
        this.errors.title = true
      }

      if (!this.description) {
        this.errors.description = true
      }

      if (!this.location) {
        this.errors.location = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/event`,
          data: {
            title: this.title.trim(),
            description: this.description.trim(),
            start_date: this.startDate,
            end_date: this.endDate,
            locale: this.locale
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
