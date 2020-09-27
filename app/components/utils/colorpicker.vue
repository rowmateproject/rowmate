
<template>
<div class="bg-color-form rounded shadow-md absolute mt-10 top-0 right-0 overflow-auto z-30">
  <chrome-picker v-model="colors" @input="handleInput" />
</div>
</template>

<script>
import {
  Chrome
} from 'vue-color'

export default {
  components: {
    'chrome-picker': Chrome
  },
  props: ['color'],
  data() {
    return {
      colors: {
        hex: '#465d32'
      },
      colorValue: ''
    }
  },
  mounted() {
    this.setColor(this.$props.color || this.colors.hex)
  },
  watch: {
    colorValue: function(value) {
      if (value) {
        this.updateColors(value)
        this.$emit('input', value)
      } else {
        this.$emit('input', this.$props.color)
      }
    }
  },
  methods: {
    setColor(color) {
      this.updateColors(color)
      this.colorValue = color
    },
    handleInput(color) {
      this.colors = color
      if (color.rgba.a === 1) {
        this.colorValue = color.hex
      } else {
        this.colorValue = `rgba(${color.rgba.r}, ${color.rgba.g}, ${color.rgba.b}, ${color.rgba.a})`
      }
      this.$emit('color', color.hex.toLowerCase())
    },
    updateColors(color) {
      if (color.slice(0, 1) === '#') {
        this.colors = {
          hex: color
        }
      } else if (color.slice(0, 4) === 'rgba') {
        const rgba = color.replace(/^rgba?\(|\s+|\)$/g, '').split(',')
        const hex = '#' + ((1 << 24) + (parseInt(rgba[0]) << 16) + (parseInt(rgba[1]) << 8) + parseInt(rgba[2])).toString(16).slice(1)
        this.colors = {
          hex: hex,
          a: rgba[3]
        }
      }
    }
  }
}
</script>
