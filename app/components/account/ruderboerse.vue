<template>
  <div>
    <Notification content="Successfully added boat" v-if="this.$route.query.msg === 'boatadded'"/>
    <div ref="notifications"></div>
    <div class="container flex justify-between pl-4">
      <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">{{ $t('Ruderboerse') }}</h3>
      <nuxt-link :to="localePath('/ruderboerse/add')"><button class="bg-color-button text-color-button h-10 px-16 transition-colors duration-150 rounded-lg focus:shadow-outline">Inserat hinzufügen</button></nuxt-link>
    </div>

    <div class="w-full lg:max-w-full lg:flex sm:flex-wrap mt-6 justify-center">
      <div v-for="ad in rowingads" class="border border-b border-gray-400 bg-white rounded p-4 m-1 flex flex-col justify-between leading-normal lg:w-2/5 hover:shadow-2xl hover:bg-gray-100">
        <nuxt-link :to="localePath('/ruderboerse/'+ad.uuid)">
          <div class="mb-8">
            <div class="text-gray-900 font-bold text-xl mb-2">{{ ad.creator.name }}</div>
            <p class="text-gray-700 text-base">{{ ad.text }}</p>
          </div>
          <div class="flex items-center">
            <div class="w-10 h-10 rounded-full mr-4">
              <avatar v-if="ad.creator.avatar !== undefined" :avatar="ad.creator.avatar" />
            </div>
            <div class="text-sm">
              <p class="text-gray-900 leading-none">{{ ad.creator.name }}</p>
              <p class="text-gray-600" v-if="ad.created_at">Erstellt: {{ ad.created_at | formatDay }}</p>
            </div>
          </div>
        </nuxt-link>
      </div>
    </div>

  </div>
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
  name: 'Ruderboerse',
  data() {
    return {
      name: "",
      rowingads: [],
      users: {}
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/rowingadverts`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.rowingads = res.data

      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {

  },
  methods: {

  }
}
</script>
