<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Kalender</h3>

  <div class="bg-svg-image bg-blue-500 rounded shadow p-3 lg:p-6 my-3 lg:my-6 mb-3">
    <h4 class="text-color-nav leading-none">Event Filter</h4>
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
