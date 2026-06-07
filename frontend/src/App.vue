<template>
  <div class="min-h-screen flex flex-col">
    <nav class="sticky top-0 z-50 bg-bg-deep/95 backdrop-blur border-b border-border-subtle">
      <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <router-link to="/" class="font-display text-lg font-semibold text-text-soft hover:text-brand-amber transition-colors">
          lazybones
        </router-link>
        <div class="flex items-center gap-4">
          <router-link to="/search" class="text-text-dim hover:text-text-soft transition-colors text-sm">Search</router-link>
          <router-link to="/publish" class="text-text-dim hover:text-text-soft transition-colors text-sm">Publish</router-link>
        </div>
      </div>
    </nav>

    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Mobile bottom nav -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-bg-deep/95 backdrop-blur border-t border-border-subtle z-50">
      <div class="flex justify-around h-14 items-center">
        <router-link to="/search" class="flex flex-col items-center text-text-dim hover:text-brand-amber transition-colors text-xs gap-0.5">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          Search
        </router-link>
        <router-link to="/" class="flex flex-col items-center text-text-dim hover:text-brand-amber transition-colors text-xs gap-0.5">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
          Home
        </router-link>
        <router-link to="/publish" class="flex flex-col items-center text-text-dim hover:text-brand-amber transition-colors text-xs gap-0.5">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>
          Publish
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
