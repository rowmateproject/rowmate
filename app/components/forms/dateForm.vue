<template>
<div class="grid grid-cols-12 lg:grid-cols-11 gap-3 w-full">
  <div class="col-span-12 lg:col-span-7 grid grid-cols-12 lg:grid-cols-5 gap-y-2 gap-x-3">
    <label class="col-span-12 lg:col-span-5 text-color-form leading-none" for="date">{{ titleDateString }}</label>

    <div class="col-span-3 lg:col-span-1 relative z-0">
      <select v-model="daySelected" :class="[errors.day ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2">
        <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>

    <div class="col-span-5 lg:col-span-2 relative z-0">
      <select v-model="monthSelected" :class="[errors.month ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2">
        <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>

    <div class="col-span-4 lg:col-span-2 relative z-0">
      <select v-model="yearSelected" :class="[errors.year ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2">
        <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  </div>

  <div class="col-span-12 lg:col-span-4 grid grid-cols-12 lg:grid-cols-2 gap-y-2 gap-x-3">
    <label class="col-span-12 lg:col-span-2 text-color-form leading-none" for="date">Uhrzeit</label>

    <div class="col-span-6 lg:col-span-1 relative z-0">
      <select v-model="hourSelected" :class="[errors.year ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2">
        <option v-for="value, index in hours" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
    <div class="col-span-6 lg:col-span-1 relative z-0">
      <select v-model="minuteSelected" :class="[errors.year ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="appearance-none block w-full rounded border focus:outline-none p-2">
        <option v-for="value, index in minutes" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      errors: {
        day: false,
        year: false,
        minute: false,
        month: false,
        hour: false
      }
    }
  },
  computed: {
    hours() {
      return Array(Math.abs(0 - 23) + 1).fill(0).map((v, i) => this.zeroPad((v + i * (0 > 23 ? -1 : 1)), 2))
    },
    minutes() {
      return Array(Math.abs(0 - 11) + 1).fill(0).map((v, i) => this.zeroPad((v + i * (0 > 11 ? -5 : 5)), 2))
    },
    days() {
      return Array(Math.abs(1 - 31) + 1).fill(1).map((v, i) => v + i * (1 > 31 ? -1 : 1))
    },
    months() {
      return ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    },
    years() {
      if (this.$props.direction === 'reverse') {
        return Array(Math.abs(parseInt(this.$props.minYear) - parseInt(this.$props.maxYear)) + 1).fill(parseInt(this.$props.minYear)).map((v, i) => v + i * (parseInt(this.$props.minYear) > parseInt(this.$props.maxYear) ? -1 : 1)).reverse()
      } else if (this.$props.direction === 'forward') {
        return Array(Math.abs(parseInt(this.$props.minYear) - parseInt(this.$props.maxYear)) + 1).fill(parseInt(this.$props.minYear)).map((v, i) => v + i * (parseInt(this.$props.minYear) > parseInt(this.$props.maxYear) ? -1 : 1))
      }
    },
    titleDateString() {
      return this.$props.title
    },
    daySelected: {
      get() {
        return this.$props.day
      },
      set(value) {
        this.$emit('day', value)
      }
    },
    monthSelected: {
      get() {
        return this.$props.month
      },
      set(value) {
        this.$emit('month', value)
      }
    },
    yearSelected: {
      get() {
        return this.$props.year
      },
      set(value) {
        this.$emit('year', value)
      }
    },
    hourSelected: {
      get() {
        return this.$props.hour
      },
      set(value) {
        this.$emit('hour', value)
      }
    },
    minuteSelected: {
      get() {
        return this.$props.minute
      },
      set(value) {
        this.$emit('minute', value)
      }
    }
  },
  props: ['title', 'minute', 'hour', 'day', 'month', 'year', 'direction', 'minYear', 'maxYear'],
  methods: {
    zeroPad(num, places) {
      return String(num).padStart(places, '0')
    }
  }
}
</script>
