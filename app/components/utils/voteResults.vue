<template>
<ul>
  <li v-for="value, index in polls" :class="{'mb-6': polls.length - index - 1 != 0}" :key="index" class="px-3 lg:px-6 pb-3 lg:pb-6 pt-2 lg:pt-4 bg-color-form rounded-md shadow-md mb-5 sm:mb-8">
    <h3 class="text-color-form">{{ value._id }}</h3>

    <question-charts :values="value.results" :target="makeId('svg-select', index)" />
  </li>
</ul>
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
