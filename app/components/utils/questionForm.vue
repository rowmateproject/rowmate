<template>
<div>
  <div>
    <label class="text-color-form" for="confirmPassword">Fragentyp</label>

    <div class="col-span-3 relative z-0">
      <select v-model="questionType" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
        <option value="text">Textfrage</option>
        <option value="select">Auswahlfrage</option>
        <option value="checkbox">Checkboxfrage</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-2 text-color-nav">
        <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  </div>

  <div class="mt-3">
    <label class="text-color-form">Frage</label>
    <input v-model="question" type="text" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1">
  </div>

  <div v-if="questionType == 'select'" class="mt-3">
    <label class="text-color-form">Auswahlfrage</label>
    <div v-for="option, index in options" :key="option.id" class="flex items-center">
      <input v-model="option.value" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1 mr-3">

      <button type="button" @click="removeInput(index)" :disabled="options.length === 1" :class="[options.length === 1 ? 'bg-gray-500' : 'bg-color-header hover:bg-gray-700']"
        class="focus:outline-none rounded text-white text-sm font-medium h-10 w-10 mt-1 mr-2">-</button>
      <button type="button" @click="addInputField(index)" class="bg-color-header focus:outline-none rounded text-white text-sm font-medium h-10 w-10 mt-1">+</button>
    </div>
  </div>

  <div v-if="questionType == 'checkbox'" class="mt-3">
    <label class="text-color-form">Checkboxfrage</label>
    <div v-for="option, index in options" :key="option.id" class="flex items-center">
      <input v-model="option.value" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1 mr-3">

      <button type="button" @click="removeInput(index)" :disabled="options.length === 1" :class="[options.length === 1 ? 'bg-gray-500' : 'bg-color-header hover:bg-gray-700']"
        class="focus:outline-none rounded text-white text-sm font-medium h-10 w-10 mt-1 mr-2">-</button>
      <button type="button" @click="addInputField(index)" class="bg-color-header focus:outline-none rounded text-white text-sm font-medium h-10 w-10 mt-1">+</button>
    </div>
  </div>
</div>
</template>

<script>
import {
  parse as uuidParse
} from 'uuid'

export default {
  data() {
    return {
      uuid: null,
      question: null,
      questionType: 'checkbox',
      options: [{
        id: 'option0',
        value: null
      }]
    }
  },
  created() {
    this.commitForm
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    },
    commitForm() {
      const formObject = this.$props.formObject

      this.uuid = formObject._id
      this.questionType = formObject.type
      this.question = formObject.question
      this.options = formObject.forms
    }
  },
  watch: {
    question: function() {
      this.submitForm()
    },
    'options.value': function() {
      this.submitForm()
    },
    questionType: function() {
      this.submitForm()
    }
  },
  props: ['formObject'],
  methods: {
    removeInput(index) {
      this.options.splice(index, 1);
    },
    addInputField(index) {
      const optionLength = this.options.length + 1

      this.options.splice(index + 1, 0, {
        id: `option${optionLength}`,
        value: null
      })
    },
    submitForm() {
      this.$emit('resultObject', {
        type: this.questionType,
        question: this.question,
        forms: this.options
      })
    }
  }
}
</script>
