<template>
<div>

  <Notification content="Successfully added boat" v-if="this.$route.query.msg === 'boatadded'"/>
  <div ref="notifications"></div>
  <div v-if="isSuperuser === 'true' || isSuperuser === true" class="container flex justify-between pl-4">
    <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">{{ $t('boats') }}</h3>
    <nuxt-link :to="localePath('/boat/add')"><button class="bg-color-button text-color-button h-10 px-16 transition-colors duration-150 rounded-lg focus:shadow-outline">Boot hinzufügen</button></nuxt-link>
  </div>


  <div class="bg-svg-image bg-blue-500 rounded shadow p-3 lg:p-6 my-3 lg:my-6 mb-3">
    <h4 class="text-color-nav leading-none">Boote Filter</h4>
    <boat-filter @resultObject="handleBoatFilter" @resetFilter="handleBoatReset" :showResetButton="true" />
  </div>

  <div>

  </div>

  <div v-if="boats.length > 0" class="flex flex-col mt-8">
    <div class="overflow-x-auto">
      <div class="min-w-full align-middle inline-block shadow overflow-hidden rounded">
        <table class="min-w-full">
          <thead class="bg-color-image text-gray-900">
            <tr>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('name') }}
              </th>
              <th class="py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('category') }}
              </th>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('steered') }}
              </th>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('crewsize') }}
              </th>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('discipline') }}
              </th>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('delete') }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-color-form">
            <tr v-for="(b, index) in boats" :key="index" class="border-b-2 border-gray-200">
              <td class="px-6 py-4 whitespace-no-wrap">
                <div class="flex items-center">
                  <div class="ml-4">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      {{ b.name }}
                    </div>
                    <div class="text-sm leading-5 text-color-body">
                      {{ boatCategories[b.id] }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                <span v-if="b.category == 0">Gig</span>
                <span v-else>Rennboot</span>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                <span v-if="b.coxswain == 0">Ja</span>
                <span v-if="b.coxswain == 1">Nein</span>
                <span v-if="b.coxswain == 2">Wechselbar</span>
                <span v-if="b.coxswain == 3">Ja (wechselbar)</span>
                <span v-if="b.coxswain == 4">Nein (wechselbar)</span>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                {{ b.crewsize }}
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                <span v-if="b.discipline == 0">Sculling</span>
                <span v-if="b.discipline == 1">Riemen</span>
                <span v-if="b.discipline == 2">Sculling (wechselbar)</span>
                <span v-if="b.discipline == 3">Riemen (wechselbar)</span>
                <span v-if="b.discipline == 4">Unbekannt</span>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                <button @click="deleteBoat(index)" class="col-span-6 bg-red-600 text-white rounded focus:outline-none px-4 py-2 md:mb-2 lg:mb-0"><fa :icon="['fas', 'trash']" class="col-span-1 mt-1" /></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="container" v-else>
    <div class="container flex justify-center my-12 text-xl">
      <h2>{{ $t('noboats') }}</h2>
    </div>
  </div>
</div>
</template>

<script>
import {
  BoatCategory
} from '@/plugins/boatcategory'
import Notification from '@/components/utils/notification'
import Vue from 'vue'
var NotificationClass = Vue.extend(Notification)

export default {
  name: 'Boats',
  data() {
    return {
      boats: [],
      boatCategories: {},
      boatsBackup: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/boats`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.boats = res.data
        this.boatsBackup = res.data
        this.boatCategories = BoatCategory.getCategories(res.data)
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {
    isSuperuser() {
      return this.$store.state.isSuperuser
    }
  },
  methods: {
    handleBoatFilter(value) {
      this.boats = [value.boat]
    },
    handleBoatReset(value) {
      if (value === true) {
        this.boats = this.boatsBackup
      }
    },
    deleteBoat(index) {
      var uuid = this.boats[index].uuid
      this.$axios({
        method: 'DELETE',
        url: `${process.env.API_URL}/boat/${uuid}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          this.boats.splice(index, 1)
          var instance = new NotificationClass({
            propsData: {
              content: 'Boat successfully deleted',
              color: 'bg-red-500'
            }
          })
          instance.$mount()
          this.$refs.notifications.appendChild(instance.$el)
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
