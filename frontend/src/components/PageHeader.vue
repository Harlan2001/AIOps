<script setup lang="ts">
defineProps<{
  title: string
  description?: string
}>()
</script>

<template>
  <header class="page-header">
    <div class="page-heading">
      <h1>{{ title }}</h1>
      <p v-if="description">{{ description }}</p>
    </div>
    <div v-if="$slots.extra" class="page-actions">
      <slot name="extra" />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.page-heading {
  min-width: 0;
}

h1 {
  margin-bottom: 7px;
  color: var(--text-primary);
  font-size: clamp(22px, 2vw, 28px);
  font-weight: 650;
  line-height: 1.25;
  letter-spacing: -0.02em;
}

p {
  max-width: 760px;
  margin-bottom: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

.page-actions {
  display: flex;
  flex: none;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
  }

  .page-actions {
    width: 100%;
  }
}
</style>
