<template>
<div>
  <div v-for="value, index in polls" :class="{'mb-6': polls.length - index - 1 != 0}" :key="index" class="mt-3 px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md mb-8">
    <h3 class="text-color-form">{{ value._id }}</h3>

    <question-charts :values="value.results" :target="makeId('svg-select', index)" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      polls: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/stats/votes`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.polls = res.data
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    makeId(value, index) {
      return `${value}-${index}`
    }
  }
}
</script>
