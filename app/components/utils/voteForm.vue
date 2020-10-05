<template>
<form v-if="polls" @submit.prevent class="mt-3 px-6 pb-6 pt-4 bg-color-form rounded-md shadow-md">
  <ul>
    <li v-for="value, index in polls">
      <h3 class="text-color-form">{{ value.question }}</h3>

      <div v-if="value.type === 'text'">
        <input v-model="polls[index].reply" @focusout="updateResponse(value._id, polls[index].reply)" type="text" class="appearance-none block w-full bg-white text-gray-700 border border-gray-500 rounded p-3 mb-1 leading-tight focus:outline-none">
      </div>

      <div v-if="value.type == 'checkbox'" v-for="option, i in value.forms" class="flex mb-1">
        <fa :key="update" @click="toggleCheckbox(value._id, index, i)" :class="[setCheckboxClass(index, i) ? 'text-green-500' : 'text-gray-500']" :icon="['fas', 'check-square']" class="cursor-pointer inline-block text-xl lg:text-2xl w-5 mr-2" />
        <span>{{ option.value }}</span>
      </div>

      <div v-if="value.type == 'select'" class="relative z-0">
        <select v-model="polls[index].reply" @change="updateResponse(value._id, polls[index].reply)" class="appearance-none block w-full rounded border form-border-color focus:outline-none p-2 mt-2">
          <option v-for="option in value.forms" :value="option.id">{{ option.value }}</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 mt-1">
          <svg class="text-color-form fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>
    </li>
  </ul>
</form>
</template>

<script>
export default {
  data() {
    return {
      polls: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/polls/${this.currentLocale}`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.polls = res.data
      }
    })
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale
    }
  },
  props: ['title'],
  methods: {
    setCheckboxClass(formIndex, checkboxIndex) {
      const elementId = `option${checkboxIndex}`
      let elementMatch = false

      if (!Array.isArray(this.task.forms[formIndex].reply)) {
        this.task.forms[formIndex].reply = []
      }

      if (this.task.forms[formIndex].reply.includes(elementId)) {
        elementMatch = true
      }

      return elementMatch
    },
    toggleCheckbox(formId, taskId, formIndex, checkboxIndex) {
      const elementId = `option${checkboxIndex}`
      let elementMatch = false

      if (this.task.forms[formIndex].reply.includes(elementId)) {
        elementMatch = true
      }

      if (elementMatch) {
        const elementIndex = this.task.forms[formIndex].reply.findIndex(e => e === elementId)
        this.task.forms[formIndex].reply.splice(elementIndex, 1)
        this.removeResponse(formId, elementId)
      } else {
        this.task.forms[formIndex].reply.push(elementId)
        this.updateResponse(formId, this.task.forms[formIndex].reply)
      }
      this.update = !this.update
    },
    updateResponse(formId, taskId, value) {
      if (Array.isArray(value)) {
        value = value.filter(e => e)
      }

      this.$axios.$post(`${process.env.API_URL}/api/v1/challenge/task/response`, {
        fid: formId,
        tid: taskId,
        reply: value
      }).then(res => {
        console.log(res)
      }).catch(error => {
        if (error.hasOwnProperty('response')) {
          console.log(error.response.data)
        } else {
          console.log(error.message)
        }
      })
    },
    removeResponse(formId, taskId, value) {
      if (Array.isArray(value)) {
        value = value.filter(e => e)
      }

      this.$axios.$put(`${process.env.API_URL}/api/v1/challenge/task/response`, {
        fid: formId,
        tid: taskId,
        reply: value
      }).then(res => {
        console.log(res)
      }).catch(error => {
        if (error.hasOwnProperty('response')) {
          console.log(error.response.data)
        } else {
          console.log(error.message)
        }
      })
    }
  }
}
</script>
