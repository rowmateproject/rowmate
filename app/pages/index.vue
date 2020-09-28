<template>
<div class="flex flex-col items-center">
  <logo class="w-full max-w-4xl mt-12 sm:mt-24 md:mt-32 lg:mt-48" />
  <p class="text-center text-color-nav text-10xl font-normal mt-6">rowmate.org</p>
</div>
</template>

<script>
export default {
  middleware: 'notAuthenticated'
}
</script>
