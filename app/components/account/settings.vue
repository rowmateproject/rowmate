<template>
<div>
  <h3 class="text-gray-700 text-3xl font-semibold">{{ $t('settings') }}</h3>

  <form @submit.prevent="saveExtendedUser">
    <div class="mt-8 p-6 bg-white rounded-md shadow-md">
      <div class="grid grid-cols-6 gap-6">
        <div class="col-span-6 sm:col-span-2 sm:pr-6 sm:border-r-2">
          <avatar :avatar="user.avatar" />

          <div class="text-center mt-8">
            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
              <input type="checkbox" name="toggle" id="toggle" class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer" />
              <label for="toggle" class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
            </div>
            <label for="toggle" class="text-xs text-gray-700">Use avatar</label>
          </div>
        </div>

        <ul class="col-span-6 sm:col-span-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <li v-if="!['isCircle'].includes(param)" class="flex flex-col" v-for="value, param in user.avatar">
            <label class="text-gray-700" :for="param">{{ param }}</label>

            <select v-model="user.avatar[param]" class="rounded border focus:outline-none p-2 mt-2">
              <option v-if="!['circleColor'].includes(param)" v-for="v, index in getItems(param)" :key="index" :value="v">{{ v }}</option>
              <option v-if="['circleColor'].includes(param)" v-for="v, index in getItems(param)" :key="index" :value="v[0]">{{ v[1] }}</option>
            </select>
          </li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-6 bg-white rounded-md shadow-md">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
        <div>
          <label class="text-gray-700" for="username">{{ $t('name') }}</label>
          <input :class="[errors.name ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="text" v-model="user.name">
          <p v-if="errors.name" class="text-red-500 text-xs italic">{{ $t('errorInvalidName') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="birthDate">{{ $t('birthDate') }}</label>
          <div class="grid grid-cols-6 gap-3 w-full mb-1">
            <select :class="[errors.birthDate.day ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-1 rounded border focus:outline-none p-2 mt-2" v-model="user.birthDate.day">
              <option v-for="value, index in days" :key="index" :value="value">{{ value }}</option>
            </select>
            <select :class="[errors.birthDate.month ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-3 rounded border focus:outline-none p-2 mt-2" v-model="user.birthDate.month">
              <option v-for="value, index in months" :key="index" :value="index + 1">{{ value }}</option>
            </select>
            <select :class="[errors.birthDate.year ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="col-span-2 rounded border focus:outline-none p-2 mt-2" v-model="user.birthDate.year">
              <option v-for="value, index in years" :key="index" :value="value">{{ value }}</option>
            </select>
          </div>
          <p v-if="errors.birthDate" class="text-red-500 text-xs italic">{{ $t('errorInvalidBirthDate') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="phoneNumber">{{ $t('phoneNumber') }}</label>
          <input :class="[errors.phone ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="tel" v-model="user.phone">
          <p v-if="errors.phone" class="text-red-500 text-xs italic">{{ $t('errorInvalidPhone') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="mailAddress">{{ $t('mailAddress') }}</label>
          <input :class="[errors.email ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="email" v-model="user.email">
          <p v-if="errors.email" class="text-red-500 text-xs italic">{{ $t('errorInvalidMail') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="password">{{ $t('password') }}</label>
          <input :class="[errors.password ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.password">
          <p v-if="errors.password" class="text-red-500 text-xs italic">{{ $t('errorInvalidPassword') }}</p>
        </div>

        <div>
          <label class="text-gray-700" for="confirmPassword">{{ $t('confirmPassword') }}</label>
          <input :class="[errors.confirm ? 'border-red-500 focus:border-red-500' : 'focus:border-blue-550']" class="w-full rounded border focus:outline-none p-2 mt-2 mb-1" type="password" v-model="user.confirm">
          <p v-if="errors.confirm" class="text-red-500 text-xs italic">{{ $t('errorInvalidConfirmPassword') }}</p>
        </div>
      </div>

      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-gray-800 text-gray-200 rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
          {{ $t('save') }}
        </button>
      </div>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        avatar: {},
        name: '',
        phone: '',
        email: '',
        birthDate: {
          day: null,
          month: null,
          year: null
        },
        password: '',
        confirm: '',

      },
      errors: {
        name: false,
        phone: false,
        email: false,
        birthDate: false,
        password: false,
        confirm: false
      },
      circleColor: [
        ['#CD5C5C', 'IndianRed'],
        ['#F08080', 'LightCoral'],
        ['#FA8072', 'Salmon'],
        ['#E9967A', 'DarkSalmon'],
        ['#FFA07A', 'LightSalmon'],
        ['#DC143C', 'Crimson'],
        ['#FF0000', 'Red'],
        ['#B22222', 'FireBrick'],
        ['#8B0000', 'DarkRed'],
        ['#FFC0CB', 'Pink'],
        ['#FFB6C1', 'LightPink'],
        ['#FF69B4', 'HotPink'],
        ['#FF1493', 'DeepPink'],
        ['#C71585', 'MediumVioletRed'],
        ['#DB7093', 'PaleVioletRed'],
        ['#FFA07A', 'LightSalmon'],
        ['#FF7F50', 'Coral'],
        ['#FF6347', 'Tomato'],
        ['#FF4500', 'OrangeRed'],
        ['#FF8C00', 'DarkOrange'],
        ['#FFA500', 'Orange'],
        ['#FFD700', 'Gold'],
        ['#FFFF00', 'Yellow'],
        ['#FFFFE0', 'LightYellow'],
        ['#FFFACD', 'LemonChiffon'],
        ['#FAFAD2', 'LightGoldenrodYellow'],
        ['#FFEFD5', 'PapayaWhip'],
        ['#FFE4B5', 'Moccasin'],
        ['#FFDAB9', 'PeachPuff'],
        ['#EEE8AA', 'PaleGoldenrod'],
        ['#F0E68C', 'Khaki'],
        ['#BDB76B', 'DarkKhaki'],
        ['#E6E6FA', 'Lavender'],
        ['#D8BFD8', 'Thistle'],
        ['#DDA0DD', 'Plum'],
        ['#EE82EE', 'Violet'],
        ['#DA70D6', 'Orchid'],
        ['#FF00FF', 'Fuchsia'],
        ['#FF00FF', 'Magenta'],
        ['#BA55D3', 'MediumOrchid'],
        ['#9370DB', 'MediumPurple'],
        ['#663399', 'RebeccaPurple'],
        ['#8A2BE2', 'BlueViolet'],
        ['#9400D3', 'DarkViolet'],
        ['#9932CC', 'DarkOrchid'],
        ['#8B008B', 'DarkMagenta'],
        ['#800080', 'Purple'],
        ['#4B0082', 'Indigo'],
        ['#6A5ACD', 'SlateBlue'],
        ['#483D8B', 'DarkSlateBlue'],
        ['#7B68EE', 'MediumSlateBlue'],
        ['#ADFF2F', 'GreenYellow'],
        ['#7FFF00', 'Chartreuse'],
        ['#7CFC00', 'LawnGreen'],
        ['#00FF00', 'Lime'],
        ['#32CD32', 'LimeGreen'],
        ['#98FB98', 'PaleGreen'],
        ['#90EE90', 'LightGreen'],
        ['#00FA9A', 'MediumSpringGreen'],
        ['#00FF7F', 'SpringGreen'],
        ['#3CB371', 'MediumSeaGreen'],
        ['#2E8B57', 'SeaGreen'],
        ['#228B22', 'ForestGreen'],
        ['#008000', 'Green'],
        ['#006400', 'DarkGreen'],
        ['#9ACD32', 'YellowGreen'],
        ['#6B8E23', 'OliveDrab'],
        ['#808000', 'Olive'],
        ['#556B2F', 'DarkOliveGreen'],
        ['#66CDAA', 'MediumAquamarine'],
        ['#8FBC8B', 'DarkSeaGreen'],
        ['#20B2AA', 'LightSeaGreen'],
        ['#008B8B', 'DarkCyan'],
        ['#008080', 'Teal'],
        ['#00FFFF', 'Aqua'],
        ['#00FFFF', 'Cyan'],
        ['#E0FFFF', 'LightCyan'],
        ['#AFEEEE', 'PaleTurquoise'],
        ['#7FFFD4', 'Aquamarine'],
        ['#40E0D0', 'Turquoise'],
        ['#48D1CC', 'MediumTurquoise'],
        ['#00CED1', 'DarkTurquoise'],
        ['#5F9EA0', 'CadetBlue'],
        ['#4682B4', 'SteelBlue'],
        ['#B0C4DE', 'LightSteelBlue'],
        ['#B0E0E6', 'PowderBlue'],
        ['#ADD8E6', 'LightBlue'],
        ['#87CEEB', 'SkyBlue'],
        ['#87CEFA', 'LightSkyBlue'],
        ['#00BFFF', 'DeepSkyBlue'],
        ['#1E90FF', 'DodgerBlue'],
        ['#6495ED', 'CornflowerBlue'],
        ['#7B68EE', 'MediumSlateBlue'],
        ['#4169E1', 'RoyalBlue'],
        ['#0000FF', 'Blue'],
        ['#0000CD', 'MediumBlue'],
        ['#00008B', 'DarkBlue'],
        ['#000080', 'Navy'],
        ['#FFF8DC', 'Cornsilk'],
        ['#FFEBCD', 'BlanchedAlmond'],
        ['#FFE4C4', 'Bisque'],
        ['#FFDEAD', 'NavajoWhite'],
        ['#F5DEB3', 'Wheat'],
        ['#DEB887', 'BurlyWood'],
        ['#D2B48C', 'Tan'],
        ['#BC8F8F', 'RosyBrown'],
        ['#F4A460', 'SandyBrown'],
        ['#DAA520', 'Goldenrod'],
        ['#B8860B', 'DarkGoldenrod'],
        ['#CD853F', 'Peru'],
        ['#D2691E', 'Chocolate'],
        ['#8B4513', 'SaddleBrown'],
        ['#A0522D', 'Sienna'],
        ['#A52A2A', 'Brown'],
        ['#800000', 'Maroon'],
        ['#FFFFFF', 'White'],
        ['#FFFAFA', 'Snow'],
        ['#F0FFF0', 'HoneyDew'],
        ['#F5FFFA', 'MintCream'],
        ['#F0FFFF', 'Azure'],
        ['#F0F8FF', 'AliceBlue'],
        ['#F8F8FF', 'GhostWhite'],
        ['#F5F5F5', 'WhiteSmoke'],
        ['#FFF5EE', 'SeaShell'],
        ['#F5F5DC', 'Beige'],
        ['#FDF5E6', 'OldLace'],
        ['#FFFAF0', 'FloralWhite'],
        ['#FFFFF0', 'Ivory'],
        ['#FAEBD7', 'AntiqueWhite'],
        ['#FAF0E6', 'Linen'],
        ['#FFF0F5', 'LavenderBlush'],
        ['#FFE4E1', 'MistyRose'],
        ['#DCDCDC', 'Gainsboro'],
        ['#D3D3D3', 'LightGray'],
        ['#C0C0C0', 'Silver'],
        ['#A9A9A9', 'DarkGray'],
        ['#808080', 'Gray'],
        ['#696969', 'DimGray'],
        ['#778899', 'LightSlateGray'],
        ['#708090', 'SlateGray'],
        ['#2F4F4F', 'DarkSlateGray'],
        ['#000000', 'Black'],
      ],
      clotheColor: [
        'Black',
        'Blue01',
        'Blue02',
        'Blue03',
        'Gray01',
        'Gray02',
        'Heather',
        'PastelBlue',
        'PastelGreen',
        'PastelOrange',
        'PastelRed',
        'PastelYellow',
        'Pink',
        'Red',
        'White'
      ],
      graphicType: [
        'Bat',
        'Cumbia',
        'Deer',
        'Diamond',
        'Hola',
        'Pizza',
        'Resist',
        'Selena',
        'Bear',
        'SkullOutline',
        'Skull'
      ],
      facialHairColor: [
        'Auburn',
        'Black',
        'Blonde',
        'BlondeGolden',
        'Brown',
        'BrownDark',
        'Platinum',
        'Red'
      ],
      facialHairType: [
        'Blank',
        'BeardMedium',
        'BeardLight',
        'BeardMajestic',
        'MoustacheFancy',
        'MoustacheMagnum'
      ],
      skinColor: [
        'Tanned',
        'Yellow',
        'Pale',
        'Light',
        'Brown',
        'DarkBrown',
        'Black'
      ],
      mouthType: [
        'Concerned',
        'Default',
        'Disbelief',
        'Eating',
        'Grimace',
        'Sad',
        'ScreamOpen',
        'Serious',
        'Smile',
        'Tongue',
        'Twinkle',
        'Vomit'
      ],
      eyeType: [
        'Close',
        'Cry',
        'Default',
        'Dizzy',
        'EyeRoll',
        'Happy',
        'Hearts',
        'Side',
        'Squint',
        'Surprised',
        'Wink',
        'WinkWacky'
      ],
      clotheType: [
        'BlazerShirt',
        'BlazerSweater',
        'CollarSweater',
        'GraphicShirt',
        'Hoodie',
        'Overall',
        'ShirtCrewNeck',
        'ShirtScoopNeck',
        'ShirtVNeck'
      ],
      eyebrowType: [
        'Angry',
        'AngryNatural',
        'Default',
        'DefaultNatural',
        'FlatNatural',
        'RaisedExcited',
        'RaisedExcitedNatural',
        'SadConcerned',
        'SadConcernedNatural',
        'UnibrowNatural',
        'UpDown',
        'UpDownNatural'
      ],
      accessoriesType: [
        'Blank',
        'Kurt',
        'Prescription01',
        'Prescription02',
        'Round',
        'Sunglasses',
        'Wayfarers'
      ],
      hairColor: [
        'Red',
        'Auburn',
        'Black',
        'Blonde',
        'BlondeGolden',
        'Brown',
        'BrownDark',
        'PastelPink',
        'Platinum',
        'SilverGray'
      ],
      topColor: [
        'Black',
        'Blue01',
        'Blue02',
        'Blue03',
        'Gray01',
        'Gray02',
        'Heather',
        'PastelBlue',
        'PastelGreen',
        'PastelOrange',
        'PastelRed',
        'PastelYellow',
        'Pink',
        'Red',
        'White'
      ],
      topType: [
        'NoHair',
        'Eyepatch',
        'Hat',
        'Hijab',
        'Turban',
        'WinterHat1',
        'WinterHat2',
        'WinterHat3',
        'WinterHat4',
        'LongHairBigHair',
        'LongHairBob',
        'LongHairBun',
        'LongHairCurly',
        'LongHairCurvy',
        'LongHairDreads',
        'LongHairFrida',
        'LongHairFro',
        'LongHairFroBand',
        'LongHairNotTooLong',
        'LongHairShavedSides',
        'LongHairMiaWallace',
        'LongHairStraight',
        'LongHairStraight2',
        'LongHairStraightStrand',
        'ShortHairDreads01',
        'ShortHairDreads02',
        'ShortHairFrizzle',
        'ShortHairShaggyMullet',
        'ShortHairShortCurly',
        'ShortHairShortFlat',
        'ShortHairShortRound',
        'ShortHairShortWaved',
        'ShortHairSides',
        'ShortHairTheCaesar',
        'ShortHairTheCaesarSidePart'
      ],
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  mounted() {
    this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

    this.$axios.$get(`${process.env.API_URL}/users/me`).then(res => {
      this.user.name = res['name'] || ''
      this.user.email = res['email'] || ''
      this.user.phone = res['phone'] || ''
      this.user.avatar = res['avatar'] || {}
      this.user.birthDate.day = new Date(Date.parse(res['birth'])).getDate() || ''
      this.user.birthDate.month = new Date(Date.parse(res['birth'])).getMonth() + 1 || ''
      this.user.birthDate.year = new Date(Date.parse(res['birth'])).getFullYear() || ''
    }).catch((error) => {
      console.log(error)
    })
  },
  computed: {
    days() {
      return Array(Math.abs(1 - 31) + 1).fill(1).map((v, i) => v + i * (1 > 31 ? -1 : 1))
    },
    months() {
      return ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    },
    years() {
      return Array(Math.abs(1940 - 2020) + 1).fill(1940).map((v, i) => v + i * (1940 > 2020 ? -1 : 1)).reverse()
    },
    birthDate() {
      return new Date(Date.UTC(this.user.birthDate.year, this.user.birthDate.month - 1, this.user.birthDate.day, 0, 0, 0))
    },
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  watch: {
    'user.avatar.accessoriesType': function() {
      this.$store.commit('updateAccessoriesType', this.user.avatar.accessoriesType)
    },
    'user.avatar.facialHairColor': function() {
      this.$store.commit('updateFacialHairColor', this.user.avatar.facialHairColor)
    },
    'user.avatar.facialHairType': function() {
      this.$store.commit('updateFacialHairType', this.user.avatar.facialHairType)
    },
    'user.avatar.graphicType': function() {
      this.$store.commit('updateGraphicType', this.user.avatar.graphicType)
    },
    'user.avatar.clotheColor': function() {
      this.$store.commit('updateClotheColor', this.user.avatar.clotheColor)
    },
    'user.avatar.eyebrowType': function() {
      this.$store.commit('updateEyebrowType', this.user.avatar.eyebrowType)
    },
    'user.avatar.circleColor': function() {
      this.$store.commit('updateCircleColor', this.user.avatar.circleColor)
    },
    'user.avatar.clotheType': function() {
      this.$store.commit('updateClotheType', this.user.avatar.clotheType)
    },
    'user.avatar.hairColor': function() {
      this.$store.commit('updateHairColor', this.user.avatar.hairColor)
    },
    'user.avatar.mouthType': function() {
      this.$store.commit('updateMouthType', this.user.avatar.mouthType)
    },
    'user.avatar.skinColor': function() {
      this.$store.commit('updateSkinColor', this.user.avatar.skinColor)
    },
    'user.avatar.eyeType': function() {
      this.$store.commit('updateEyeType', this.user.avatar.eyeType)
    },
    'user.avatar.topType': function() {
      this.$store.commit('updateTopType', this.user.avatar.topType)
    },
    'user.avatar.topColor': function() {
      this.$store.commit('updateTopColor', this.user.avatar.topColor)
    },
    'user.email': function() {
      if (this.user.email.trim() !== '') {
        if (this.emailRegex.test(this.user.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    'user.password': function() {
      if (this.user.password.trim() !== '') {
        if (this.user.password.trim().length >= 5) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    },
    'user.confirm': function() {
      if (this.user.confirm.trim() !== '') {
        if (this.user.confirm.trim() === this.user.password.trim()) {
          this.errors.confirm = false
        } else {
          this.errors.confirm = true
        }
      }
    },
    'user.phone': function() {
      if (this.user.phone.trim() !== '') {
        if (this.user.phone.trim().length >= 7) {
          this.errors.phone = false
        } else {
          this.errors.phone = true
        }
      }
    },
    'user.name': function() {
      if (this.user.name.trim() !== '') {
        if (this.user.name.trim().length >= 2) {
          this.errors.name = false
        } else {
          this.errors.name = true
        }
      }
    },
    'user.birthDate.day': function() {
      if (this.user.birthDate.day !== null) {
        if (this.user.birthDate.day >= 0 && this.user.birthDate.day <= 31) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    },
    'user.birthDate.month': function() {
      if (this.user.birthDate.month !== null) {
        if (this.user.birthDate.month >= 1 && this.user.birthDate.month <= 12) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    },
    'user.birthDate.year': function() {
      if (this.user.birthDate.year !== null) {
        if (this.user.birthDate.year >= 1940 && this.user.birthDate.year <= 2020) {
          this.errors.birthDate = false
        } else {
          this.errors.birthDate = true
        }
      }
    }
  },
  methods: {
    getItems(item) {
      return this[item]
    },
    saveExtendedUser() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.user.name) {
        this.errors.name = true
      }

      if (!this.user.email) {
        this.errors.email = true
      }

      if (!this.user.phone) {
        this.errors.phone = true
      }

      if (!this.user.password) {
        this.errors.password = true
      }

      if (this.user.confirm !== this.user.password) {
        this.errors.confirm = true
      }

      if (this.user.birthDate.day <= 0 && this.user.birthDate.day >= 31) {
        this.errors.birthDate = true
      }

      if (this.user.birthDate.month <= 1 && this.user.birthDate.month >= 12) {
        this.errors.birthDate = true
      }

      if (this.user.birthDate.year <= 1940 && this.user.birthDate.year >= 2020) {
        this.errors.birthDate = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

        this.$axios({
          method: 'PATCH',
          url: `${process.env.API_URL}/users/me`,
          data: {
            name: this.user.name.trim(),
            email: this.user.email.trim(),
            password: this.user.password.trim(),
            confirm: this.user.confirm.trim(),
            phone: this.user.phone.trim(),
            avatar: this.user.avatar,
            birth: this.birthDate
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.classResponse = 'text-green-500'
            this.showResponse = true
            this.response = 'Einstellungen wurden erfolgreich geändert'
          } else if (res.status === 400) {
            this.classResponse = 'text-red-500'
            this.showResponse = true
            this.response = 'Fehler'
          } else if (res.status === 500) {
            this.classResponse = 'text-red-500'
            this.showResponse = true
            this.response = 'Fehler'
          }
        })
      }
    }
  }
}
</script>

<style>
.toggle-checkbox:checked {
  @apply: right-0 border-green-400;
  border-color: #68D391;
  right: 0;
}

.toggle-checkbox:checked+.toggle-label {
  background-color: #68D391;
  @apply: bg-green-400;
}
</style>
