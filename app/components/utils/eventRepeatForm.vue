<template>
<div class="grid grid-cols-6 gap-x-4 mt-4">
  <div class="col-span-1">
    <label class="text-color-form" for="repeat-event">Wiederholungen</label>

    <div class="relative">
      <select v-model="repeatIntervalNumber" class="appearance-none block w-full rounded border border-color-form focus:outline-none p-2 mt-2">
        <option value="0">Keine</option>
        <option v-for="value, index in repeatIntervals" :key="index" :value="value">{{ value }}</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  </div>
  <div class="col-span-1">
    <label class="text-color-form" for="repeat-event">Einheiten</label>

    <div class="relative">
      <select v-model="repeatUnitNumber" class="appearance-none block w-full rounded border border-color-form focus:outline-none p-2 mt-2">
        <option v-for="value, index in repeatUnits" :key="index" :value="value">{{ $t(value) }}</option>
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
  computed: {
    repeatUnitNumber: {
      get() {
        return this.$props.repeatUnit
      },
      set(value) {
        this.$emit('repeatUnitNumber', value)
      }
    },
    repeatIntervalNumber: {
      get() {
        return this.$props.repeatInterval
      },
      set(value) {
        this.$emit('repeatIntervalNumber', value)
      }
    },
    repeatUnits() {
      return ['days', 'weeks', 'months', 'years']
    },
    repeatIntervals() {
      return Array(Math.abs(1 - 14) + 1).fill(1).map((v, i) => v + i * (1 > 14 ? -1 : 1))
    }
  },
  props: ['repeatUnit', 'repeatInterval']
}
</script>
