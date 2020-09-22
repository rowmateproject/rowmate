<template>
<div>
  <h3 class="text-gray-700 text-3xl font-medium">Dashboard</h3>

  <div class="mt-4">
    <div class="flex flex-wrap -mx-6">
      <div class="w-full px-6 sm:w-1/2 xl:w-1/3">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-red-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'users']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">282</h4>
            <div class="text-gray-500">Registrierte Nutzer</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 sm:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-orange-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'network-wired']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">2.021</h4>
            <div class="text-gray-500">Registrierte Vereine</div>
          </div>
        </div>
      </div>

      <div class="w-full mt-6 px-6 sm:w-1/2 xl:w-1/3 xl:mt-0">
        <div class="flex items-center px-5 py-6 shadow-sm rounded-md bg-white">
          <div class="flex items-center justify-center rounded-full bg-green-600 bg-opacity-75 w-16 h-16">
            <fa :icon="['fas', 'calendar-alt']" class="text-gray-250 text-3xl" />
          </div>

          <div class="mx-5">
            <h4 class="text-2xl font-semibold text-gray-700">542</h4>
            <div class="text-gray-500">Veranstaltungen</div>
          </div>
        </div>
      </div>
    </div>
  </div>

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
            <tr v-for="(u, index) in users" :key="index">
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img class="h-10 w-10 rounded-full" :src="avatar" alt="" />
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
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">{{ u.status }}</span>
              </td>

              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500">
                {{ u.role }}
              </td>

              <td class="px-6 py-4 whitespace-no-wrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
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

export default {
  data() {
    return {
      mockupUser: {
        name: 'John Doe',
        email: 'john@example.com',
        title: 'Software Engineer',
        title2: 'Web dev',
        status: 'Active',
        role: 'Owner',
      }
    }
  },
  computed: {
    avatar() {
      return new AvatarGenerator().generateRandomAvatar()
    },
    users() {
      return [...Array(10).keys()].map(() => this.mockupUser)
    }
  }
}
</script>
