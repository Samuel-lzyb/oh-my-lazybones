<template>
  <div class="max-w-3xl mx-auto px-6 py-8">
    <button
      class="text-text-dim hover:text-text-soft transition-colors text-sm flex items-center gap-1 mb-8"
      @click="router.back()"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m15 18-6-6 6-6"/></svg>
      Back to results
    </button>

    <!-- Loading -->
    <template v-if="loading">
      <div class="animate-pulse">
        <div class="h-8 bg-bg-hover rounded w-1/2 mb-4"></div>
        <div class="h-4 bg-bg-hover rounded w-1/3 mb-6"></div>
        <div class="h-24 bg-bg-hover rounded mb-6"></div>
      </div>
    </template>

    <!-- Error -->
    <template v-else-if="error">
      <div class="text-center py-16">
        <p class="text-text-dim text-lg">Skill not found.</p>
        <router-link to="/" class="text-brand-amber hover:text-brand-deep transition-colors text-sm mt-4 inline-block">Go home</router-link>
      </div>
    </template>

    <!-- Detail -->
    <template v-else-if="skill">
      <h1 class="font-display text-3xl font-bold text-text-soft mb-2">{{ skill.name }}</h1>
      <p class="text-text-dim text-sm mb-6">
        v{{ skill.version }} &middot; @{{ skill.author }} &middot; {{ skill.downloads.toLocaleString() }} installs
      </p>

      <!-- Install command (hero element) -->
      <div class="bg-bg-card border border-brand-amber/20 rounded-card p-6 mb-8">
        <p class="text-text-dim text-xs mb-3 uppercase tracking-wide">Install</p>
        <div class="flex items-center justify-between gap-4">
          <code class="font-mono text-lg text-text-soft">$ lazy install {{ skill.name }}</code>
          <button
            class="shrink-0 px-5 py-2.5 text-sm text-brand-amber border border-brand-amber/30 rounded-btn hover:bg-brand-amber/10 transition-colors flex items-center gap-2"
            @click="copy"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            {{ copied ? 'Copied' : 'Copy' }}
          </button>
        </div>
      </div>

      <!-- Description -->
      <div class="mb-8">
        <p class="text-text-soft leading-relaxed whitespace-pre-wrap">{{ skill.description }}</p>
      </div>

      <!-- Tags -->
      <div v-if="skill.tags.length" class="mb-8">
        <p class="text-text-dim text-xs mb-3 uppercase tracking-wide">Tags</p>
        <div class="flex flex-wrap gap-2">
          <TagBadge v-for="tag in skill.tags" :key="tag" :label="tag" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSkill, type Skill } from '@/api/client'
import TagBadge from '@/components/TagBadge.vue'

const props = defineProps<{ name: string }>()
const router = useRouter()

const skill = ref<Skill | null>(null)
const loading = ref(true)
const error = ref(false)
const copied = ref(false)

onMounted(async () => {
  try {
    skill.value = await getSkill(props.name)
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})

async function copy() {
  await navigator.clipboard.writeText(`lazy install ${props.name}`)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
</script>
