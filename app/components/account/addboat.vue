<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium leading-none text-color-title">{{ $t('addboat') }}</h3>
  <div class="flex flex-col mt-8">
    <div class="col-span-12 lg:col-span-4 grid grid-cols-12 gap-3 justify-end">

      <div class="col-span-6 grid grid-cols-5 gap-2">
        <label class="col-span-6 text-color-form leading-none">Name</label>
        <input v-model="name" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2">
      </div>
      <div class="col-span-6 grid grid-cols-5 gap-2">
        <label class="col-span-6 text-color-form leading-none">Hersteller (optional)</label>
        <input v-model="manufacturer" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2">
      </div>


      <div class="col-span-2 grid grid-cols-6 gap-2">
        <label class="col-span-6 text-color-form leading-none">Kategorie</label>
        <select v-model="category" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2">
          <option v-for="(key, value) in categories" :value="key" :key="key">{{ value }}</option>
        </select>
      </div>
      <div class="col-span-3 grid grid-cols-3 gap-2">
        <label class="col-span-6 text-color-form leading-none">Disziplin</label>
        <select v-model="discipline" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2">
          <option v-for="(key, value) in disciplines" :value="key" :key="key">{{ value }}</option>
        </select>
      </div>
      <div class="col-span-3 grid grid-cols-3 gap-2">
        <label class="col-span-6 text-color-form leading-none">Steuerung</label>
        <select v-model="steered" type="text" class="col-span-6 rounded border border-color-form focus:outline-none p-2">
          <option v-for="(key, value) in coxswain" :value="key" :key="key">{{ value }}</option>
        </select>
      </div>
      <div class="col-span-2 grid grid-cols-2 gap-2">
        <label class="col-span-2 text-color-form leading-none">Plätze (inklusive Stm/Stf)</label>
        <input v-model="athletes" type="number" min="1" max="9" class="col-span-2 rounded border border-color-form focus:outline-none p-2">
      </div>
      <div class="col-span-2 grid grid-cols-1 gap-2 mr-8">
        <label class="col-span-1 text-color-form leading-none">Baujahr (optional)</label>
        <input v-model="built" type="text" class="col-span-1 rounded border border-color-form focus:outline-none p-2">
      </div>

    </div>
  </div>
  <div class="flex w-full justify-center mt-8">
    <button @click="addBoat()" class="px-4 py-2 w-1/3 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">Boot hinzufügen</button>
  </div>
</div>
</template>

<script>
import {
  BoatCategory,
  Disciplines,
  Categories,
  Coxswain
} from '@/plugins/boatcategory'

export default {
  name: 'Add Boat',
  data() {
    return {
      name: "",
      manufacturer: "",
      built: 0,
      category: 0,
      discipline: 0,
      steered: 0,
      athletes: 1
    }
  },
  computed: {
    disciplines: function () {
      return Disciplines
    },
    coxswain: function () {
      return Coxswain
    },
    categories: function () {
      return Categories
    },
  },
  methods: {
    addBoat() {
      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/boat`,
        data: {
          name: this.name,
          crewsize: this.athletes,
          category: this.category,
          coxswain: this.steered,
          discipline: this.discipline,
          manufacturer: this.manufacturer,
          built: this.built
        },
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
    }
  }
}
</script>
