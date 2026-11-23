<script setup lang="ts">
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'

withDefaults(defineProps<{
  loading?: boolean
  error?: string
  empty?: boolean
  loadingRows?: number
  emptyText?: string
  errorTitle?: string
}>(), {
  loading: false,
  error: '',
  empty: false,
  loadingRows: 4,
  emptyText: '暂无数据',
  errorTitle: '暂时无法加载',
})

defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="state-block" aria-live="polite">
    <a-skeleton v-if="loading" active :paragraph="{ rows: loadingRows }" />
    <div v-else-if="error" class="error-state" role="alert">
      <ExclamationCircleOutlined class="error-icon" />
      <h3>{{ errorTitle }}</h3>
      <p>{{ error }}</p>
      <a-button @click="$emit('retry')">重新加载</a-button>
    </div>
    <a-empty v-else-if="empty" :description="emptyText" />
    <slot v-else />
  </div>
</template>

<style scoped>
.state-block {
  min-height: 120px;
}

.error-state {
  display: flex;
  min-height: 180px;
  padding: 24px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.error-icon {
  margin-bottom: 12px;
  color: var(--danger);
  font-size: 28px;
}

h3 {
  margin-bottom: 6px;
  font-size: 16px;
}

p {
  max-width: 560px;
  margin-bottom: 16px;
  color: var(--text-secondary);
  overflow-wrap: anywhere;
}
</style>
