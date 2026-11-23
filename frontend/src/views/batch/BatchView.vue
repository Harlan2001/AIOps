<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ClearOutlined, PlayCircleOutlined } from '@ant-design/icons-vue'

import { batchReplay } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import PageHeader from '@/components/PageHeader.vue'
import ResponsiveDrawer from '@/components/ResponsiveDrawer.vue'
import ResultCard from '@/components/ResultCard.vue'
import StateBlock from '@/components/StateBlock.vue'
import StatusTag from '@/components/StatusTag.vue'
import { DIAGNOSE_SOURCES } from '@/constants/sources'
import { classifyBatchItem, type BatchStatus } from '@/utils/batchStatus'
import { formatConfidence } from '@/utils/diagnosis'
import { diagnosisClassLabel } from '@/utils/label'
import type { BatchItem, DiagnosisResult } from '@/types/contract'

const source = ref(DIAGNOSE_SOURCES[0].id)
const date = ref('')
const dateError = ref('')
const loading = ref(false)
const errorMsg = ref('')
const truncated = ref(false)
const maxBatch = ref(200)
const items = ref<BatchItem[]>([])
const hasRun = ref(false)
let generation = 0

const keyword = ref('')
const classFilter = ref('')
const statusFilter = ref<BatchStatus | ''>('')
const mobilePage = ref(1)

interface Row {
  key: number
  text: string
  cls: string
  type: string
  confidence?: number | null
  status: BatchStatus
  item: BatchItem
}

const rows = computed<Row[]>(() => items.value.map((item, index) => {
  const result = item.result as DiagnosisResult | null | undefined
  return {
    key: index,
    text: item.record.text,
    cls: result?.rule_res?.class ?? '',
    type: result?.rule_res?.type?.title ?? (item.error ? '诊断失败' : '未识别'),
    confidence: result?.answer?.confidence,
    status: classifyBatchItem(item),
    item,
  }
}))

const counts = computed(() => ({
  normal: rows.value.filter((row) => row.status === 'normal').length,
  degraded: rows.value.filter((row) => row.status === 'degraded').length,
  error: rows.value.filter((row) => row.status === 'error').length,
}))

const classOptions = computed(() => [...new Set(rows.value.map((row) => row.cls).filter(Boolean))])
const filteredRows = computed(() => {
  const query = keyword.value.trim().toLocaleLowerCase()
  return rows.value.filter((row) => {
    const matchClass = !classFilter.value || row.cls === classFilter.value
    const matchStatus = !statusFilter.value || row.status === statusFilter.value
    const matchKeyword = !query || row.text.toLocaleLowerCase().includes(query) || row.type.toLocaleLowerCase().includes(query)
    return matchClass && matchStatus && matchKeyword
  })
})

const mobileRows = computed(() => filteredRows.value.slice((mobilePage.value - 1) * 10, mobilePage.value * 10))
watch([keyword, classFilter, statusFilter], () => {
  mobilePage.value = 1
})

function onMobilePageChange(nextPage: number) {
  mobilePage.value = nextPage
}

const columns = [
  { title: '报错文本', dataIndex: 'text', key: 'text', width: 360, ellipsis: true },
  { title: '分类', dataIndex: 'cls', key: 'cls', width: 130 },
  { title: '问题类型', dataIndex: 'type', key: 'type', width: 180 },
  { title: '置信度', dataIndex: 'confidence', key: 'confidence', width: 100 },
  { title: '结果状态', dataIndex: 'status', key: 'status', width: 120 },
  { title: '操作', key: 'action', width: 110, fixed: 'right' as const },
]

const drawerVisible = ref(false)
const current = ref<BatchItem | null>(null)

function openDetail(row: Row) {
  current.value = row.item
  drawerVisible.value = true
}

function toggleStatus(status: BatchStatus) {
  statusFilter.value = statusFilter.value === status ? '' : status
}

async function run() {
  dateError.value = date.value ? '' : '请选择要回放的业务日期'
  if (dateError.value) return

  const requestGeneration = ++generation
  hasRun.value = true
  loading.value = true
  errorMsg.value = ''
  try {
    const response = await batchReplay(source.value, date.value)
    if (requestGeneration !== generation) return
    items.value = response.results
    truncated.value = response.truncated
    maxBatch.value = response.max_batch
    keyword.value = ''
    classFilter.value = ''
    statusFilter.value = ''
    mobilePage.value = 1
  } catch (error) {
    if (requestGeneration !== generation) return
    errorMsg.value = error instanceof ApiError
      ? error.status === 0
        ? `无法连接诊断服务：${error.message}`
        : `批量回放未完成（${error.status}）：${error.message}`
      : '批量回放异常，请稍后重试'
  } finally {
    if (requestGeneration === generation) loading.value = false
  }
}

function clearResults() {
  generation += 1
  items.value = []
  hasRun.value = false
  truncated.value = false
  loading.value = false
  errorMsg.value = ''
  keyword.value = ''
  classFilter.value = ''
  statusFilter.value = ''
}
</script>

<template>
  <div class="page-shell">
    <PageHeader
      title="批量回放"
      description="按来源和业务日期重新执行规则诊断，集中比较正常、降级与失败结果，并逐条查看完整诊断报告。"
    >
      <template #extra>
        <a-button v-if="rows.length" @click="clearResults"><ClearOutlined /> 清空结果</a-button>
      </template>
    </PageHeader>

    <a-card class="replay-form-card">
      <a-form layout="vertical" @submit.prevent="run">
        <div class="replay-form">
          <a-form-item label="错误来源" required>
            <a-select v-model:value="source" :options="DIAGNOSE_SOURCES.map((item) => ({ value: item.id, label: `${item.label}（${item.id}）` }))" />
          </a-form-item>
          <a-form-item label="业务日期" required :validate-status="dateError ? 'error' : ''" :help="dateError">
            <a-date-picker
              v-model:value="date"
              value-format="YYYYMMDD"
              format="YYYY-MM-DD"
              placeholder="选择回放日期"
              class="full-width"
              @change="dateError = ''"
            />
          </a-form-item>
          <a-form-item label=" ">
            <a-button type="primary" html-type="submit" :loading="loading" block>
              <PlayCircleOutlined /> {{ rows.length ? '重新回放' : '开始回放' }}
            </a-button>
          </a-form-item>
        </div>
      </a-form>
      <p class="replay-hint">单次同步请求可能耗时数分钟，请保持页面打开。页面不会显示虚构的进度百分比；服务未提供后台取消能力。</p>
    </a-card>

    <a-alert
      v-if="loading && rows.length"
      type="info"
      show-icon
      message="新批次正在执行，下方暂时保留上次结果"
      class="result-alert"
    />
    <a-alert
      v-if="errorMsg && rows.length"
      type="error"
      show-icon
      :message="errorMsg"
      class="result-alert"
    />
    <a-alert
      v-if="truncated && rows.length"
      type="warning"
      show-icon
      :message="`记录超过 ${maxBatch} 条上限，结果已截断。请调整日期范围或分批核对。`"
      class="result-alert"
    />

    <a-card class="results-card">
      <template #title>回放结果</template>
      <template v-if="rows.length" #extra><span class="result-total">共 {{ rows.length }} 条</span></template>

      <StateBlock v-if="loading && !rows.length" loading :loading-rows="7" />
      <StateBlock v-else-if="errorMsg && !rows.length" :error="errorMsg" @retry="run" />
      <StateBlock
        v-else-if="!rows.length"
        empty
        :empty-text="hasRun ? '本批次没有返回诊断记录' : '选择来源和日期后开始回放，结果会显示在这里'"
      />
      <template v-else>
        <div class="summary-grid" aria-label="按结果状态筛选">
          <button type="button" class="summary-item" :aria-pressed="statusFilter === 'normal'" @click="toggleStatus('normal')">
            <span><i class="dot normal" />正常</span><strong>{{ counts.normal }}</strong>
          </button>
          <button type="button" class="summary-item" :aria-pressed="statusFilter === 'degraded'" @click="toggleStatus('degraded')">
            <span><i class="dot degraded" />降级</span><strong>{{ counts.degraded }}</strong>
          </button>
          <button type="button" class="summary-item" :aria-pressed="statusFilter === 'error'" @click="toggleStatus('error')">
            <span><i class="dot error" />异常</span><strong>{{ counts.error }}</strong>
          </button>
        </div>

        <div class="result-filters">
          <a-input v-model:value="keyword" allow-clear placeholder="搜索报错文本或问题类型" class="keyword-input" />
          <a-select v-model:value="classFilter" allow-clear placeholder="全部分类" class="class-select">
            <a-select-option v-for="item in classOptions" :key="item" :value="item">{{ diagnosisClassLabel(item) }}</a-select-option>
          </a-select>
          <a-select v-model:value="statusFilter" allow-clear placeholder="全部状态" class="status-select">
            <a-select-option value="normal">正常</a-select-option>
            <a-select-option value="degraded">降级</a-select-option>
            <a-select-option value="error">异常</a-select-option>
          </a-select>
        </div>

        <div class="responsive-records" :class="{ 'is-refreshing': loading }">
          <div class="desktop-records">
            <a-table
              :columns="columns"
              :data-source="filteredRows"
              :pagination="{ pageSize: 10, hideOnSinglePage: true }"
              :scroll="{ x: 1100 }"
              :locale="{ emptyText: '没有符合当前筛选条件的结果，请调整筛选' }"
              row-key="key"
            >
              <template #bodyCell="{ column, record }">
                <span v-if="column.key === 'text'" class="cell-text" :title="record.text">{{ record.text }}</span>
                <StatusTag v-else-if="column.key === 'cls'" :status="record.cls" />
                <span v-else-if="column.key === 'confidence'" class="numeric-cell">{{ formatConfidence(record.confidence) }}</span>
                <StatusTag
                  v-else-if="column.key === 'status'"
                  :status="record.status === 'normal' ? 'normal' : record.status === 'degraded' ? 'degraded' : 'error'"
                  :label="record.status === 'normal' ? '正常' : record.status === 'degraded' ? '降级' : '异常'"
                />
                <a-button v-else-if="column.key === 'action'" type="link" size="small" @click="openDetail(record)">查看详情</a-button>
              </template>
            </a-table>
          </div>
          <div class="mobile-records">
            <a-empty v-if="!mobileRows.length" description="没有符合当前筛选条件的结果，请调整筛选" />
            <article v-for="row in mobileRows" :key="row.key" class="mobile-record-card">
              <div class="mobile-record-body">
                <div class="mobile-record-top">
                  <strong>{{ row.type }}</strong>
                  <StatusTag
                    :status="row.status === 'normal' ? 'normal' : row.status === 'degraded' ? 'degraded' : 'error'"
                    :label="row.status === 'normal' ? '正常' : row.status === 'degraded' ? '降级' : '异常'"
                  />
                </div>
                <p class="mobile-record-description">{{ row.text }}</p>
                <div class="mobile-record-meta">
                  <StatusTag :status="row.cls" />
                  <span>置信度 {{ formatConfidence(row.confidence) }}</span>
                </div>
              </div>
              <div class="mobile-record-actions">
                <a-button size="small" @click="openDetail(row)">查看完整诊断</a-button>
              </div>
            </article>
            <a-pagination
              v-if="filteredRows.length > 10"
              simple
              size="small"
              :current="mobilePage"
              :page-size="10"
              :total="filteredRows.length"
              :show-size-changer="false"
              @change="onMobilePageChange"
            />
          </div>
        </div>
      </template>
    </a-card>

    <ResponsiveDrawer v-model:open="drawerVisible" title="回放诊断详情" :width="780">
      <template v-if="current?.error">
        <a-result status="error" title="该记录诊断失败" :sub-title="current.error" />
        <a-collapse ghost>
          <a-collapse-panel key="input" header="查看原始记录">
            <pre class="raw-record">{{ current.record.text }}</pre>
          </a-collapse-panel>
        </a-collapse>
      </template>
      <ResultCard v-else-if="current?.result" :result="current.result" />
      <a-empty v-else description="该记录没有可展示的结果" />
    </ResponsiveDrawer>
  </div>
</template>

<style scoped>
.replay-form-card {
  margin-bottom: 20px;
}

.replay-form {
  display: grid;
  grid-template-columns: minmax(260px, 1fr) minmax(220px, 0.7fr) 160px;
  gap: 16px;
}

.full-width {
  width: 100%;
}

.replay-hint {
  margin: -4px 0 0;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.6;
}

.result-alert {
  margin-bottom: 16px;
}

.result-total {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 400;
}

.summary-grid {
  display: grid;
  margin-bottom: 18px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.summary-item {
  display: flex;
  padding: 14px 16px;
  align-items: center;
  justify-content: space-between;
  color: var(--text-primary);
  background: var(--surface-subtle);
  border: 1px solid var(--border-soft);
  border-radius: 10px;
  cursor: pointer;
}

.summary-item:hover,
.summary-item[aria-pressed='true'] {
  background: var(--brand-soft);
  border-color: #a9c9ed;
}

.summary-item > span {
  display: flex;
  gap: 8px;
  align-items: center;
  color: var(--text-secondary);
}

.summary-item strong {
  font-size: 22px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.dot.normal { background: var(--success); }
.dot.degraded { background: var(--warning); }
.dot.error { background: var(--danger); }

.result-filters {
  display: flex;
  margin-bottom: 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.keyword-input {
  width: min(360px, 100%);
}

.class-select {
  width: 170px;
}

.status-select {
  width: 140px;
}

.is-refreshing {
  opacity: 0.62;
}

.mobile-records {
  display: none;
}

.raw-record {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

@media (max-width: 767px) {
  .desktop-records {
    display: none;
  }

  .mobile-records {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .mobile-record-card {
    overflow: hidden;
    border: 1px solid var(--border-soft);
    border-radius: 10px;
  }

  .mobile-record-body {
    padding: 15px;
  }

  .mobile-record-top,
  .mobile-record-meta {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
  }

  .mobile-record-description {
    display: -webkit-box;
    margin: 12px 0;
    overflow: hidden;
    color: var(--text-secondary);
    font-size: 13px;
    line-height: 1.65;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
  }

  .mobile-record-meta {
    color: var(--text-muted);
    font-size: 11px;
  }

  .mobile-record-actions {
    display: flex;
    padding: 10px 15px;
    justify-content: flex-end;
    background: var(--surface-subtle);
    border-top: 1px solid var(--border-soft);
  }

  .mobile-records :deep(.ant-pagination) {
    justify-content: center;
    margin-top: 4px;
  }
}

@media (max-width: 800px) {
  .replay-form {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
  }

  .summary-grid {
    gap: 8px;
  }

  .summary-item {
    padding: 12px;
  }

  .class-select,
  .status-select {
    width: calc(50% - 6px);
  }
}

@media (max-width: 480px) {
  .summary-item {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
  }
}
</style>
