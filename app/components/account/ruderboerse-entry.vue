<template>
  <div v-if="rowingad.creator !== undefined">
    <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Inserat von {{ rowingad.creator.name }}</h3>


  </div>
</template>

<script>

import Notification from '@/components/utils/notification'
import Vue from 'vue'
import Avataaars from 'vuejs-avataaars'
var NotificationClass = Vue.extend(Notification)

export default {
  components: {
    Avataaars
  },
  name: 'Ruderboerse-Entry',
  data() {
    return {
      name: "",
      rowingad: {},
      users: {}
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/rowingadverts/${this.$route.params.id}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.rowingad = res.data

      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    uuid() {
      return this.$route.params.id
    }
  },
  methods: {

  }
}
</script>
