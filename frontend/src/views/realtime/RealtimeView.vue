<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'

import { getRealtimeAlarms, getRealtimeDetail } from '@/api/realtime'
import { ApiError } from '@/api/client'
import type { DiagLogItem } from '@/types/contract'
import { labelNull } from '@/utils/label'
import { REALTIME_SOURCE_LABELS } from '@/constants/sources'

const PAGE_SIZE = 10

const items = ref<DiagLogItem[]>([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)
const errorMsg = ref('')
const lastUpdated = ref('')

// 自动刷新（体现“实时”）：默认开启，每 10 秒拉一次最新结果。
const autoRefresh = ref(true)
const REFRESH_INTERVAL = 10000
let timer: ReturnType<typeof setInterval> | null = null

// 分类标签配色
const classColor: Record<string, string> = {
  biz: 'red',
  noise: 'default',
  ora: 'orange',
  other: 'blue',
  error: 'volcano',
}

const columns = [
  { title: 'ID', dataIndex: 'id', width: 70 },
  { title: '业务日期', dataIndex: 'business_date', width: 110 },
  { title: '来源', dataIndex: 'source', width: 110 },
  { title: '预警内容', dataIndex: 'error_text' },
  { title: '分类', dataIndex: 'diag_class', width: 90 },
  { title: '诊断类型', dataIndex: 'diag_type', width: 120 },
  { title: '根因', dataIndex: 'root_cause', ellipsis: true },
  { title: '置信度', dataIndex: 'confidence', width: 90 },
  { title: '状态', dataIndex: 'diag_status', width: 90 },
]

// 来源 id 转中文标签，未知来源回退显示原始 id。
function sourceLabel(source: string | null | undefined): string {
  if (!source) return '-'
  return REALTIME_SOURCE_LABELS[source] ?? source
}

// 详情抽屉
const drawerOpen = ref(false)
const detail = ref<DiagLogItem | null>(null)
const detailLoading = ref(false)

onMounted(() => {
  load()
  startTimer()
})

onBeforeUnmount(() => stopTimer())

async function load() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await getRealtimeAlarms(
      (page.value - 1) * PAGE_SIZE,
      PAGE_SIZE,
    )
    items.value = res.items
    total.value = res.total
    lastUpdated.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError
        ? `加载失败（${e.status}）：${e.message}`
        : '加载异常，请稍后重试'
  } finally {
    loading.value = false
  }
}

function startTimer() {
  stopTimer()
  timer = setInterval(() => {
    if (autoRefresh.value && page.value === 1) load()
  }, REFRESH_INTERVAL)
}

function stopTimer() {
  if (timer !== null) {
    clearInterval(timer)
    timer = null
  }
}

function onAutoRefreshChange(enabled: boolean) {
  autoRefresh.value = enabled
  if (enabled) startTimer()
  else stopTimer()
}

function onPageChange(p: number) {
  page.value = p
  load()
}

function onTableChange(pag: { current?: number }) {
  onPageChange(pag.current ?? 1)
}

async function openDetail(record: DiagLogItem) {
  drawerOpen.value = true
  detailLoading.value = true
  detail.value = null
  try {
    detail.value = await getRealtimeDetail(record.id)
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError ? `详情加载失败：${e.message}` : '详情加载失败'
  } finally {
    detailLoading.value = false
  }
}

function fmtConf(v: number | null | undefined): string {
  return v === null || v === undefined ? '-' : Number(v).toFixed(2)
}
</script>

<template>
  <a-card>
    <template #title>
      <a-space>
        <span>Dimple 实时监控</span>
        <a-tag color="processing">合规预警 / 自成交 / 违规委托</a-tag>
      </a-space>
    </template>
    <template #extra>
      <a-space>
        <span class="meta">自动刷新</span>
        <a-switch
          :checked="autoRefresh"
          checked-children="开"
          un-checked-children="关"
          @change="onAutoRefreshChange"
        />
        <span class="meta">最后更新：{{ lastUpdated || '--' }}</span>
        <a-button size="small" :loading="loading" @click="load">
          立即刷新
        </a-button>
      </a-space>
    </template>

    <a-alert
      v-if="errorMsg"
      type="error"
      show-icon
      :message="errorMsg"
      class="block"
    />

    <a-table
      :columns="columns"
      :data-source="items"
      :loading="loading"
      row-key="id"
      :pagination="{
        current: page,
        pageSize: PAGE_SIZE,
        total,
        showSizeChanger: false,
      }"
      @change="onTableChange"
    >
      <template #bodyCell="{ column, record }">
        <a v-if="column.dataIndex === 'id'" @click="openDetail(record)">
          {{ record.id }}
        </a>
        <span v-else-if="column.dataIndex === 'source'">
          {{ sourceLabel(record.source) }}
        </span>
        <a-tag
          v-else-if="column.dataIndex === 'diag_class'"
          :color="classColor[record.diag_class ?? ''] ?? 'default'"
        >
          {{ labelNull(record.diag_class) }}
        </a-tag>
        <span v-else-if="column.dataIndex === 'diag_type'">
          {{ labelNull(record.diag_type) }}
        </span>
        <span v-else-if="column.dataIndex === 'confidence'">
          {{ fmtConf(record.confidence) }}
        </span>
        <a-tag
          v-else-if="column.dataIndex === 'diag_status'"
          :color="record.diag_status === 'success' ? 'green' : 'red'"
        >
          {{ record.diag_status }}
        </a-tag>
      </template>
    </a-table>

    <a-empty
      v-if="!loading && total === 0"
      description="暂无实时预警（Dimple 产生合规预警、自成交或违规委托后将自动出现在这里）"
    />
  </a-card>

  <a-drawer v-model:open="drawerOpen" title="实时预警详情" width="560">
    <a-spin :spinning="detailLoading">
      <a-descriptions v-if="detail" :column="1" bordered size="small">
        <a-descriptions-item label="ID">{{ detail.id }}</a-descriptions-item>
        <a-descriptions-item label="批次号">{{ detail.batch_id }}</a-descriptions-item>
        <a-descriptions-item label="来源 / 日期">
          {{ detail.source }} / {{ detail.business_date }}
        </a-descriptions-item>
        <a-descriptions-item label="预警文本">{{ detail.error_text }}</a-descriptions-item>
        <a-descriptions-item label="分类 / 类型">
          {{ detail.diag_class }} / {{ detail.diag_type }}
        </a-descriptions-item>
        <a-descriptions-item label="根因">{{ detail.root_cause }}</a-descriptions-item>
        <a-descriptions-item label="置信度">
          {{ fmtConf(detail.confidence) }}
        </a-descriptions-item>
        <a-descriptions-item label="取证步数">
          {{ detail.evidence_count }}
        </a-descriptions-item>
        <a-descriptions-item label="诊断时间">{{ detail.created_at }}</a-descriptions-item>
      </a-descriptions>
    </a-spin>
  </a-drawer>
</template>

<style scoped>
.block {
  margin-bottom: 16px;
}

.meta {
  color: #666;
  font-size: 13px;
}
</style>
