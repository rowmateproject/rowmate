<template>
<div>
  <h3 class="text-gray-700 text-3xl font-semibold">Theme</h3>

  <form @submit.prevent="patchTheme">
    <ul class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 mt-8">
      <li v-for="color, index in theme" :key="index" class="bg-white px-2 pt-1 pb-2">
        <color @affe="paintColor" :id="index" :name="color.title" :hex="color.color" />
      </li>
    </ul>

    <div class="flex justify-end mt-4">
      <button class="px-4 py-2 bg-gray-800 text-gray-200 rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
        {{ $t('save') }}
      </button>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {
      theme: {
        headerBackground: {
          title: 'Header background color',
          color: '#841497'
        },
        footerBackground: {
          title: 'Footer background color',
          color: '#150f55'
        },
        buttonBackground: {
          title: 'Button background color',
          color: '#4299e1'
        },
        imageBackground: {
          title: 'Image background color',
          color: '#efefef'
        },
        pageBackground: {
          title: 'Page background color',
          color: '#cbcbcb'
        },
        formBackground: {
          title: 'Form background color',
          color: '#efefef'
        },
        navBackground: {
          title: 'Nav background color',
          color: '#150f55'
        },
        footerText: {
          title: 'Footer text color',
          color: '#efefef'
        },
        formBorder: {
          title: 'Form border color',
          color: '#e2e8f0'
        },
        buttonText: {
          title: 'Button text color',
          color: '#e2e8f0'
        },
        titleText: {
          title: 'Title text color',
          color: '#333333'
        },
        linkText: {
          title: 'Link text color',
          color: '#4299e1'
        },
        bodyText: {
          title: 'Body text color',
          color: '#000f57'
        },
        saleText: {
          title: 'Sale text color',
          color: '#be2222'
        },
        formText: {
          title: 'Form text color',
          color: '#000f57'
        },
        imageText: {
          title: 'Image text color',
          color: '#161a1a'
        },
        pageText: {
          title: 'Page text color',
          color: '#161a1a'
        },
        navText: {
          title: 'Nav text color',
          color: '#e5e2e4'
        }
      }
    }
  },
  computed: {
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  methods: {
    paintColor(value) {
      this.theme[value.objectName].color = value.color
    },
    patchTheme() {
      this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

      this.$axios({
        method: 'PATCH',
        url: `${process.env.API_URL}/theme/settings`,
        data: {
          headerBackground: this.theme.headerBackground.color,
          footerBackground: this.theme.footerBackground.color,
          buttonBackground: this.theme.buttonBackground.color,
          imageBackground: this.theme.imageBackground.color,
          pageBackground: this.theme.pageBackground.color,
          formBackground: this.theme.formBackground.color,
          navBackground: this.theme.navBackground.color,
          footerText: this.theme.footerText.color,
          formBorder: this.theme.formBorder.color,
          buttonText: this.theme.buttonText.color,
          titleText: this.theme.titleText.color,
          linkText: this.theme.linkText.color,
          bodyText: this.theme.bodyText.color,
          saleText: this.theme.saleText.color,
          formText: this.theme.formText.color,
          imageText: this.theme.imageText.color,
          pageText: this.theme.pageText.color,
          navText: this.theme.navText.color
        },
        validateStatus: () => true
      }).then(res => {
        console.log(res)
      })
    }
  }
}
</script>
