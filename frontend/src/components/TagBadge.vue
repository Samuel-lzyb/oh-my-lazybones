<template>
  <span class="inline-block px-2.5 py-1 text-xs rounded-btn bg-brand-amber/10 text-brand-amber">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
defineProps<{ label: string }>()
</script>
