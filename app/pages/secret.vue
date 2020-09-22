<template>
<div class="container mx-auto flex justify-center items-center">
  <div class="text-center">
    <p class="mb-6 text-gray-250 text-2xl">Du bist auf einer geheimen Mission</p>
    <h1 class="animate-bounce p-4">
      <nuxt-link to="/" class="text-white text-6xl">Back home</nuxt-link>
    </h1>
  </div>
</div>
</template>

<script>
export default {
  middleware: 'authenticated'
}
</script>
