<template>
<div>
  <div ref="notifications"></div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">Inserat zur Ruderbörse hinzufügen</h3>
  <div class="flex flex-col mt-8">
    <div class="col-span-12 lg:col-span-4 grid grid-cols-12 gap-3 justify-end">


      <div class="col-span-2 grid grid-cols-5 gap-2">
        <label class="col-span-5 text-color-form leading-none">Datum angeben</label>
        <input v-model="setdatetime" type="checkbox" class="col-span-5 h-8 -mt-1">
      </div>

      <div class="col-span-4 grid grid-cols-5 gap-2">
        <label class="col-span-6 text-color-form leading-none">Datum und Uhrzeit</label>
        <client-only v-if="setdatetime">
          <VueTailwindDatetimePicker @change="(v) => handleDate(v)" :lang="$i18n.locale" :startFromMonday="true">
            <input type="text" class="rounded border border-color-form focus:outline-none p-2" v-model="dateString" />
          </VueTailwindDatetimePicker>
        </client-only>
        <span v-else class="text-green-700 col-span-6 rounded border border-color-form focus:outline-none p-2">Datumseingabe deaktiviert.</span>
      </div>
      <div class="col-span-2 grid grid-cols-5 gap-2">
        <label class="col-span-5 text-color-form leading-none">Ein Boot auswählen</label>
        <input v-model="fillboat" type="checkbox" class="col-span-5 h-8 -mt-1">
      </div>
      <div class="col-span-4 grid grid-cols-5 gap-2">
        <label class="col-span-5 text-color-form leading-none">Ein Boot auswählen</label>
        <select v-model="boat" type="checkbox" class="col-span-5 h-8 -mt-1" v-if="fillboat && boats.length!==0">
          <option value="" disabled selected>Bitte Boot wählen</option>
          <option v-for="iboat in boats" :value="iboat.uuid">{{ boatCategories[iboat.uuid] }} {{ iboat.name }}</option>
        </select>
        <span v-if="boats.length!==0 && !fillboat" class="text-green-700 col-span-6 rounded border border-color-form focus:outline-none p-2">Bootsauswahl deaktiviert.</span>
        <span v-if="boats.length===0" class="text-red-700 col-span-6 rounded border border-color-form focus:outline-none p-2">Keine Boote auf der Plattform</span>
      </div>
      <div class="col-span-12 grid grid-cols-5 gap-2 mt-8">
        <span v-if="errors.name" class="text-red-700 col-span-6"> {{ errors.name }}</span>
        <label class="col-span-6 text-color-form leading-none" v-else>Text</label>
        <textarea v-model="text" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2"></textarea>
      </div>


    </div>
  </div>
  <div class="flex w-full justify-center mt-8">
    <button @click="addAd()" class="px-4 py-2 w-1/3 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">Inserat hinzufügen</button>
  </div>
</div>
</template>

<script>
import VueTailwindDatetimePicker from 'vue-tailwind-datetime-picker'
import Notification from '@/components/utils/notification'
import {
  BoatCategory
} from '@/plugins/boatcategory'
import Vue from 'vue'
var NotificationClass = Vue.extend(Notification)

export default {
  name: 'AddAdvert',
  data() {
    return {
      fillboat: false,
      text: "",
      errors: {},
      dateString: "",
      boats: [],
      boat: "",
      boatCategories: {},
      setdatetime: true,
      date: {
        day: null,
        hour: null,
        minute: null,
        month: null,
        year: null
      },
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
        this.boatCategories = BoatCategory.getCategories(res.data)
      } else {
        console.debug(res.data)
      }
    })
  },
  computed: {

  },
  methods: {

    handleDate(v) {
      this.dateString = v
      let date = new Date(v)
      this.date.year = date.getFullYear()
      this.date.month = date.getMonth()
      this.date.day = date.getDay()
      this.date.hour = date.getHours()
      this.date.minute = date.getMinutes()
    },
    addAd() {
      console.log('Submit Ad-Data')
      this.errors = {}
      if (this.text.length < 1) {
        this.errors.name = 'Please add a text'
      }
      if (Object.keys(this.errors).length === 0) {
        const data = {
          text: this.text,
        }
        if (this.boat.length > 0) {
          data.boat = this.boat
        }
        if (this.setdatetime === true) {
          data.time = this.dateString
        }
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/rowingadverts`,
          data: data,
          validateStatus: () => true
        }).then((res) => {
          if (res.status === 200) {
            this.$router.push('/ruderboerse?msg=adadded');
          } else {
            var instance = new NotificationClass({
              propsData: {
                content: 'Couldn\'t add advert',
                color: 'bg-red-500'
              }
            })
            instance.$mount()
            this.$refs.notifications.appendChild(instance.$el)
          }
        })
      }
    }
  },

  components: {
    VueTailwindDatetimePicker
  }
}
</script>
