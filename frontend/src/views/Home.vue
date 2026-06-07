<template>
  <div class="max-w-7xl mx-auto px-6 pt-24 pb-12">
    <!-- Hero -->
    <div class="text-center mb-12">
      <div class="mb-8">
        <svg class="mx-auto w-28 h-28 text-brand-amber" viewBox="0 0 112 112" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <!-- Head -->
          <ellipse cx="56" cy="62" rx="26" ry="22"/>
          <!-- Eye patches -->
          <path d="M36 54 Q40 48 46 54" stroke-width="2"/>
          <path d="M66 54 Q70 48 76 54" stroke-width="2"/>
          <!-- Eyes — half-lidded -->
          <path d="M38 58 Q42 56 46 58" stroke-width="1.5"/>
          <path d="M66 58 Q70 56 74 58" stroke-width="1.5"/>
          <!-- Nose -->
          <ellipse cx="56" cy="64" rx="4" ry="3"/>
          <!-- Smile -->
          <path d="M48 72 Q56 78 64 72" stroke-width="1.5"/>
          <!-- Left arm -->
          <path d="M30 54 Q18 58 14 72 Q12 80 18 84" stroke-width="2"/>
          <!-- Right arm -->
          <path d="M82 54 Q94 58 98 72 Q100 80 94 84" stroke-width="2"/>
          <!-- Claws -->
          <path d="M14 82 L12 86" stroke-width="2"/>
          <path d="M18 84 L18 88" stroke-width="2"/>
          <path d="M98 82 L100 86" stroke-width="2"/>
          <path d="M94 84 L94 88" stroke-width="2"/>
          <!-- Brows -->
          <path d="M34 46 Q40 42 48 44" stroke-width="1"/>
          <path d="M64 44 Q72 42 78 46" stroke-width="1"/>
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
