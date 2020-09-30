<template>
<div>
  <div class="mb-4">
    <label class="flex justify-start items-center text-color-form" :for="makeId('title', locale)">
      <img :src="makePath(locale)" :alt="locale" class="h-4 mr-1">
      <span>Titel</span>
    </label>
    <input v-model="titleString" type="text" placeholder="Titel eingeben" :class="[titleErrorString ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1">
    <p v-if="titleErrorString" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
  <div>
    <label class="text-color-form" :for="makeId('description', locale)">Notiz</label>
    <textarea v-model="descriptionString" placeholder="Notiz hinzufügen" :class="[descriptionErrorString ? 'border-red-500 focus:border-red-500' : 'border-color-form']" class="h-48 w-full rounded border focus:outline-none p-2 mt-2 mb-1"></textarea>
    <p v-if="descriptionErrorString" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
  </div>
</div>
</template>

<script>
export default {
  computed: {
    locale() {
      return this.$props.code
    },
    titleErrorString() {
      // console.log(typeof this.$props.titleError)
      return this.$props.titleError
    },
    descriptionErrorString() {
      // console.log(typeof this.$props.descriptionError)
      return this.$props.descriptionError
    },
    titleString: {
      get() {
        return this.$props.title
      },
      set(value) {
        this.$emit('titleString', {
          locale: this.locale,
          title: value
        })
      }
    },
    descriptionString: {
      get() {
        return this.$props.description
      },
      set(value) {
        this.$emit('descriptionString', {
          locale: this.locale,
          description: value
        })
      }
    }
  },
  props: ['code', 'title', 'description', 'titleError', 'descriptionError'],
  methods: {
    makePath(locale) {
      return `/flags/${locale}.svg`
    },
    makeId(value, locale) {
      return `${value}-${locale}`
    }
  }
}
</script>
