<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { ReloadOutlined, ThunderboltOutlined } from '@ant-design/icons-vue'

import { getRealtimeAlarms, getRealtimeDetail } from '@/api/realtime'
import { getRules } from '@/api/meta'
import { ApiError } from '@/api/client'
import PageHeader from '@/components/PageHeader.vue'
import ResponsiveDrawer from '@/components/ResponsiveDrawer.vue'
import ResultCard from '@/components/ResultCard.vue'
import StateBlock from '@/components/StateBlock.vue'
import StatusTag from '@/components/StatusTag.vue'
import { REALTIME_SOURCE_LABELS } from '@/constants/sources'
import { formatBusinessDate, formatConfidence, formatDateTime, parseDiagnosisResult } from '@/utils/diagnosis'
import { ruleTypeLabel } from '@/utils/label'
import type { DiagLogItem, RuleItem } from '@/types/contract'
import { useRealtimeLlm } from './useRealtimeLlm'

const PAGE_SIZE = 10
const REFRESH_INTERVAL = 10000
const viewMode = ref<'anomaly' | 'all'>('anomaly')
const source = ref<string>()
const diagClass = ref<string>()
const items = ref<DiagLogItem[]>([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)
const backgroundLoading = ref(false)
const errorMsg = ref('')
const lastUpdated = ref('')
const autoRefresh = ref(true)
let timer: ReturnType<typeof setInterval> | null = null
let listGeneration = 0
let detailGeneration = 0

const rules = ref<RuleItem[]>([])
const sourceOptions = Object.entries(REALTIME_SOURCE_LABELS).map(([value, label]) => ({ value, label }))
const classOptions = [
  { value: 'biz', label: '业务报错' },
  { value: 'noise', label: '噪音' },
  { value: 'ora', label: 'DBA 技术错误' },
  { value: 'other', label: '其他/未识别' },
]
const hasFilters = computed(() => Boolean(source.value || diagClass.value))
const emptyDescription = computed(() => {
  if (hasFilters.value) return '没有符合当前来源和分类的记录，请调整筛选'
  return viewMode.value === 'anomaly'
    ? '暂无真实异常。Dimple 或 iQuant 产生需要关注的报错或告警后会显示在这里。'
    : '当前没有实时落库记录'
})

const columns = [
  { title: 'ID', dataIndex: 'id', width: 80, responsive: ['md'] },
  { title: '业务日期', dataIndex: 'business_date', width: 120, responsive: ['sm'] },
  { title: '来源', dataIndex: 'source', width: 140 },
  { title: '预警内容', dataIndex: 'error_text', width: 320, ellipsis: true },
  { title: '分类', dataIndex: 'diag_class', width: 130 },
  { title: '诊断类型', dataIndex: 'diag_type', width: 150 },
  { title: '根因摘要', dataIndex: 'root_cause', width: 280, ellipsis: true },
  { title: '置信度', dataIndex: 'confidence', width: 100 },
  { title: '诊断状态', dataIndex: 'diag_status', width: 120 },
  { title: '操作', key: 'action', width: 110, fixed: 'right' as const },
]

const drawerOpen = ref(false)
const detail = ref<DiagLogItem | null>(null)
const detailLoading = ref(false)
const detailError = ref('')
const activeDetailId = ref<number | null>(null)
const llmSection = ref<HTMLElement | null>(null)
const parsed = computed(() => parseDiagnosisResult(detail.value?.result_json))
const parsedResult = computed(() => parsed.value.result)

const {
  llmEnabled,
  llmLoading,
  llmAnswer,
  llmError,
  llmNotice,
  onLlmToggle,
  resetLlm,
} = useRealtimeLlm(detail)

onMounted(() => {
  void loadRules()
  void load(false)
  startTimer()
})

async function loadRules() {
  try {
    rules.value = (await getRules()).rules
  } catch {
    // 类型标题不可用时回退为 id，不阻塞实时异常主流程。
    rules.value = []
  }
}

onBeforeUnmount(() => {
  listGeneration += 1
  detailGeneration += 1
  stopTimer()
  resetLlm()
})

async function load(background = false) {
  const requestGeneration = ++listGeneration
  loading.value = true
  backgroundLoading.value = background
  if (!background) errorMsg.value = ''
  try {
    const response = await getRealtimeAlarms(
      (page.value - 1) * PAGE_SIZE,
      PAGE_SIZE,
      viewMode.value === 'anomaly',
      { source: source.value, diag_class: diagClass.value },
    )
    if (requestGeneration !== listGeneration) return
    items.value = response.items
    total.value = response.total
    errorMsg.value = ''
    lastUpdated.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  } catch (error) {
    if (requestGeneration !== listGeneration) return
    errorMsg.value = error instanceof ApiError
      ? `加载失败（${error.status}）：${error.message}`
      : '加载异常，请稍后重试'
  } finally {
    if (requestGeneration === listGeneration) {
      loading.value = false
      backgroundLoading.value = false
    }
  }
}

function startTimer() {
  stopTimer()
  timer = setInterval(() => {
    if (autoRefresh.value && page.value === 1 && !loading.value) void load(true)
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

function onViewModeChange() {
  page.value = 1
  void load(false)
}

function onFilterChange() {
  page.value = 1
  void load(false)
}

function resetFilters() {
  source.value = undefined
  diagClass.value = undefined
  page.value = 1
  void load(false)
}

function onTableChange(pagination: { current?: number }) {
  const nextPage = pagination.current ?? 1
  if (nextPage === page.value) return
  page.value = nextPage
  void load(false)
}

function onMobilePageChange(nextPage: number) {
  onTableChange({ current: nextPage })
}

function sourceLabel(value?: string | null) {
  if (!value) return '—'
  return REALTIME_SOURCE_LABELS[value] ?? value
}

async function loadDetail(id: number) {
  const requestGeneration = ++detailGeneration
  activeDetailId.value = id
  detailLoading.value = true
  detailError.value = ''
  detail.value = null
  resetLlm()
  try {
    const response = await getRealtimeDetail(id)
    if (requestGeneration !== detailGeneration) return
    detail.value = response
  } catch (error) {
    if (requestGeneration !== detailGeneration) return
    detailError.value = error instanceof ApiError ? `详情加载失败：${error.message}` : '详情加载失败，请重试'
  } finally {
    if (requestGeneration === detailGeneration) detailLoading.value = false
  }
}

function openDetail(record: DiagLogItem) {
  drawerOpen.value = true
  void loadDetail(record.id)
}

function closeDetail() {
  drawerOpen.value = false
  detailGeneration += 1
  detailLoading.value = false
  detail.value = null
  resetLlm()
}

function retryDetail() {
  if (activeDetailId.value !== null) void loadDetail(activeDetailId.value)
}

function scrollToLlm() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  llmSection.value?.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' })
}
</script>

<template>
  <div class="page-shell">
    <PageHeader
      title="实时异常"
      description="查看 Dimple 与 iQuant 采集并落库的诊断记录。页面只负责刷新已保存的数据，实际采集频率由后端调度配置决定。"
    >
      <template #extra>
        <a-button :loading="loading && !backgroundLoading" @click="load(false)"><ReloadOutlined /> 立即刷新</a-button>
      </template>
    </PageHeader>

    <section class="realtime-controls surface-card" aria-label="实时记录筛选">
      <div class="mode-row">
        <a-radio-group v-model:value="viewMode" option-type="button" button-style="solid" @change="onViewModeChange">
          <a-radio-button value="anomaly">真实异常</a-radio-button>
          <a-radio-button value="all">全部记录</a-radio-button>
        </a-radio-group>
        <span class="mode-description">
          {{ viewMode === 'anomaly' ? '排除正常行情、持仓、资金等业务数据' : '包含业务数据，便于核对异常过滤结果' }}
        </span>
      </div>
      <div class="filter-row">
        <a-select
          v-model:value="source"
          allow-clear
          show-search
          option-filter-prop="label"
          :options="sourceOptions"
          placeholder="全部实时来源"
          class="source-filter"
          @change="onFilterChange"
        />
        <a-select
          v-model:value="diagClass"
          allow-clear
          :options="classOptions"
          placeholder="全部分类"
          class="class-filter"
          @change="onFilterChange"
        />
        <a-button v-if="hasFilters" type="text" @click="resetFilters">重置筛选</a-button>
        <div class="refresh-control">
          <a-switch :checked="autoRefresh" size="small" @change="onAutoRefreshChange" />
          <span>10 秒自动刷新</span>
          <span class="update-time">{{ loading ? '正在更新' : lastUpdated ? `更新于 ${lastUpdated}` : '尚未更新' }}</span>
        </div>
      </div>
      <p v-if="page > 1" class="paused-note">当前不在第一页，自动刷新已暂停；返回第一页后恢复。</p>
    </section>

    <a-alert
      v-if="errorMsg && items.length"
      type="warning"
      show-icon
      :message="errorMsg"
      description="本次刷新失败，表格保留上次成功数据，可能不是最新状态。"
      class="list-alert"
    />
    <a-alert
      v-else-if="loading && !backgroundLoading && items.length"
      type="info"
      show-icon
      message="正在更新列表，当前保留上次成功数据"
      class="list-alert"
    />

    <a-card class="realtime-table-card">
      <template #title>{{ viewMode === 'anomaly' ? '异常记录' : '全部落库记录' }}</template>
      <template #extra><span class="record-count">共 {{ total }} 条</span></template>
      <StateBlock v-if="loading && !items.length" loading :loading-rows="7" />
      <StateBlock v-else-if="errorMsg && !items.length" :error="errorMsg" @retry="load(false)" />
      <a-empty v-else-if="!items.length" :description="emptyDescription" />
      <div v-else class="responsive-records">
        <div class="desktop-records">
          <a-table
            :columns="columns"
            :data-source="items"
            row-key="id"
            :scroll="{ x: 1520 }"
            :pagination="{ current: page, pageSize: PAGE_SIZE, total, showSizeChanger: false }"
            @change="onTableChange"
          >
            <template #bodyCell="{ column, record }">
              <span v-if="column.dataIndex === 'business_date'">{{ formatBusinessDate(record.business_date) }}</span>
              <span v-else-if="column.dataIndex === 'source'">{{ sourceLabel(record.source) }}</span>
              <span v-else-if="column.dataIndex === 'error_text'" class="cell-text" :title="record.error_text">{{ record.error_text || '—' }}</span>
              <StatusTag v-else-if="column.dataIndex === 'diag_class'" :status="record.diag_class" />
              <span v-else-if="column.dataIndex === 'diag_type'">{{ ruleTypeLabel(record.diag_type, rules) }}</span>
              <span v-else-if="column.dataIndex === 'root_cause'" class="cell-text" :title="record.root_cause">{{ record.root_cause || '—' }}</span>
              <span v-else-if="column.dataIndex === 'confidence'" class="numeric-cell">{{ formatConfidence(record.confidence) }}</span>
              <StatusTag
                v-else-if="column.dataIndex === 'diag_status'"
                :status="record.diag_status"
                :label="record.diag_status === 'success' ? '诊断完成' : '诊断失败'"
                :tone="record.diag_status === 'success' ? 'success' : 'error'"
              />
              <a-button v-else-if="column.key === 'action'" type="link" size="small" @click="openDetail(record)">查看详情</a-button>
            </template>
          </a-table>
        </div>
        <div class="mobile-records">
          <article v-for="record in items" :key="record.id" class="mobile-record-card">
            <button type="button" class="mobile-record-main" @click="openDetail(record)">
              <span class="mobile-record-top">
                <span class="mobile-record-source">{{ sourceLabel(record.source) }} · #{{ record.id }}</span>
                <StatusTag
                  :status="record.diag_status"
                  :label="record.diag_status === 'success' ? '诊断完成' : '诊断失败'"
                  :tone="record.diag_status === 'success' ? 'success' : 'error'"
                />
              </span>
              <strong>{{ ruleTypeLabel(record.diag_type, rules) }}</strong>
              <span class="mobile-record-description">{{ record.root_cause || record.error_text || '暂无根因摘要' }}</span>
              <span class="mobile-record-meta">{{ formatBusinessDate(record.business_date) }} · 置信度 {{ formatConfidence(record.confidence) }}</span>
              <span class="mobile-record-action">查看完整诊断 <span aria-hidden="true">→</span></span>
            </button>
          </article>
          <a-pagination
            v-if="total > PAGE_SIZE"
            simple
            size="small"
            :current="page"
            :page-size="PAGE_SIZE"
            :total="total"
            :show-size-changer="false"
            @change="onMobilePageChange"
          />
        </div>
      </div>
    </a-card>

    <ResponsiveDrawer v-model:open="drawerOpen" title="实时诊断详情" :width="820" @close="closeDetail">
      <StateBlock v-if="detailLoading" loading :loading-rows="8" />
      <StateBlock
        v-else-if="detailError"
        :error="detailError"
        error-title="无法打开诊断详情"
        @retry="retryDetail"
      />
      <template v-else-if="detail">
        <section class="detail-summary">
          <div class="detail-title-row">
            <div>
              <span class="detail-source">{{ sourceLabel(detail.source) }} · #{{ detail.id }}</span>
              <h2>{{ ruleTypeLabel(detail.diag_type, rules) }}</h2>
            </div>
            <StatusTag
              :status="detail.diag_status"
              :label="detail.diag_status === 'success' ? '诊断完成' : '诊断失败'"
              :tone="detail.diag_status === 'success' ? 'success' : 'error'"
            />
          </div>
          <p>{{ detail.root_cause || '暂无根因摘要，请查看下方原始报错。' }}</p>
          <dl class="detail-meta">
            <div><dt>业务日期</dt><dd>{{ formatBusinessDate(detail.business_date) }}</dd></div>
            <div><dt>诊断时间</dt><dd>{{ formatDateTime(detail.created_at) }}</dd></div>
            <div><dt>诊断路径</dt><dd>{{ detail.diag_path || '—' }}</dd></div>
            <div><dt>历史升级</dt><dd>{{ detail.escalated ? '实际升级过' : '未升级' }}</dd></div>
          </dl>
          <a-button type="text" size="small" @click="scrollToLlm"><ThunderboltOutlined /> 前往按需大模型预览</a-button>
        </section>

        <a-alert
          v-if="parsed.error"
          type="warning"
          show-icon
          :message="parsed.error"
          description="已保存的来源、日期、根因摘要仍可参考；完整动作与证据暂不可展示。"
          class="snapshot-alert"
        />
        <ResultCard v-if="parsedResult" :result="parsedResult" />
        <section v-else class="fallback-detail">
          <h3>已保存的摘要</h3>
          <dl class="report-fallback">
            <div><dt>根因摘要</dt><dd>{{ detail.root_cause || '—' }}</dd></div>
            <div><dt>置信度</dt><dd>{{ formatConfidence(detail.confidence) }}</dd></div>
            <div><dt>原始报错</dt><dd>{{ detail.error_text || '—' }}</dd></div>
          </dl>
        </section>

        <section ref="llmSection" class="llm-section" aria-live="polite">
          <div class="llm-heading">
            <div>
              <span class="section-eyebrow">按需分析</span>
              <h3>大模型升级预览</h3>
            </div>
            <a-button
              v-if="!llmAnswer"
              type="primary"
              :loading="llmLoading"
              @click="onLlmToggle(true)"
            >
              <ThunderboltOutlined /> {{ llmEnabled ? '正在分析' : '使用大模型分析' }}
            </a-button>
            <a-button v-else @click="onLlmToggle(false)">关闭预览</a-button>
          </div>
          <p class="llm-description">仅在你点击后调用，可能耗时较长并消耗模型额度。结果只用于当前预览，不新增事件，也不覆盖历史诊断。</p>
          <a-alert v-if="llmNotice" type="info" show-icon :message="llmNotice" class="llm-alert" />
          <a-alert v-if="llmError" type="error" show-icon :message="llmError" class="llm-alert" />
          <a-skeleton v-if="llmLoading" active :paragraph="{ rows: 3 }" />
          <div v-if="llmAnswer" class="llm-result">
            <div class="llm-result-head">
              <h4>大模型判断</h4>
              <a-tag color="blue">置信度 {{ formatConfidence(llmAnswer.confidence) }}</a-tag>
            </div>
            <p class="llm-root">{{ llmAnswer.root || '大模型未返回明确根因' }}</p>
            <ol v-if="llmAnswer.actions.length" class="llm-actions">
              <li v-for="(action, index) in llmAnswer.actions" :key="index">{{ action }}</li>
            </ol>
            <p v-if="llmAnswer.evidence_note" class="llm-note">依据：{{ llmAnswer.evidence_note }}</p>
            <a-button size="small" :loading="llmLoading" @click="onLlmToggle(true)">重新生成预览</a-button>
          </div>
        </section>
      </template>
    </ResponsiveDrawer>
  </div>
</template>

<style scoped>
.realtime-controls {
  margin-bottom: 20px;
  padding: 16px;
}

.mode-row,
.filter-row,
.refresh-control {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-row {
  margin-top: 14px;
}

.mode-description,
.paused-note {
  color: var(--text-muted);
  font-size: 12px;
}

.paused-note {
  margin: 12px 0 0;
  color: var(--warning);
}

.source-filter {
  width: 230px;
}

.class-filter {
  width: 160px;
}

.refresh-control {
  margin-left: auto;
  color: var(--text-secondary);
  font-size: 12px;
}

.update-time {
  padding-left: 12px;
  color: var(--text-muted);
  border-left: 1px solid var(--border);
}

.list-alert {
  margin-bottom: 16px;
}

.record-count {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 400;
}

.mobile-records {
  display: none;
}

.detail-summary {
  margin-bottom: 20px;
  padding: 18px;
  background: var(--surface-subtle);
  border: 1px solid var(--border-soft);
  border-radius: 12px;
  scroll-margin-top: 16px;
}

.detail-title-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
}

.detail-source {
  color: var(--text-muted);
  font-size: 12px;
}

.detail-title-row h2 {
  margin: 5px 0 10px;
  font-size: 20px;
}

.detail-summary > p {
  color: var(--text-secondary);
  line-height: 1.65;
}

.detail-meta {
  display: grid;
  margin: 0 0 8px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.detail-meta dt,
.report-fallback dt {
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 11px;
}

.detail-meta dd,
.report-fallback dd {
  margin: 0;
  overflow-wrap: anywhere;
}

.snapshot-alert {
  margin-bottom: 16px;
}

.fallback-detail {
  padding: 20px 0;
  border-bottom: 1px solid var(--border-soft);
}

.report-fallback {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.report-fallback > div:last-child {
  grid-column: 1 / -1;
}

.llm-section {
  margin-top: 24px;
  padding: 20px;
  background: #f7faff;
  border: 1px solid #dce8f7;
  border-radius: 12px;
  scroll-margin-top: 16px;
}

.llm-heading {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
}

.section-eyebrow {
  color: var(--text-muted);
  font-size: 11px;
  letter-spacing: 0.06em;
}

.llm-heading h3 {
  margin: 5px 0 0;
  font-size: 17px;
}

.llm-description {
  margin: 14px 0 16px;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.65;
}

.llm-alert {
  margin-bottom: 12px;
}

.llm-result {
  padding: 16px;
  background: #fff;
  border: 1px solid var(--border-soft);
  border-radius: 10px;
}

.llm-result-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.llm-result h4 {
  margin: 0;
}

.llm-root {
  margin: 14px 0;
  font-size: 16px;
  line-height: 1.65;
}

.llm-actions {
  padding-left: 22px;
  line-height: 1.8;
}

.llm-note {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.6;
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

  .mobile-record-main {
    display: flex;
    width: 100%;
    padding: 15px;
    flex-direction: column;
    gap: 9px;
    color: var(--text-primary);
    text-align: left;
    background: #fff;
    border: 0;
    cursor: pointer;
  }

  .mobile-record-main:hover {
    background: #fafcff;
  }

  .mobile-record-top {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
  }

  .mobile-record-source,
  .mobile-record-meta {
    color: var(--text-muted);
    font-size: 11px;
  }

  .mobile-record-description {
    display: -webkit-box;
    overflow: hidden;
    color: var(--text-secondary);
    font-size: 13px;
    line-height: 1.65;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }

  .mobile-record-action {
    color: var(--brand-hover);
    font-size: 12px;
    font-weight: 500;
  }

  .mobile-records :deep(.ant-pagination) {
    justify-content: center;
    margin-top: 4px;
  }

  .refresh-control {
    width: 100%;
    margin-left: 0;
  }

  .update-time {
    margin-left: auto;
  }
}

@media (max-width: 640px) {
  .source-filter,
  .class-filter {
    width: 100%;
  }

  .detail-meta,
  .report-fallback {
    grid-template-columns: minmax(0, 1fr);
  }

  .report-fallback > div:last-child {
    grid-column: auto;
  }

  .llm-section {
    padding: 16px;
  }

  .llm-heading {
    flex-direction: column;
  }
}
</style>
