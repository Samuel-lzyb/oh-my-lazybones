<template>
  <div class="relative">
    <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-dim" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
    </svg>
    <input
      ref="inputRef"
      :value="modelValue"
      type="text"
      :placeholder="placeholder"
      class="w-full bg-bg-card border border-border-subtle rounded-input py-3.5 pl-12 pr-4 text-text-soft placeholder:text-text-dim focus:outline-none focus:border-brand-amber/40 transition-colors text-base"
      @input="onInput"
      @keydown.enter="onEnter"
    />
    <button
      v-if="modelValue"
      class="absolute right-4 top-1/2 -translate-y-1/2 text-text-dim hover:text-text-soft transition-colors"
      @click="$emit('update:modelValue', '')"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

defineProps<{
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: []
}>()

const inputRef = ref<HTMLInputElement | null>(null)
let timer: ReturnType<typeof setTimeout> | null = null

function onInput(e: Event) {
  const value = (e.target as HTMLInputElement).value
  emit('update:modelValue', value)
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => emit('search'), 300)
}

function onEnter() {
  if (timer) clearTimeout(timer)
  emit('search')
}

function focus() {
  inputRef.value?.focus()
}

onMounted(() => {
  focus()
})

defineExpose({ focus })
</script>
