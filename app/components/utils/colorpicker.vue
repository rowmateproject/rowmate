<template>
<div class="bg-color-form rounded shadow absolute mt-10 top-0 right-0 overflow-auto z-30">
  <picker v-model="colors" @input="handleInput" />
</div>
</template>

<script>
import {
  Sketch
} from 'vue-color'

export default {
  components: {
    'picker': Sketch
  },
  props: ['toChild'],
  computed: {
    colors: {
      get() {
        return this.$props.toChild
      },
      set(value) {
        return value
      }
    }
  },
  watch: {
    colors: function(value) {
      this.$emit('input', value)
    }
  },
  methods: {
    handleInput(value) {
      this.colors = value.hex
      this.$emit('color', value.hex.toLowerCase())
    }
  }
}
</script>
