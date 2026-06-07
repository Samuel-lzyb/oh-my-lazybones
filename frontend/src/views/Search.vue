<template>
  <div class="max-w-7xl mx-auto px-6 py-8">
    <div class="mb-8">
      <SearchBar
        v-model="query"
        placeholder="Search skills..."
        @search="doSearch"
      />
    </div>

    <div class="flex items-center justify-between mb-6">
      <p class="text-text-dim text-sm">
        <template v-if="query">{{ total }} results</template>
        <template v-else>Browse all skills</template>
      </p>
      <select
        v-model="sort"
        class="bg-bg-card border border-border-subtle rounded-input px-3 py-1.5 text-sm text-text-soft focus:outline-none focus:border-brand-amber/40"
        @change="doSearch"
      >
        <option value="downloads">Popular</option>
        <option value="created_at">Newest</option>
      </select>
    </div>

    <!-- Results -->
    <div v-if="skills.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkillCard v-for="skill in skills" :key="skill.name" :skill="skill" @click="goDetail(skill.name)" />
    </div>

    <!-- Loading -->
    <div v-if="loading && !skills.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkeletonCard v-for="i in 6" :key="i" />
    </div>

    <!-- Empty -->
    <div v-if="!loading && !skills.length && searched" class="text-center py-16">
      <svg class="mx-auto w-16 h-16 text-text-dim mb-4" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5">
        <ellipse cx="32" cy="36" rx="14" ry="11"/>
        <circle cx="26" cy="30" r="3" fill="currentColor"/>
        <circle cx="38" cy="30" r="3" fill="currentColor"/>
        <path d="M28 40 Q32 44 36 40"/>
      </svg>
      <p class="text-text-dim text-lg mb-2">No skills found for "{{ query }}".</p>
      <p class="text-text-dim text-sm mb-6">Try a different search, or publish the first one.</p>
      <router-link to="/publish" class="inline-block px-6 py-2.5 bg-brand-amber/10 text-brand-amber rounded-btn hover:bg-brand-amber/20 transition-colors text-sm">
        Publish a Skill
      </router-link>
    </div>

    <!-- Sentry for infinite scroll -->
    <div ref="sentryRef" class="h-4" />

    <!-- Loading more -->
    <div v-if="loading && skills.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
      <SkeletonCard v-for="i in 3" :key="i" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSkills } from '@/composables/useSkills'
import SearchBar from '@/components/SearchBar.vue'
import SkillCard from '@/components/SkillCard.vue'
import SkeletonCard from '@/components/SkeletonCard.vue'

const route = useRoute()
const router = useRouter()
const { skills, total, loading, hasMore, search, loadMore } = useSkills()

const query = ref((route.query.q as string) || '')
const sort = ref((route.query.sort as string) || 'downloads')
const searched = ref(false)
const sentryRef = ref<HTMLElement | null>(null)

function doSearch() {
  searched.value = true
  const q = query.value.trim()
  router.replace({ query: { q: q || undefined, sort: sort.value } })
  search(q)
}

let observer: IntersectionObserver | null = null

onMounted(() => {
  if (query.value) doSearch()

  observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && hasMore.value && query.value) {
      loadMore(query.value)
    }
  }, { rootMargin: '200px' })

  if (sentryRef.value) observer.observe(sentryRef.value)
})

onUnmounted(() => observer?.disconnect())

function goDetail(name: string) {
  router.push(`/skills/${name}`)
}
</script>
