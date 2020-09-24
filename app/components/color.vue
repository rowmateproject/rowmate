<template>
<div>
  <p class="text-gray-800 mb-2">{{ this.$props.name }}</p>
  <div class="relative grid grid-cols-6">
    <input type="text" v-model="hex" class="col-span-5 font-sans bg-gray-300 focus:outline-none px-2 py-1">
    <button :style="{ backgroundColor: hex }" @click.stop="toggleColorpicker" type="button" class="col-span-1 focus:outline-none curor-pointer"></button>
    <colorpicker @color="fromChildComponent" v-if="showColorpicker" v-click-outside="toggleColorpicker" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      showColorpicker: false
    }
  },
  props: ['id', 'name', 'hex'],
  watch: {
    id: function(value) {
      return value
    },
    hex: function(value) {
      return value
    },
    name: function(value) {
      return value
    }
  },
  methods: {
    fromChildComponent(value) {
      this.color = value

      const childObject = {
        color: value,
        objectName: this.$props.id
      }

      this.$emit('affe', childObject)
    },
    toggleColorpicker() {
      this.showColorpicker = !this.showColorpicker
    }
  }
}
</script>
