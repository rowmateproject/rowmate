<template>
<div>
  <h3 class="text-3xl font-medium text-color-title">{{ $t('createEvent') }}</h3>

  <form @submit.prevent="xxx" class="mt-3 lg:mt-8 p-3 lg:p-6 bg-color-form rounded-md shadow-md">
    <div class="flex mb-8">
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'glass-cheers']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Was ist der Anlass?</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'calendar-alt']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Wann ist der Termin?</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'question-circle']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Umfrage erstellen</h2>
        </div>
      </div>
      <div class="flex-1 flex items-center justify-center">
        <fa :icon="['fas', 'angle-double-right']" class="text-xl font-thin mx-4" />
      </div>
      <div class="w-1/4 text-center text-color-form bg-color-page rounded flex items-center justify-center h-20">
        <div class="w-1/4 flex items-center justify-start px-4">
          <fa :icon="['fas', 'clipboard-check']" class="text-2xl" />
        </div>
        <div class="w-2/3 flex flex-col items-center justify-center px-1">
          <h2 class="font-bold text-sm">Event anlegen</h2>
        </div>
      </div>
    </div>

    <div>
      <div class="mb-4">
        <label class="text-color-form" for="title">Titel</label>
        <input type="text" placeholder="Titel eingeben" required="required" maxlength="64" autocomplete="off" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1">
      </div>
      <div class="mb-4">
        <label class="text-color-form" for="location">Ort</label>
        <input type="text" placeholder="Ort hinzufügen" maxlength="256" autocomplete="off" class="w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1">
      </div>
      <div>
        <label class="text-color-form" for="hint">Notiz</label>
        <textarea rows="1" placeholder="Notiz hinzufügen" maxlength="3000" class="h-32 w-full rounded border border-color-form focus:outline-none p-2 mt-2 mb-1"></textarea>
      </div>
      <div class="flex justify-end mt-4">
        <button class="px-4 py-2 bg-gray-800 text-color-button rounded-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700">
          {{ $t('save') }}
        </button>
      </div>
    </div>
  </form>
</div>
</template>
