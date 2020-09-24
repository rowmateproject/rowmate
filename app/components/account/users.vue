<template>
<div>
  <h3 class="text-gray-700 text-3xl font-medium">Nutzer</h3>

  <div class="flex flex-col mt-8">
    <div class="-my-2 py-2 overflow-x-auto sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
      <div class="align-middle inline-block min-w-full shadow overflow-hidden sm:rounded-lg border-b border-gray-200">
        <table class="table-fixed min-w-full">
          <thead>
            <tr>
              <th class="w-3/12 px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('name') }}
              </th>
              <th class="w-2/12 px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('membercategory') }}
              </th>
              <th class="w-3/12 px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('status') }}
              </th>
              <th class="w-2/12 px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('role') }}
              </th>
              <th class="w-2/12 px-6 py-3 border-b border-gray-200 bg-gray-50"></th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="(u, index) in users" :key="index" :class="{'shadow': u.is_active}">
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <avatar :avatar="u.avatar" />
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

              <td class="grid grid-cols-3 gap-3 p-6 border-b border-gray-200">
                <span :class="[u.is_active ? 'text-green-800' : 'text-red-800']" class="pt-1 px-2 text-xs leading-5 font-semibold">
                  <fa :icon="['fas', 'user']" class="mr-2" />{{ u.is_active ? 'Aktiv' : 'Inaktiv'}}
                </span>
                <span :class="[u.is_confirmed ? 'text-green-800' : 'text-red-800']" class="pt-1 px-2 text-xs leading-5 font-semibold">
                  <fa :icon="['fas', 'envelope']" class="mr-2" />{{ u.is_confirmed ? 'Ja' : 'Nein'}}
                </span>
                <span :class="[u.is_accepted ? 'text-green-800' : 'text-red-800']" class="pt-1 px-2 text-xs leading-5 font-semibold">
                  <fa :icon="['fas', 'user-edit']" class="mr-2" />{{ u.is_accepted ? 'Ja' : 'Nein'}}
                </span>
              </td>

              <td v-if="u.is_superuser" class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500">
                Superuser
              </td>
              <td v-else class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500">
                User
              </td>

              <td class="px-6 py-4 whitespace-no-wrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                <button v-if="u.is_active" @click="deactivateUser(u.id, index)" class="text-indigo-600 hover:text-indigo-900">Deaktivieren</button>
                <button v-else @click="activateUser(u.id, index)" class="text-indigo-600 hover:text-indigo-900">Aktivieren</button>
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
import Avataaars from 'vuejs-avataaars'

export default {
  components: {
    Avataaars
  },
  data() {
    return {
      users: []
    }
  },
  computed: {
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  mounted() {
    this.$axios.setHeader('Authorization', `Bearer ${this.accessToken}`)

    this.$axios.$get(`${process.env.API_URL}/manage/users/list`).then(res => {
      this.users = res.users
    })
  },
  methods: {
    activateUser(uuid, index) {
      this.$axios.$get(`${process.env.API_URL}/manage/users/activate/${uuid}`).then(res => {
        this.users[index].is_active = !this.users[index].is_active
        this.users[index].is_accepted = true
      })
    },
    deactivateUser(uuid, index) {
      this.$axios.$get(`${process.env.API_URL}/manage/users/deactivate/${uuid}`).then(res => {
        this.users[index].is_active = !this.users[index].is_active
      })
    }
  }
}
</script>
