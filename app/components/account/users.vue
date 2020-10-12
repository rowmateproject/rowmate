<template>
<div>
  <h3 class="text-xl sm:text-2xl md:text-3xl font-medium text-color-title">Nutzer</h3>

  <div class="mt-1 sm:mt-3 md:mt-5 lg:mt-8 p-3 lg:px-6 lg:pb-6 lg:pt-4 bg-svg-image bg-blue-500 rounded-md shadow">
    <h4 class="text-color-nav">Nutzer Filter</h4>
    <user-filter @resultObject="handleUserFilter" @resetFilter="handleUserReset" :showResetButton="true" />
  </div>

  <div class="bg-color-image mt-1 sm:mt-3 md:mt-5 lg:mt-8 px-3 lg:px-6 pb-3 lg:pb-6 pt-2 lg:pt-4 rounded shadow">
    <h4 class="text-xl mb-1">Benutzer einladen</h4>
    <p>Alleine arbeiten macht keinen Spass. Lade weitere Benutzer ein und bestimme deren Zugriffsrechte. Du kannst diese jederzeit ändern.</p>
  </div>

  <div v-if="users.length > 0" class="flex flex-col mt-8">
    <div class="overflow-x-auto">
      <div class="min-w-full align-middle inline-block shadow overflow-hidden rounded">
        <table class="min-w-full">
          <thead class="bg-color-image text-gray-900">
            <tr>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('name') }}
              </th>
              <th class="py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('status') }}
              </th>
              <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                {{ $t('role') }}
              </th>
              <th class="px-6 py-6"></th>
            </tr>
          </thead>
          <tbody class="bg-color-form">
            <tr v-for="(u, index) in users" :key="index" class="border-b-2 border-gray-200">
              <td class="px-6 py-4 whitespace-no-wrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <avatar :avatar="u.avatar" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      {{ u.name }}
                    </div>
                    <div class="text-sm leading-5 text-color-body">
                      {{ u.email }}
                    </div>
                  </div>
                </div>
              </td>

              <td class="text-xs leading-5 font-semibold">
                <div class="grid grid-cols-12 gap-6">
                  <span :class="[u.is_active ? 'text-green-800' : 'text-red-700']" class="col-span-5 lg:col-span-4 pt-1">
                    <fa :icon="['fas', 'user']" class="mr-2" />
                    <span>{{ u.is_active ? 'Aktiv' : 'Inaktiv'}}</span>
                  </span>
                  <span :class="[u.is_confirmed ? 'text-green-800' : 'text-red-700']" class="col-span-4 lg:col-span-4 pt-1">
                    <fa :icon="['fas', 'envelope']" class="mr-2" />
                    <span>{{ u.is_confirmed ? 'Ja' : 'Nein'}}</span>
                  </span>
                  <span :class="[u.is_accepted ? 'text-green-800' : 'text-red-700']" class="col-span-3 lg:col-span-4 pt-1">
                    <fa :icon="['fas', 'user-edit']" class="mr-2" />
                    <span>{{ u.is_accepted ? 'Ja' : 'Nein'}}</span>
                  </span>
                </div>
              </td>

              <td class="px-6 py-4 whitespace-no-wrap text-sm leading-5 text-color-body">
                {{ u.is_superuser ? 'Administrator' : 'Nutzer' }}
              </td>

              <td class="px-6 py-4 whitespace-no-wrap text-right text-sm leading-5 font-medium">
                <button v-if="u.is_active" @click="deactivateUser(u.id, index)" class="text-color-link focus:outline-none">Deaktivieren</button>
                <button v-else @click="activateUser(u.id, index)" class="text-color-link focus:outline-none">Aktivieren</button>
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
      users: [],
      usersBackup: []
    }
  },
  mounted() {
    this.$axios({
      method: 'GET',
      url: `${process.env.API_URL}/manage/users/list`,
      validateStatus: () => true
    }).then((res) => {
      if (res.status === 200) {
        this.users = res.data.users
        this.usersBackup = res.data.users
      } else {
        console.debug(res.data)
      }
    })
  },
  methods: {
    handleUserFilter(value) {
      this.users = [value.user]
    },
    handleUserReset(value) {
      if (value === true) {
        this.users = this.usersBackup
      }
    },
    activateUser(uuid, index) {
      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/manage/users/activate/${uuid}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          this.users[index].is_active = !this.users[index].is_active
          this.users[index].is_accepted = true
        } else {
          console.debug(res.data)
        }
      })
    },
    deactivateUser(uuid, index) {
      this.$axios({
        method: 'POST',
        url: `${process.env.API_URL}/manage/users/deactivate/${uuid}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          this.users[index].is_active = !this.users[index].is_active
        } else {
          console.debug(res.data)
        }
      })
    }
  }
}
</script>
