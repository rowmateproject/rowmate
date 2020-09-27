<template>
<div class="container text-center mt-8 mx-auto text-gray-250">
  <h3 class="p-3 text-3xl border-b-4 border-t-2 border-green-700 border-opacity-75" v-if="status === 200">Mail confirmed successfully</h3>
  <h3 class="p-3 text-3xl border-b-4 border-t-2 border-red-800 border-opacity-75" v-if="status === 400">Token expired or not valid</h3>
</div>
</template>

<script>
export default {
  middleware: 'notAuthenticated',
  data() {
    return {
      status: 0
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/confirm/`+this.$route.params.id,
      alidateStatus: () => true
    }).then(res => {
      this.status = res.status
    }).catch(err => {
      this.status = err.response.status
    })
  }
}
</script>
