<script setup lang="ts">
import { computed } from 'vue'
import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  SyncOutlined,
} from '@ant-design/icons-vue'

type Tone = 'success' | 'warning' | 'error' | 'processing' | 'neutral'

const props = defineProps<{
  status?: string | null
  label?: string
  tone?: Tone
}>()

const labels: Record<string, string> = {
  ok: '正常',
  success: '成功',
  normal: '正常',
  degraded: '降级',
  warning: '需关注',
  error: '异常',
  failed: '失败',
  correct: '已标正确',
  wrong: '已标错误',
  unannotated: '未标注',
  running: '进行中',
  loading: '加载中',
  biz: '业务报错',
  noise: '噪音',
  ora: 'DBA 技术错误',
  other: '其他/未识别',
  escalated: '已升级',
}

const successStates = new Set(['ok', 'success', 'normal', 'correct'])
const warningStates = new Set(['degraded', 'warning', 'wrong', 'missing_params'])
const errorStates = new Set(['error', 'failed'])
const processingStates = new Set(['running', 'loading', 'processing', 'escalated'])

const normalized = computed(() => props.status?.toLowerCase() ?? '')
const text = computed(() => props.label ?? labels[normalized.value] ?? props.status ?? '未知')
const currentTone = computed<Tone>(() => {
  if (props.tone) return props.tone
  if (successStates.has(normalized.value)) return 'success'
  if (warningStates.has(normalized.value)) return 'warning'
  if (errorStates.has(normalized.value)) return 'error'
  if (processingStates.has(normalized.value)) return 'processing'
  return 'neutral'
})
const color = computed(() => currentTone.value === 'neutral' ? undefined : currentTone.value)
</script>

<template>
  <a-tag :color="color" class="status-tag">
    <CheckCircleOutlined v-if="currentTone === 'success'" />
    <ExclamationCircleOutlined v-else-if="currentTone === 'warning'" />
    <CloseCircleOutlined v-else-if="currentTone === 'error'" />
    <SyncOutlined v-else-if="currentTone === 'processing'" :spin="normalized === 'loading'" />
    <span>{{ text }}</span>
  </a-tag>
</template>

<style scoped>
.status-tag {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  margin-inline-end: 0;
  line-height: 22px;
  white-space: nowrap;
}
</style>
