<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">Kalender</h3>

  <event-filter @resultObject="handleResult" @resetFilter="handleReset" :eventSubscriptions="false" />
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
