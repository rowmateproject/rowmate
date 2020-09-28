<template>
<div>
  <p class="text-color-body mb-2">{{ $t($props.name) }}</p>

  <div class="relative grid grid-cols-6">
    <input type="text" v-model="hexCustom" class="col-span-5 font-sans bg-gray-300 focus:outline-none px-2 py-1">
    <button :style="{ backgroundColor: hexCustom }" @click.stop="toggleColorpicker" type="button" class="col-span-1 focus:outline-none curor-pointer"></button>
    <colorpicker v-if="togglePicker" @color="fromChild" :toChild="hexCustom" v-click-outside="toggleColorpicker" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      togglePicker: false
    }
  },
  props: ['id', 'name', 'hex'],
  computed: {
    hexCustom: {
      get() {
        return this.$props.hex
      },
      set(value) {
        return this.fromChild(value)
      }
    }
  },
  methods: {
    fromChild(value) {
      this.color = value

      const childObject = {
        color: value,
        name: this.$props.name
      }

      this.$emit('data', childObject)
    },
    toggleColorpicker() {
      this.togglePicker = !this.togglePicker
    }
  }
}
</script>
