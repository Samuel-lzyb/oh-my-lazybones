<template>
  <div
    class="bg-bg-card rounded-card p-6 transition-all duration-200 cursor-pointer group hover:-translate-y-0.5 hover:shadow-[0_2px_16px_rgba(245,158,11,0.06)] hover:ring-1 hover:ring-brand-amber/20"
    @click="$emit('click')"
  >
    <h3 class="font-display text-lg font-semibold text-text-soft mb-1 truncate">{{ skill.name }}</h3>
    <p class="text-text-dim text-xs mb-3">
      v{{ skill.version }} &middot; @{{ skill.author }}
    </p>

    <p v-if="skill.description" class="text-text-dim text-sm mb-4 line-clamp-2">
      {{ skill.description }}
    </p>

    <div v-if="skill.tags.length" class="flex flex-wrap gap-2 mb-4">
      <TagBadge v-for="tag in skill.tags" :key="tag" :label="tag" />
    </div>

    <p class="text-accent-green text-sm flex items-center gap-1">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      {{ skill.downloads.toLocaleString() }} installs
    </p>

    <!-- Hover install command -->
    <div class="max-h-0 overflow-hidden group-hover:max-h-12 transition-all duration-300 ease-out mt-4 border-t border-border-subtle pt-3">
      <div class="flex items-center justify-between gap-2">
        <code class="font-mono text-sm text-text-soft truncate">$ lazy install {{ skill.name }}</code>
        <button
          class="shrink-0 px-3 py-1 text-xs text-brand-amber border border-brand-amber/30 rounded-btn hover:bg-brand-amber/10 transition-colors"
          @click.stop="copy"
        >
          {{ copied ? 'Copied' : 'Copy' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Skill } from '@/api/client'
import TagBadge from './TagBadge.vue'

defineProps<{ skill: Skill }>()
defineEmits<{ click: [] }>()

const copied = ref(false)

async function copy() {
  await navigator.clipboard.writeText(`lazy install ${(defineProps as any).skill?.name}`)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
</script>
