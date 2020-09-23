<template>
<div>
  <h3 class="text-gray-700 text-3xl font-medium">Nutzer</h3>


  <div class="mt-8"></div>

  <div class="flex flex-col mt-8">
    <div class="-my-2 py-2 overflow-x-auto sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
      <div class="align-middle inline-block min-w-full shadow overflow-hidden sm:rounded-lg border-b border-gray-200">
        <table class="min-w-full">
          <thead>
            <tr>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50"></th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="(u, index) in users" :key="index" :class="{ 'shadow':u.is_active}">
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <userAvatar :avatar="u.avatar"></userAvatar>
                    <!--- <img class="h-10 w-10 rounded-full" :src="avatar" alt="" /> -->
                  </div>

                  <div class="ml-4">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      {{ u.name }}
                    </div>
                    <div class="text-sm leading-5 text-gray-500">
                      {{ u.email }}
                    </div>
                  </div>
                </div>
              </td>

              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="text-sm leading-5 text-gray-900">
                  {{ u.title }}
                </div>
                <div class="text-sm leading-5 text-gray-500">
                  {{ u.title2 }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <span class="px-2 text-xs leading-5 font-semibold rounded-full" :class="[ u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' ]"><fa :icon="['fas', 'user']" class="mr-2"  />{{ u.is_active ? 'Aktiv' : 'Inaktiv'}}</span>
                <span class="px-2 text-xs leading-5 font-semibold rounded-full" :class="[ u.is_confirmed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' ]"><fa :icon="['fas', 'envelope']" class="mr-2"  />{{ u.is_confirmed ? 'Ja' : 'Nein'}}</span>
                <span class="px-2 text-xs leading-5 font-semibold rounded-full" :class="[ u.is_accepted ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' ]"><fa :icon="['fas', 'user-edit']" class="mr-2"  />{{ u.is_accepted ? 'Ja' : 'Nein'}}</span>
              </td>

              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500" v-if="u.is_superuser">
                Superuser
              </td>
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500" v-else>
                User
              </td>

              <td class="px-6 py-4 whitespace-no-wrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                <button v-on:click="deactivateUser(u.id, index)" class="text-indigo-600 hover:text-indigo-900" v-if="u.is_active">Deaktivieren</button>
                <button v-on:click="activateUser(u.id, index)" class="text-indigo-600 hover:text-indigo-900" v-else>Aktivieren</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import {
  AvatarGenerator
} from 'random-avatar-generator'
import Avataaars from 'vuejs-avataaars'
import userAvatar from '../userAvatar'


export default {
  data() {
    return {
      users: []
    }
  },
  methods: {
    activateUser: function (uuid, index) {
      this.$axios.$get(`${process.env.API_URL}/user/activate/` + uuid).then(data => {
        this.users[index].is_active = !this.users[index].is_active
        this.users[index].is_accepted = true
      })
    },
    deactivateUser: function (uuid, index) {
      this.$axios.$get(`${process.env.API_URL}/user/deactivate/` + uuid).then(data => {
        this.users[index].is_active = !this.users[index].is_active
      })
    }
  },
  mounted: function () {
    this.$axios.setHeader('Authorization', 'Bearer ' + this.$store.state.accessToken)

    this.$axios.$get(`${process.env.API_URL}/dashboard/users`).then(data => {
      this.users = data.users
    })
  },
  computed: {
    avatar() {
      return new AvatarGenerator().generateRandomAvatar()
    }
  },
  components: {
    Avataaars,
    userAvatar
  }
}
</script>
