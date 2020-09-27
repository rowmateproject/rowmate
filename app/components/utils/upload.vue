<template>
<div class="bg-white rounded mt-3 md:mt-6">
  <p class="text-color-body p-2" :for="upload">Logo Upload</p>

  <img ref="upload" class="px-2">

  <form enctype="multipart/form-data" class="w-48 p-2">
    <label class="flex flex-col items-center bg-color-header text-color-button cursor-pointer rounded shadow px-4 py-2">
      <svg class="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
        <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
      </svg>
      <span class="mt-2 text-base leading-normal">Select a file</span>
      <input type="file" accept="image/*" @input="upload($event.target.files)" class="hidden">
    </label>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {}
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/theme/image`,
      responseType: 'blob',
      validateStatus: () => true
    }).then(res => {
      if (res.status === 200) {
        const vm = this
        let reader = new window.FileReader()
        reader.readAsDataURL(res.data)
        reader.onload = function() {
          vm.$refs.upload.src = reader.result
        }
      } else {
        console.debug(res.data)
      }
    })
  },
  methods: {
    createObjectURL(image) {
      const URL = window.URL || window.webkitURL || window.mozURL || window.msURL
      return URL.createObjectURL(image)
    },
    resizeImageAndCrop(src, width, height) {
      const crop = width === 0 || height === 0

      if (src.width <= width && height === 0) {
        width = src.width
        height = src.height
      }

      if (src.width > width && height === 0) {
        height = src.height * (width / src.width)
      }

      const xscale = width / src.width
      const yscale = height / src.height
      const scale = crop ? Math.min(xscale, yscale) : Math.max(xscale, yscale)

      const canvas = document.createElement('canvas')
      canvas.width = width ? width : Math.round(src.width * scale)
      canvas.height = height ? height : Math.round(src.height * scale)
      canvas.getContext('2d').scale(scale, scale)
      canvas.getContext('2d').drawImage(src, ((src.width * scale) - canvas.width) * -.5, ((src.height * scale) - canvas.height) * -.5)

      return canvas
    },
    upload(file) {
      const formData = new FormData()
      const imageData = new Image()
      const vm = this

      imageData.src = this.createObjectURL(file[0])
      imageData.onload = function(e) {
        const source = vm.resizeImageAndCrop(e.target, 800, 200)
        vm.$refs.upload.src = source.toDataURL('image/png')
      }

      formData.set('upload', file[0])

      this.$axios({
        method: 'PATCH',
        url: `${process.env.API_URL}/theme/image`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        validateStatus: () => true
      }).then(res => {
        if (res.status === 200) {
          console.debug(res.data)
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
