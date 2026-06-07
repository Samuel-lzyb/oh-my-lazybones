<template>
  <div class="flex justify-center gap-8 md:gap-16 py-8">
    <div v-for="stat in stats" :key="stat.label" class="text-center">
      <p class="font-display text-2xl md:text-3xl font-semibold text-brand-amber">{{ stat.value.toLocaleString() }}</p>
      <p class="text-text-dim text-sm mt-1">{{ stat.label }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stats: { label: string; value: number }[]
}>()
</script>
