<template>
<div class="grid grid-cols-12 gap-3 lg:gap-6">
  <div class="col-span-12 sm:col-span-6">
    <label class="text-color-form">Position</label>
    <input v-model="position.title" type="text" :class="[errors.position ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1"
      placeholder="Vorsitzender, Schriftfüher oder Kassenwart">
    <p v-if="errors.position" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
  <div class="col-span-12 sm:col-span-6">
    <label class="text-color-form">Name</label>
    <user-filter @resultObject="handleMember" @resetFilter="handleMemberReset" :searchQuery="position.member" :showResetButton="false" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      position: {
        _id: '',
        member: '',
        title: ''
      },
      errors: {
        title: false,
        member: false
      }
    }
  },
  mounted() {
    this.position = this.$props.positionObject
  },
  watch: {
    'position.title': function() {
      this.$emit('resultObject', this.position)
    },
    'position.member': function() {
      this.$emit('resultObject', this.position)
    }
  },
  props: ['positionObject'],
  methods: {
    handleMember(value) {
      this.position.member = value.user.name
    },
    handleMemberReset(value) {
      if (value === true) {
        this.position = {}
      }
    }
  }
}
</script>
