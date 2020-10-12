<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium text-color-title">Kalender</h3>

  <div class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-3 lg:px-6 lg:pb-6 lg:pt-4 bg-svg-image bg-blue-500 rounded-md shadow">
    <h4 class="text-color-nav">Event Filter</h4>
    <event-filter @resultObject="handleResult" @resetFilter="handleReset" :eventSubscriptions="false" />
  </div>

  <event-cards :eventFilter="events" :resetFilter="reset" :eventSubscriptions="false" />
</div>
</template>

<script>
export default {
  data() {
    return {
      events: [],
      reset: true
    }
  },
  methods: {
    handleReset(value) {
      this.reset = value
    },
    handleResult(value) {
      this.events = [value]
    }
  }
}
</script>
