<template>
<div>
  <label class="text-color-form" for="date">{{ titleString }}</label>

  <div class="grid grid-cols-6 gap-3 w-full mb-1">
    <div class="col-span-1 relative z-0">
      <select v-model="daySelected" :class="[errors.day ? 'border-red-500 focus:border-red-500' : 'border-color-form']"
        class="appearance-none block w-full rounded border focus:outline-none p-2 mt-2">
        <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
    <div class="col-span-3 relative z-0">
      <select v-model="monthSelected" :class="[errors.month ? 'border-red-500 focus:border-red-500' : 'border-color-form']"
        class="appearance-none block w-full rounded border focus:outline-none p-2 mt-2">
        <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
    <div class="col-span-2 relative z-0">
      <select v-model="yearSelected" :class="[errors.year ? 'border-red-500 focus:border-red-500' : 'border-color-form']"
        class="appearance-none block w-full rounded border focus:outline-none p-2 mt-2">
        <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
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
        month: false,
        year: false
      }
    }
  },
  computed: {
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
    titleString() {
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
    }
  },
  props: ['title', 'day', 'month', 'year', 'direction', 'minYear', 'maxYear'],
  methods: {
    updateSelected(key, value) {
      this[key] = value
      this.$emit('dateObject', this.dateObject)
    }
  }
}
</script>
