
  console.log(value)
<template>
<div class="grid grid-cols-12 gap-6">
  <div class="col-span-6">
    <label class="text-color-form">Position</label>
    <input v-model="position.title" type="text" :class="[errors.position ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1"
      placeholder="Vorsitzender, Schriftfüher oder Kassenwart">
    <p v-if="errors.position" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
  <div class="col-span-6">
    <label class="text-color-form">Mitglieder Filter</label>
    <user-filter @resultObject="handleMember" @resetFilter="handleMemberReset" :showResetButton="true" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      position: {
        title: '',
        member: ''
      },
      errors: {
        title: false,
        member: false
      }
    }
  },
  computed: {
    watchMe() {
      const positionObject = this.$props.positionObject

      this.position.title = positionObject.title
      this.position.member = positionObject.member
    }
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
