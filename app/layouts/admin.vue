<template>
<div class="flex min-h-screen bg-gray-200 font-roboto">
  <sidebar />

  <div class="flex-1 flex flex-col overflow-hidden">
    <searchbar />

    <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200">
      <div class="container mx-auto px-6 py-8">
        <nuxt />
      </div>
    </main>
  </div>
</div>
</template>
