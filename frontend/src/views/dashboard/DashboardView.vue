<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import type { EChartsOption } from 'echarts'
import {
  MedicineBoxOutlined,
  ReloadOutlined,
  RightOutlined,
  TableOutlined,
} from '@ant-design/icons-vue'

import { getRules } from '@/api/meta'
import { getDiagnoses, getDiagnosisStats } from '@/api/diagnoses'
import { ApiError } from '@/api/client'
import BaseChart, { type ChartDatum } from '@/components/BaseChart.vue'
import PageHeader from '@/components/PageHeader.vue'
import StateBlock from '@/components/StateBlock.vue'
import StatusTag from '@/components/StatusTag.vue'
import { SOURCE_LABELS } from '@/constants/sources'
import { formatBusinessDate, formatPercent } from '@/utils/diagnosis'
import { diagnosisClassLabel, ruleTypeLabel } from '@/utils/label'
import type { DiagLogItem, DiagStats, RulesResponse } from '@/types/contract'

const router = useRouter()
const rules = ref<RulesResponse | null>(null)
const rulesLoading = ref(false)
const rulesError = ref('')
const stats = ref<DiagStats | null>(null)
const statsLoading = ref(false)
const statsError = ref('')
const recent = ref<DiagLogItem[]>([])
const recentLoading = ref(false)
const recentError = ref('')
const lastUpdated = ref('')
const range = ref<'all' | '7' | '30' | 'custom'>('all')
const customDates = ref<[string, string]>(['', ''])
const dateError = ref('')
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
let rulesGeneration = 0
let statsGeneration = 0
let recentGeneration = 0

const refreshing = computed(() => statsLoading.value || recentLoading.value || rulesLoading.value)

function localDate(date: Date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

const dateRange = computed(() => {
  if (range.value === 'all') return { start: undefined, end: undefined }
  if (range.value === 'custom') {
    return { start: customDates.value[0] || undefined, end: customDates.value[1] || undefined }
  }
  const end = new Date()
  const start = new Date()
  start.setDate(end.getDate() - Number(range.value) + 1)
  return { start: localDate(start), end: localDate(end) }
})

const rangeLabel = computed(() => {
  if (range.value === 'all') return '全部时间'
  if (range.value === 'custom') {
    return `${formatBusinessDate(customDates.value[0])} 至 ${formatBusinessDate(customDates.value[1])}`
  }
  return `近 ${range.value} 天`
})

const kpis = computed(() => [
  {
    key: 'total',
    label: '真实异常诊断',
    value: stats.value?.total ?? '—',
    hint: '已排除行情、持仓、资金等业务数据',
    danger: false,
  },
  {
    key: 'failed',
    label: '诊断失败',
    value: stats.value?.abnormal ?? '—',
    hint: '诊断状态为 error 的记录',
    danger: (stats.value?.abnormal ?? 0) > 0,
  },
  {
    key: 'failure-rate',
    label: '诊断失败率',
    value: stats.value ? formatPercent(stats.value.abnormal_rate) : '—',
    hint: '诊断失败数 / 真实异常诊断数',
    danger: false,
  },
  {
    key: 'escalated',
    label: '实际 LLM 升级',
    value: stats.value?.escalated ?? '—',
    hint: '仅统计真实执行过升级路径的记录',
    danger: false,
  },
])

const trendRows = computed<ChartDatum[]>(() =>
  (stats.value?.by_date ?? []).map((row) => ({ label: formatBusinessDate(row.key), value: row.count })),
)
const topTypeRows = computed<ChartDatum[]>(() =>
  (stats.value?.top_types ?? []).map((row) => ({ label: ruleTypeLabel(row.key, rules.value?.rules), value: row.count })),
)
const classTotal = computed(() => (stats.value?.by_class ?? []).reduce((sum, row) => sum + row.count, 0))

const chartBase = {
  animation: !reduceMotion,
  animationDuration: 180,
  textStyle: { color: '#566174', fontFamily: 'Segoe UI, PingFang SC, Microsoft YaHei, sans-serif' },
  tooltip: { trigger: 'axis' as const },
}

const trendChart = computed<EChartsOption>(() => ({
  ...chartBase,
  grid: { left: 48, right: 20, top: 20, bottom: 42 },
  xAxis: {
    type: 'category',
    data: trendRows.value.map((row) => row.label),
    boundaryGap: false,
    axisLine: { lineStyle: { color: '#c9d1dc' } },
    axisLabel: { hideOverlap: true, color: '#687386' },
  },
  yAxis: {
    type: 'value',
    minInterval: 1,
    axisLabel: { color: '#687386' },
    splitLine: { lineStyle: { color: '#edf0f4', type: 'solid' } },
  },
  series: [{
    name: '真实异常诊断数',
    type: 'line',
    data: trendRows.value.map((row) => row.value),
    smooth: false,
    showSymbol: trendRows.value.length <= 12,
    symbolSize: 8,
    lineStyle: { width: 2, color: '#2a78d6' },
    itemStyle: { color: '#2a78d6', borderColor: '#ffffff', borderWidth: 2 },
    areaStyle: { color: '#2a78d6', opacity: 0.08 },
  }],
}))

const topTypeChart = computed<EChartsOption>(() => ({
  ...chartBase,
  grid: { left: 116, right: 28, top: 20, bottom: 38 },
  xAxis: {
    type: 'value',
    minInterval: 1,
    axisLabel: { color: '#687386' },
    splitLine: { lineStyle: { color: '#edf0f4', type: 'solid' } },
  },
  yAxis: {
    type: 'category',
    inverse: true,
    data: topTypeRows.value.map((row) => row.label),
    axisLabel: { color: '#566174', width: 100, overflow: 'truncate' },
    axisLine: { lineStyle: { color: '#c9d1dc' } },
  },
  series: [{
    name: '诊断数',
    type: 'bar',
    data: topTypeRows.value.map((row) => row.value),
    barMaxWidth: 24,
    itemStyle: { color: '#2a78d6', borderRadius: [0, 4, 4, 0] },
  }],
}))

onMounted(() => {
  void loadRules()
  void loadData()
})

watch(range, (value) => {
  dateError.value = ''
  if (value !== 'custom') void loadData()
})

function errorText(error: unknown, fallback: string) {
  return error instanceof ApiError ? `${fallback}：${error.message}` : fallback
}

async function loadRules() {
  const requestGeneration = ++rulesGeneration
  rulesLoading.value = true
  rulesError.value = ''
  try {
    const response = await getRules()
    if (requestGeneration !== rulesGeneration) return
    rules.value = response
  } catch (error) {
    if (requestGeneration !== rulesGeneration) return
    rulesError.value = errorText(error, '规则信息加载失败')
  } finally {
    if (requestGeneration === rulesGeneration) rulesLoading.value = false
  }
}

async function loadStats() {
  const requestGeneration = ++statsGeneration
  statsLoading.value = true
  statsError.value = ''
  try {
    const response = await getDiagnosisStats(dateRange.value.start, dateRange.value.end)
    if (requestGeneration !== statsGeneration) return
    stats.value = response
    lastUpdated.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  } catch (error) {
    if (requestGeneration !== statsGeneration) return
    statsError.value = error instanceof ApiError && error.status === 503
      ? `诊断结果存储未就绪或暂不可用：${error.message}`
      : errorText(error, '统计数据加载失败')
  } finally {
    if (requestGeneration === statsGeneration) statsLoading.value = false
  }
}

async function loadRecent() {
  const requestGeneration = ++recentGeneration
  recentLoading.value = true
  recentError.value = ''
  try {
    const response = await getDiagnoses({
      anomaly_only: true,
      start_date: dateRange.value.start,
      end_date: dateRange.value.end,
      limit: 6,
    })
    if (requestGeneration !== recentGeneration) return
    recent.value = response.items
    lastUpdated.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  } catch (error) {
    if (requestGeneration !== recentGeneration) return
    recentError.value = errorText(error, '最新异常加载失败')
  } finally {
    if (requestGeneration === recentGeneration) recentLoading.value = false
  }
}

async function loadData() {
  await Promise.all([loadStats(), loadRecent()])
}

function refreshAll() {
  void loadRules()
  void loadData()
}

function applyCustomRange() {
  const [start, end] = customDates.value
  if (!start || !end) {
    dateError.value = '请选择完整的起止日期'
    return
  }
  if (start > end) {
    dateError.value = '开始日期不能晚于结束日期'
    return
  }
  dateError.value = ''
  void loadData()
}

function openHistory(id: number) {
  void router.push({ name: 'history', query: { id: String(id) } })
}
</script>

<template>
  <div class="page-shell">
    <PageHeader
      title="运维总览"
      description="先了解服务与诊断态势，再进入具体异常。所有指标均来自现有诊断日志，不展示尚未接入的处置数据。"
    >
      <template #extra>
        <a-button @click="$router.push('/batch')"><TableOutlined /> 批量回放</a-button>
        <a-button type="primary" @click="$router.push('/diagnose')"><MedicineBoxOutlined /> 开始诊断</a-button>
      </template>
    </PageHeader>

    <section class="overview-filter surface-card" aria-label="总览筛选">
      <div class="range-controls">
        <span class="filter-caption">统计范围</span>
        <a-radio-group v-model:value="range" option-type="button" button-style="solid">
          <a-radio-button value="all">全部</a-radio-button>
          <a-radio-button value="7">近 7 天</a-radio-button>
          <a-radio-button value="30">近 30 天</a-radio-button>
          <a-radio-button value="custom">自定义</a-radio-button>
        </a-radio-group>
        <template v-if="range === 'custom'">
          <a-range-picker
            v-model:value="customDates"
            value-format="YYYYMMDD"
            format="YYYY-MM-DD"
            :allow-clear="false"
          />
          <a-button type="primary" @click="applyCustomRange">应用</a-button>
        </template>
        <span v-if="dateError" class="date-error" role="alert">{{ dateError }}</span>
      </div>
      <div class="refresh-info">
        <span>{{ rangeLabel }}<template v-if="lastUpdated"> · 更新于 {{ lastUpdated }}</template></span>
        <a-button type="text" :loading="refreshing" aria-label="刷新总览" @click="refreshAll"><ReloadOutlined /></a-button>
      </div>
    </section>

    <a-alert
      v-if="statsError"
      type="warning"
      show-icon
      :message="statsError"
      :description="stats ? '当前仍显示上次成功加载的数据。' : '统计数据暂不可用，不会用数字 0 代替未知值。'"
      class="overview-alert"
    >
      <template #action><a-button size="small" @click="loadStats">重试</a-button></template>
    </a-alert>

    <section class="metric-grid" :class="{ 'is-refreshing': statsLoading && stats }" aria-label="关键指标">
      <a-card v-for="metric in kpis" :key="metric.key" class="metric-card">
        <a-skeleton v-if="statsLoading && !stats" active :paragraph="false" :title="{ width: '45%' }" />
        <template v-else>
          <span class="metric-label">{{ metric.label }}</span>
          <strong :class="{ 'metric-danger': metric.danger }">{{ typeof metric.value === 'number' ? metric.value.toLocaleString('zh-CN') : metric.value }}</strong>
          <p>{{ metric.hint }}</p>
        </template>
      </a-card>
    </section>

    <div class="charts-grid">
      <a-card title="真实异常诊断趋势">
        <BaseChart
          :option="trendChart"
          title="真实异常诊断趋势"
          :rows="trendRows"
          series-name="诊断数"
          :loading="statsLoading"
          :height="292"
        />
      </a-card>
      <a-card title="高频问题 TOP">
        <BaseChart
          :option="topTypeChart"
          title="高频问题 TOP"
          :rows="topTypeRows"
          series-name="诊断数"
          :loading="statsLoading"
          :height="292"
        />
      </a-card>
    </div>

    <div class="overview-bottom">
      <a-card>
        <template #title>最新真实异常</template>
        <template #extra>
          <a-button type="link" @click="$router.push({ name: 'history', query: { anomaly_only: 'true' } })">
            查看全部 <RightOutlined />
          </a-button>
        </template>
        <StateBlock
          :loading="recentLoading && !recent.length"
          :error="recent.length ? '' : recentError"
          :empty="!recent.length && !recentError"
          empty-text="当前范围内没有真实异常诊断记录"
          @retry="loadRecent"
        >
          <a-alert v-if="recentError" type="warning" show-icon :message="recentError" class="inline-alert" />
          <div class="anomaly-list">
            <button v-for="record in recent" :key="record.id" type="button" class="anomaly-row" @click="openHistory(record.id)">
              <span class="anomaly-main">
                <span class="anomaly-topline">
                  <strong>{{ ruleTypeLabel(record.diag_type, rules?.rules) }}</strong>
                  <span>{{ SOURCE_LABELS[record.source ?? ''] ?? record.source ?? '未知来源' }}</span>
                </span>
                <span class="anomaly-root">{{ record.root_cause || record.error_text || '暂无根因摘要' }}</span>
                <span class="anomaly-meta">#{{ record.id }} · {{ formatBusinessDate(record.business_date) }}</span>
              </span>
              <span class="anomaly-side">
                <StatusTag
                  :status="record.diag_status"
                  :label="record.diag_status === 'success' ? '诊断完成' : '诊断失败'"
                  :tone="record.diag_status === 'success' ? 'success' : 'error'"
                />
                <RightOutlined class="row-arrow" />
              </span>
            </button>
          </div>
        </StateBlock>
      </a-card>

      <div class="side-stack">
        <a-card title="诊断分类">
          <a-empty v-if="!classTotal && !statsLoading" description="当前范围暂无分类数据" />
          <div v-else class="class-list">
            <div v-for="row in stats?.by_class ?? []" :key="row.key ?? 'unknown'" class="class-row">
              <div class="class-label"><span>{{ diagnosisClassLabel(row.key) }}</span><strong>{{ row.count }}</strong></div>
              <div class="class-meter">
                <a-progress
                  :percent="classTotal ? Math.round(row.count / classTotal * 100) : 0"
                  :show-info="false"
                  :stroke-width="7"
                  stroke-color="#2a78d6"
                  trail-color="#edf1f6"
                />
                <span>{{ classTotal ? formatPercent(row.count / classTotal, 0) : '—' }}</span>
              </div>
            </div>
          </div>
        </a-card>

        <a-card title="规则与标注">
          <StateBlock :loading="rulesLoading && !rules" :error="rulesError" @retry="loadRules">
            <dl class="rules-summary">
              <div><dt>规则类型</dt><dd>{{ rules?.total ?? '—' }}</dd></div>
              <div><dt>噪音关键词</dt><dd>{{ rules?.noise_keywords.length ?? '—' }}</dd></div>
              <div><dt>已人工标注</dt><dd>{{ stats?.annotated ?? '—' }}</dd></div>
            </dl>
            <p class="coverage-copy">{{ rules?.coverage || '暂无规则覆盖说明' }}</p>
          </StateBlock>
        </a-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overview-filter {
  display: flex;
  margin-bottom: 20px;
  padding: 14px 16px;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
}

.range-controls,
.refresh-info {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-caption {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.refresh-info {
  flex: none;
  color: var(--text-muted);
  font-size: 12px;
}

.date-error {
  color: var(--danger);
  font-size: 12px;
}

.overview-alert,
.inline-alert {
  margin-bottom: 16px;
}

.metric-grid {
  display: grid;
  margin-bottom: 20px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.metric-card {
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 3px;
  background: var(--brand);
  opacity: 0.75;
  content: '';
}

.metric-label {
  display: block;
  margin-bottom: 10px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.metric-card strong {
  display: block;
  margin-bottom: 10px;
  color: var(--text-primary);
  font-size: clamp(28px, 3vw, 36px);
  font-weight: 650;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.metric-card strong.metric-danger {
  color: var(--danger);
}

.metric-card p {
  min-height: 34px;
  margin-bottom: 0;
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1.55;
}

.charts-grid {
  display: grid;
  margin-bottom: 20px;
  grid-template-columns: minmax(0, 1.35fr) minmax(360px, 0.85fr);
  gap: 20px;
}

.overview-bottom {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.85fr);
  gap: 20px;
  align-items: start;
}

.side-stack {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 20px;
}

.anomaly-list {
  margin: -8px 0;
}

.anomaly-row {
  display: flex;
  width: 100%;
  padding: 15px 4px;
  gap: 16px;
  align-items: center;
  color: var(--text-primary);
  text-align: left;
  background: transparent;
  border: 0;
  border-bottom: 1px solid var(--border-soft);
  cursor: pointer;
}

.anomaly-row:last-child {
  border-bottom: 0;
}

.anomaly-row:hover {
  background: #fafcff;
}

.anomaly-main {
  display: flex;
  min-width: 0;
  flex: 1;
  flex-direction: column;
}

.anomaly-topline {
  display: flex;
  margin-bottom: 6px;
  gap: 10px;
  align-items: baseline;
}

.anomaly-topline strong {
  font-size: 14px;
}

.anomaly-topline > span,
.anomaly-meta {
  color: var(--text-muted);
  font-size: 11px;
}

.anomaly-root {
  margin-bottom: 7px;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.anomaly-side {
  display: flex;
  flex: none;
  gap: 12px;
  align-items: center;
}

.row-arrow {
  color: #8a96a8;
}

.class-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.class-label,
.class-meter {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.class-label {
  margin-bottom: 7px;
  color: var(--text-secondary);
  font-size: 13px;
}

.class-label strong {
  color: var(--text-primary);
}

.class-meter :deep(.ant-progress) {
  min-width: 0;
  flex: 1;
  margin: 0;
}

.class-meter > span {
  width: 38px;
  color: var(--text-muted);
  font-size: 12px;
  text-align: right;
}

.rules-summary {
  display: grid;
  margin: 0 0 14px;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.rules-summary > div {
  min-width: 0;
}

.rules-summary dt {
  margin-bottom: 5px;
  color: var(--text-muted);
  font-size: 11px;
}

.rules-summary dd {
  margin: 0;
  color: var(--text-primary);
  font-size: 22px;
  font-weight: 600;
}

.coverage-copy {
  margin: 0;
  padding: 12px;
  color: var(--text-secondary);
  background: var(--surface-subtle);
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.65;
}

.is-refreshing {
  opacity: 0.62;
}

@media (max-width: 1199px) {
  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .charts-grid,
  .overview-bottom {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 767px) {
  .overview-filter {
    align-items: flex-start;
    flex-direction: column;
  }

  .refresh-info {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 640px) {
  .metric-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 12px;
  }

  .metric-card p {
    min-height: 0;
  }

  .anomaly-side :deep(.ant-tag) {
    display: none;
  }
}
</style>
