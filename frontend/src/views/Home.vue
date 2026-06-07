<template>
  <div class="max-w-7xl mx-auto px-6 pt-24 pb-12">
    <!-- Hero -->
    <div class="text-center mb-12">
      <div class="mb-8">
        <svg class="mx-auto w-24 h-24 text-text-dim" viewBox="0 0 96 96" fill="none" stroke="currentColor" stroke-width="1.5">
          <ellipse cx="48" cy="52" rx="20" ry="16"/>
          <circle cx="38" cy="42" r="5" fill="currentColor"/>
          <circle cx="58" cy="42" r="5" fill="currentColor"/>
          <path d="M42 58 Q48 64 54 58" stroke-width="2"/>
          <path d="M24 44 Q20 30 32 24 Q44 18 48 28"/>
          <path d="M72 44 Q76 30 64 24 Q52 18 48 28"/>
        </svg>
      </div>
      <h1 class="font-display text-4xl md:text-5xl font-bold text-text-soft mb-4">
        Discover Agent Skills.
      </h1>
      <p class="text-text-dim text-lg mb-8 max-w-xl mx-auto">
        Install in one command. Let your Agent do the work.
      </p>
      <div class="max-w-2xl mx-auto mb-8">
        <SearchBar
          v-model="query"
          placeholder="What do you want your Agent to do?"
          @search="goSearch"
        />
      </div>
    </div>

    <!-- Stats -->
    <StatsBar
      v-if="stats"
      :stats="[
        { label: 'Skills', value: stats.skills },
        { label: 'Authors', value: stats.authors },
        { label: 'Installs', value: stats.installs },
      ]"
    />

    <!-- Popular Skills -->
    <section class="mt-16">
      <div class="flex items-center justify-between mb-6">
        <h2 class="font-display text-xl font-semibold text-text-soft">Popular Skills</h2>
        <router-link to="/search?sort=downloads" class="text-text-dim hover:text-brand-amber text-sm transition-colors">View all</router-link>
      </div>
      <div v-if="popular.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SkillCard v-for="skill in popular" :key="skill.name" :skill="skill" @click="goDetail(skill.name)" />
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SkeletonCard v-for="i in 6" :key="i" />
      </div>
    </section>

    <!-- Recent Skills -->
    <section class="mt-16">
      <div class="flex items-center justify-between mb-6">
        <h2 class="font-display text-xl font-semibold text-text-soft">Recently Added</h2>
        <router-link to="/search?sort=created_at" class="text-text-dim hover:text-brand-amber text-sm transition-colors">View all</router-link>
      </div>
      <div v-if="recent.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SkillCard v-for="skill in recent" :key="skill.name" :skill="skill" @click="goDetail(skill.name)" />
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SkeletonCard v-for="i in 3" :key="i" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { searchSkills, getStats, type Skill, type Stats } from '@/api/client'
import SearchBar from '@/components/SearchBar.vue'
import StatsBar from '@/components/StatsBar.vue'
import SkillCard from '@/components/SkillCard.vue'
import SkeletonCard from '@/components/SkeletonCard.vue'

const router = useRouter()
const query = ref('')
const popular = ref<Skill[]>([])
const recent = ref<Skill[]>([])
const stats = ref<Stats | null>(null)

onMounted(async () => {
  try {
    const [popRes, recentRes, statsRes] = await Promise.all([
      searchSkills('', 1, 6, 'downloads'),
      searchSkills('', 1, 6, 'created_at'),
      getStats(),
    ])
    popular.value = popRes.items
    recent.value = recentRes.items
    stats.value = statsRes
  } catch {
    // Silent degrade
  }
})

function goSearch() {
  if (query.value.trim()) {
    router.push({ path: '/search', query: { q: query.value } })
  }
}

function goDetail(name: string) {
  router.push(`/skills/${name}`)
}

// Keyboard shortcut
function onKeydown(e: KeyboardEvent) {
  if (e.key === '/' && document.activeElement?.tagName !== 'INPUT') {
    e.preventDefault()
    const el = document.querySelector<HTMLInputElement>('input[type="text"]')
    el?.focus()
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
</script>
