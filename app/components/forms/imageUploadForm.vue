<template>
<div class="bg-color-form mt-3 lg:mt-8 p-6 rounded shadow">
  <div class="grid grid-cols-12 gap-6">
    <div class="col-span-12 sm:col-span-8 md:col-span-9">
      <img v-if="image" :src="image" class="w-full object-cover bg-color-image rounded">
    </div>

    <div class="col-span-12 sm:col-span-4 md:col-span-3">
      <div class="bg-color-image rounded px-4 py-2 mb-6">
        <h4 class="text-xl mb-1">Hinweis</h4>
        <p>Das hochzuladende Bild muss eine Größe von 1280px zu 330px haben oder im Verhältnis sein.</p>
      </div>
      <div class="sm:flex justify-end items-end">
        <form enctype="multipart/form-data" class="w-full h-full">
          <label class="h-full flex flex-col justify-center items-center bg-color-header text-color-button cursor-pointer rounded shadow px-4 py-2">
            <svg class="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
            </svg>
            <span class="mt-2 text-base leading-normal">Wähle ein Bild aus</span>
            <input type="file" accept="image/*" @input="upload($event.target.files)" class="hidden">
          </label>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      image: null
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/theme/default/image`,
      responseType: 'blob',
      validateStatus: () => true
    }).then(res => {
      if (res.status === 200) {
        const vm = this
        let reader = new window.FileReader()
        reader.readAsDataURL(res.data)
        reader.onload = function() {
          vm.image = reader.result
        }
      } else {
        console.debug(res.data)
      }
    })
  },
  methods: {
    createObjectURL(blob) {
      return URL.createObjectURL(blob)
    },
    createCanvas(src, width, height) {
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
    b64toBlob(b64Data, contentType = '', sliceSize = 512) {
      const byteCharacters = atob(b64Data)
      const byteArrays = []

      for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize)
        const byteNumbers = new Array(slice.length)

        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i)
        }

        const byteArray = new Uint8Array(byteNumbers)
        byteArrays.push(byteArray)
      }

      const blob = new Blob(byteArrays, {
        type: contentType
      })

      return blob
    },
    upload(file) {
      const formData = new FormData()
      const imageData = new Image()
      const vm = this

      imageData.src = this.createObjectURL(file[0])
      imageData.onload = function(e) {
        const canvas = vm.createCanvas(e.target, 1280, 330)
        const dataImage = canvas.toDataURL('image/png')
        const dataString = dataImage.replace('data:image/png;base64,', '')
        const blobData = vm.b64toBlob(dataString, 'image/png')
        formData.append('image', blobData)

        vm.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/theme/default/image`,
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            vm.image = vm.createObjectURL(blobData)
            vm.$store.commit('updateImageBlob', vm.image)
          } else {
            console.debug(res.data)
          }
        })
      }
    }
  }
}
</script>
