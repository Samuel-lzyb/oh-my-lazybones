import { ref } from 'vue'
import { searchSkills, type Skill, type PaginatedResponse } from '@/api/client'

export function useSkills() {
  const skills = ref<Skill[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const page = ref(1)
  const hasMore = ref(true)

  async function search(q: string, reset = true) {
    if (reset) {
      skills.value = []
      page.value = 1
      hasMore.value = true
    }

    loading.value = true
    error.value = null

    try {
      const data: PaginatedResponse<Skill> = await searchSkills(q, page.value, 20)
      if (reset) {
        skills.value = data.items
      } else {
        skills.value.push(...data.items)
      }
      total.value = data.total
      hasMore.value = skills.value.length < data.total
      page.value++
    } catch (e) {
      error.value = 'Failed to load skills'
    } finally {
      loading.value = false
    }
  }

  async function loadMore(q: string) {
    if (loading.value || !hasMore.value) return
    await search(q, false)
  }

  return { skills, total, loading, error, hasMore, search, loadMore }
}
