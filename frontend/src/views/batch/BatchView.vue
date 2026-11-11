<script setup lang="ts">
import { computed, ref } from 'vue'

import { batchReplay } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import ResultCard from '@/components/ResultCard.vue'
import { SOURCES } from '@/constants/sources'
import type { BatchItem, DiagnosisResult } from '@/types/contract'

const source = ref(SOURCES[0].id)
const date = ref('')
const loading = ref(false)
const errorMsg = ref('')
const truncated = ref(false)
const items = ref<BatchItem[]>([])

const keyword = ref('')
const classFilter = ref<string>('')

interface Row {
  key: number
  text: string
  cls: string
  type: string
  confidence: number | string
  degraded: boolean
  item: BatchItem
}

const rows = computed<Row[]>(() => {
  const out: Row[] = []
  items.value.forEach((item, i) => {
    const res = item.result as DiagnosisResult | null
    out.push({
      key: i,
      text: item.record.text,
      cls: res?.rule_res?.class ?? '-',
      type: res?.rule_res?.type?.title ?? (item.error ? '诊断异常' : '未识别'),
      confidence: res?.answer?.confidence ?? '-',
      degraded:
        (res?.rule_res?.missing_params?.length ?? 0) > 0 ||
        (res?.rule_res?.sql_errors?.length ?? 0) > 0,
      item,
    })
  })
  return out
})

const classOptions = computed(() => [
  ...new Set(rows.value.map((r) => r.cls)),
])

const filteredRows = computed(() =>
  rows.value.filter((r) => {
    const matchClass = !classFilter.value || r.cls === classFilter.value
    const matchKeyword =
      !keyword.value || r.text.includes(keyword.value) || r.type.includes(keyword.value)
    return matchClass && matchKeyword
  }),
)

const columns = [
  { title: '报错文本', dataIndex: 'text', key: 'text', ellipsis: true },
  { title: '分类', dataIndex: 'cls', key: 'cls' },
  { title: '问题类型', dataIndex: 'type', key: 'type' },
  { title: '置信度', dataIndex: 'confidence', key: 'confidence', width: 90 },
  { title: '降级', dataIndex: 'degraded', key: 'degraded', width: 80 },
]

const drawerVisible = ref(false)
const current = ref<BatchItem | null>(null)

function openDetail(row: Row) {
  current.value = row.item
  drawerVisible.value = true
}

async function run() {
  loading.value = true
  errorMsg.value = ''
  items.value = []
  try {
    const res = await batchReplay(source.value, date.value)
    items.value = res.results
    truncated.value = res.truncated
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError
        ? `请求失败（${e.status}）：${e.message}`
        : '请求异常，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <a-card title="批量回放">
    <a-row :gutter="16" align="middle">
      <a-col :span="8">
        <a-select v-model:value="source" style="width: 100%">
          <a-select-option v-for="s in SOURCES" :key="s.id" :value="s.id">
            {{ s.label }}（{{ s.id }}）
          </a-select-option>
        </a-select>
      </a-col>
      <a-col :span="6">
        <a-input v-model:value="date" placeholder="业务日期 YYYYMMDD" />
      </a-col>
      <a-col :span="4">
        <a-button type="primary" :loading="loading" @click="run">
          开始回放
        </a-button>
      </a-col>
    </a-row>

    <a-alert
      v-if="truncated"
      class="alert"
      type="warning"
      show-icon
      message="记录超过 200 条上限，结果已截断，请缩小日期范围或分批查看"
    />
    <a-alert
      v-if="errorMsg"
      class="alert"
      type="error"
      show-icon
      :message="errorMsg"
    />

    <div v-if="rows.length" class="toolbar">
      <a-input-search
        v-model:value="keyword"
        placeholder="搜索文本/类型"
        style="max-width: 280px"
      />
      <a-select
        v-model:value="classFilter"
        placeholder="按分类筛选"
        allow-clear
        style="width: 160px"
      >
        <a-select-option
          v-for="c in classOptions"
          :key="c"
          :value="c"
        >
          {{ c }}
        </a-select-option>
      </a-select>
    </div>

    <a-table
      :columns="columns"
      :data-source="filteredRows"
      :loading="loading"
      :pagination="{ pageSize: 10 }"
      @row-click="openDetail"
      :custom-row="(record: Row) => ({ onClick: () => openDetail(record) })"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'degraded'">
          <a-tag :color="record.degraded ? 'orange' : 'green'">
            {{ record.degraded ? '是' : '否' }}
          </a-tag>
        </template>
      </template>
    </a-table>
  </a-card>

  <a-drawer
    v-model:open="drawerVisible"
    title="诊断详情"
    width="640"
    placement="right"
  >
    <a-result
      v-if="current?.error"
      status="error"
      :title="current.error"
    />
    <ResultCard
      v-else-if="current?.result"
      :result="current.result as DiagnosisResult"
    />
  </a-drawer>
</template>

<style scoped>
.alert {
  margin-top: 16px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin: 16px 0;
}
</style>
