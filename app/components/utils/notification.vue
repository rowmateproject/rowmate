<template>
  <div>
    <script>
      setTimeout(function() {
        $('#id{{this.uuid}}').fadeOut('slow');
      }, 3000);
    </script>
    <div class="text-white px-6 py-4 border-0 w-1/2 rounded mb-4 fixed z-50" :class="color" style="right: 10px; top: 10px" :id="'id'+uuid" v-show="show">
      <span class="text-xl inline-block mr-5 align-middle">
        <fa :icon="['fas', icon]" />
      </span>
      <span class="inline-block align-middle mr-8">
        {{ content }}
      </span>
      <button class="absolute bg-transparent text-2xl font-semibold leading-none inline right-0 top-0 mt-4 mr-6 outline-none focus:outline-none" v-on:click="hide()">
        <fa :icon="['fas', 'times']" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      uuid: 0,
      show: true
    }
  },
  props: {
    content: {
      type: String
    },
    color: {
      type: String,
      default: 'bg-green-500'
    },
    icon: {
      type: String,
      default: 'bell'
    }
  },
  created() {
    this.uuid = this._uid
  },
  methods: {
    hide() {
      this.show = false
    }
  }
}
</script>
