<template>
  <div class="max-w-5xl mx-auto px-6 py-8">
    <h1 class="font-display text-2xl font-bold text-text-soft mb-8">Publish a Skill</h1>

    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Form -->
      <div class="flex-1 space-y-6">
        <div>
          <label class="block text-text-soft text-sm mb-2">
            Name <span class="text-text-dim">*</span>
            <span v-if="valid.name" class="text-accent-green ml-2">&#10003;</span>
          </label>
          <input
            v-model="form.name"
            type="text"
            class="w-full bg-bg-card border border-border-subtle rounded-input px-4 py-3 text-text-soft placeholder:text-text-dim focus:outline-none focus:border-brand-amber/40 transition-colors"
            placeholder="my-awesome-skill"
            maxlength="64"
            @input="validate"
          />
          <p class="text-text-dim text-xs mt-1">Lowercase letters, numbers, hyphens. 3-64 chars.</p>
        </div>

        <div>
          <label class="block text-text-soft text-sm mb-2">
            Author <span class="text-text-dim">*</span>
            <span v-if="valid.author" class="text-accent-green ml-2">&#10003;</span>
          </label>
          <input
            v-model="form.author"
            type="text"
            class="w-full bg-bg-card border border-border-subtle rounded-input px-4 py-3 text-text-soft placeholder:text-text-dim focus:outline-none focus:border-brand-amber/40 transition-colors"
            placeholder="your-name"
            maxlength="64"
            @input="validate"
          />
        </div>

        <div>
          <label class="block text-text-soft text-sm mb-2">
            Description <span class="text-text-dim">*</span>
            <span v-if="valid.description" class="text-accent-green ml-2">&#10003;</span>
          </label>
          <textarea
            v-model="form.description"
            class="w-full bg-bg-card border border-border-subtle rounded-input px-4 py-3 text-text-soft placeholder:text-text-dim focus:outline-none focus:border-brand-amber/40 transition-colors resize-none"
            rows="4"
            placeholder="What does your skill do? Describe it clearly..."
            maxlength="2000"
            @input="validate"
          />
          <p class="text-text-dim text-xs mt-1">{{ form.description.length }}/2000</p>
        </div>

        <div>
          <label class="block text-text-soft text-sm mb-2">Tags</label>
          <div class="flex flex-wrap gap-2 mb-2">
            <span
              v-for="tag in form.tags"
              :key="tag"
              class="inline-flex items-center gap-1 px-2.5 py-1 text-xs rounded-btn bg-brand-amber/10 text-brand-amber cursor-pointer hover:bg-brand-amber/20 transition-colors"
              @click="removeTag(tag)"
            >
              {{ tag }}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </span>
          </div>
          <input
            v-model="tagInput"
            type="text"
            class="w-full bg-bg-card border border-border-subtle rounded-input px-4 py-2.5 text-text-soft placeholder:text-text-dim focus:outline-none focus:border-brand-amber/40 transition-colors text-sm"
            placeholder="Add a tag and press Enter..."
            maxlength="32"
            @keydown.enter.prevent="addTag"
          />
        </div>

        <button
          class="w-full py-3 bg-brand-amber/10 text-brand-amber rounded-btn hover:bg-brand-amber/20 transition-colors font-medium disabled:opacity-40 disabled:cursor-not-allowed"
          :disabled="!canSubmit || submitting"
          @click="submit"
        >
          {{ submitting ? 'Publishing...' : 'Publish Skill' }}
        </button>
      </div>

      <!-- Live Preview -->
      <div class="flex-1">
        <p class="text-text-dim text-xs mb-3 uppercase tracking-wide">Live Preview</p>
        <SkillCard :skill="previewSkill" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { createSkill } from '@/api/client'
import SkillCard from '@/components/SkillCard.vue'

const router = useRouter()
const submitting = ref(false)
const tagInput = ref('')

const form = reactive({
  name: '',
  author: '',
  description: '',
  tags: [] as string[],
})

const valid = reactive({
  name: false,
  author: false,
  description: false,
})

function validate() {
  valid.name = /^[a-z0-9-]{3,64}$/.test(form.name)
  valid.author = form.author.length >= 1 && form.author.length <= 64
  valid.description = form.description.length >= 1 && form.description.length <= 2000
}

const canSubmit = computed(() => valid.name && valid.author && valid.description)

const previewSkill = computed(() => ({
  id: '',
  name: form.name || 'your-skill',
  version: '0.1.0',
  author: form.author || 'you',
  description: form.description || 'Your skill description will appear here.',
  tags: form.tags,
  downloads: 0,
  created_at: '',
  updated_at: '',
}))

function addTag() {
  const tag = tagInput.value.trim().toLowerCase()
  if (tag && !form.tags.includes(tag) && form.tags.length < 10) {
    form.tags.push(tag)
  }
  tagInput.value = ''
}

function removeTag(tag: string) {
  form.tags = form.tags.filter(t => t !== tag)
}

async function submit() {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  try {
    await createSkill({
      name: form.name,
      author: form.author,
      description: form.description,
      tags: form.tags,
    })
    router.push(`/skills/${form.name}`)
  } catch {
    submitting.value = false
  }
}
</script>
