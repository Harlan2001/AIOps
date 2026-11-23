<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter, type LocationQuery } from 'vue-router'
import { EditOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

import {
  annotateDiagnosis,
  getDiagnoses,
  getDiagnosisDetail,
  type DiagListParams,
} from '@/api/diagnoses'
import { getRules } from '@/api/meta'
import { ApiError } from '@/api/client'
import PageHeader from '@/components/PageHeader.vue'
import ResponsiveDrawer from '@/components/ResponsiveDrawer.vue'
import ResultCard from '@/components/ResultCard.vue'
import StateBlock from '@/components/StateBlock.vue'
import StatusTag from '@/components/StatusTag.vue'
import { LOG_SOURCES, SOURCE_LABELS } from '@/constants/sources'
import { formatBusinessDate, formatConfidence, formatDateTime, parseDiagnosisResult } from '@/utils/diagnosis'
import { ruleTypeLabel } from '@/utils/label'
import type { DiagLogItem, RuleItem } from '@/types/contract'

const PAGE_SIZE = 10
const route = useRoute()
const router = useRouter()
const items = ref<DiagLogItem[]>([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)
const errorMsg = ref('')
let listGeneration = 0
let detailGeneration = 0

const source = ref<string>()
const diagClass = ref<string>()
const diagType = ref<string>()
const annotFilter = ref<string>()
const dates = ref<[string, string]>(['', ''])
const anomalyOnly = ref(false)
const dimpleOnly = ref(false)
const dateError = ref('')
const filtersExpanded = ref(false)
const activeFilterCount = computed(() => [
  source.value,
  diagClass.value,
  diagType.value,
  annotFilter.value,
  dates.value[0] || dates.value[1],
  anomalyOnly.value,
  dimpleOnly.value,
].filter(Boolean).length)

const rules = ref<RuleItem[]>([])
const rulesLoading = ref(false)
const rulesError = ref('')
const ruleOptions = computed(() => rules.value.map((rule) => ({ value: rule.id, label: `${rule.title}（${rule.id}）` })))
const sourceOptions = LOG_SOURCES.map((item) => ({ value: item.id, label: `${item.label}（${item.id}）` }))
const classOptions = [
  { value: 'biz', label: '业务报错' },
  { value: 'noise', label: '噪音' },
  { value: 'ora', label: 'DBA 技术错误' },
  { value: 'other', label: '其他/未识别' },
]
const annotOptions = [
  { value: 'correct', label: '已标正确' },
  { value: 'wrong', label: '已标错误' },
]

const columns = [
  { title: 'ID', dataIndex: 'id', width: 80, responsive: ['md'] },
  { title: '业务日期', dataIndex: 'business_date', width: 120, responsive: ['sm'] },
  { title: '来源', dataIndex: 'source', width: 180 },
  { title: '分类', dataIndex: 'diag_class', width: 130 },
  { title: '类型', dataIndex: 'diag_type', width: 150 },
  { title: '根因摘要', dataIndex: 'root_cause', width: 280, ellipsis: true },
  { title: '置信度', dataIndex: 'confidence', width: 100 },
  { title: '诊断状态', dataIndex: 'diag_status', width: 120 },
  { title: '人工标注', dataIndex: 'annot_status', width: 120 },
  { title: '诊断时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', key: 'action', width: 170, fixed: 'right' as const },
]

const drawerOpen = ref(false)
const detail = ref<DiagLogItem | null>(null)
const detailLoading = ref(false)
const detailError = ref('')
const activeDetailId = ref<number | null>(null)
const parsed = computed(() => parseDiagnosisResult(detail.value?.result_json))
const parsedResult = computed(() => parsed.value.result)

const annotModalOpen = ref(false)
const annotTarget = ref<DiagLogItem | null>(null)
const annotStatus = ref<'correct' | 'wrong'>('correct')
const correctAnswer = ref('')
const annotator = ref('')
const submitLoading = ref(false)
const annotErrors = reactive({ annotator: '', correctAnswer: '', form: '' })

function queryValue(value: unknown): string {
  return Array.isArray(value) ? String(value[0] ?? '') : String(value ?? '')
}

function readFilters() {
  source.value = queryValue(route.query.source) || undefined
  diagClass.value = queryValue(route.query.diag_class) || undefined
  diagType.value = queryValue(route.query.diag_type) || undefined
  annotFilter.value = queryValue(route.query.annot_status) || undefined
  dates.value = [queryValue(route.query.start_date), queryValue(route.query.end_date)]
  anomalyOnly.value = queryValue(route.query.anomaly_only) === 'true'
  dimpleOnly.value = queryValue(route.query.dimple_only) === 'true'
  page.value = Math.max(1, Number(queryValue(route.query.page)) || 1)
  dateError.value = ''
}

function buildQuery(id?: string | number): LocationQuery {
  const query: LocationQuery = {}
  if (source.value) query.source = source.value
  if (diagClass.value) query.diag_class = diagClass.value
  if (diagType.value) query.diag_type = diagType.value
  if (annotFilter.value) query.annot_status = annotFilter.value
  if (dates.value[0]) query.start_date = dates.value[0]
  if (dates.value[1]) query.end_date = dates.value[1]
  if (anomalyOnly.value) query.anomaly_only = 'true'
  if (dimpleOnly.value) query.dimple_only = 'true'
  if (page.value > 1) query.page = String(page.value)
  if (id !== undefined && id !== '') query.id = String(id)
  return query
}

function updateQuery(preserveDetail = true) {
  const id = preserveDetail ? queryValue(route.query.id) : ''
  void router.replace({ name: 'history', query: buildQuery(id) })
}

const filterWatchKey = computed(() => JSON.stringify([
  route.query.source,
  route.query.diag_class,
  route.query.diag_type,
  route.query.annot_status,
  route.query.start_date,
  route.query.end_date,
  route.query.anomaly_only,
  route.query.dimple_only,
  route.query.page,
]))

watch(filterWatchKey, () => {
  readFilters()
  void load()
}, { immediate: true })

watch(() => route.query.id, (value) => {
  const id = Number(queryValue(value))
  if (Number.isInteger(id) && id > 0) {
    drawerOpen.value = true
    void loadDetail(id)
  } else {
    detailGeneration += 1
    drawerOpen.value = false
    detail.value = null
  }
}, { immediate: true })

onMounted(loadRules)

async function loadRules() {
  rulesLoading.value = true
  rulesError.value = ''
  try {
    rules.value = (await getRules()).rules
  } catch (error) {
    rulesError.value = error instanceof ApiError ? error.message : '规则类型加载失败'
  } finally {
    rulesLoading.value = false
  }
}

function buildParams(): DiagListParams {
  return {
    source: source.value,
    diag_class: diagClass.value,
    diag_type: diagType.value,
    annot_status: annotFilter.value,
    start_date: dates.value[0] || undefined,
    end_date: dates.value[1] || undefined,
    anomaly_only: anomalyOnly.value || undefined,
    dimple_only: dimpleOnly.value || undefined,
    offset: (page.value - 1) * PAGE_SIZE,
    limit: PAGE_SIZE,
  }
}

async function load() {
  const requestGeneration = ++listGeneration
  loading.value = true
  errorMsg.value = ''
  try {
    const response = await getDiagnoses(buildParams())
    if (requestGeneration !== listGeneration) return
    items.value = response.items
    total.value = response.total
  } catch (error) {
    if (requestGeneration !== listGeneration) return
    errorMsg.value = error instanceof ApiError ? `加载失败（${error.status}）：${error.message}` : '加载异常，请稍后重试'
  } finally {
    if (requestGeneration === listGeneration) loading.value = false
  }
}

function search() {
  const [start, end] = dates.value
  if ((start && !end) || (!start && end)) {
    dateError.value = '请选择完整的起止日期，或清空日期范围'
    return
  }
  if (start && end && start > end) {
    dateError.value = '开始日期不能晚于结束日期'
    return
  }
  dateError.value = ''
  page.value = 1
  filtersExpanded.value = false
  updateQuery()
}

function reset() {
  source.value = undefined
  diagClass.value = undefined
  diagType.value = undefined
  annotFilter.value = undefined
  dates.value = ['', '']
  anomalyOnly.value = false
  dimpleOnly.value = false
  dateError.value = ''
  page.value = 1
  updateQuery()
}

function onTableChange(pagination: { current?: number }) {
  page.value = pagination.current ?? 1
  updateQuery()
}

function onMobilePageChange(nextPage: number) {
  onTableChange({ current: nextPage })
}

async function loadDetail(id: number) {
  const requestGeneration = ++detailGeneration
  activeDetailId.value = id
  detailLoading.value = true
  detailError.value = ''
  detail.value = null
  try {
    const response = await getDiagnosisDetail(id)
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
  void router.replace({ name: 'history', query: buildQuery(record.id) })
}

function closeDetail() {
  updateQuery(false)
}

function retryDetail() {
  if (activeDetailId.value !== null) void loadDetail(activeDetailId.value)
}

function openAnnot(record: DiagLogItem) {
  annotTarget.value = record
  annotStatus.value = record.annot_status === 'wrong' ? 'wrong' : 'correct'
  correctAnswer.value = record.correct_answer ?? ''
  annotator.value = record.annotator ?? ''
  annotErrors.annotator = ''
  annotErrors.correctAnswer = ''
  annotErrors.form = ''
  annotModalOpen.value = true
}

async function submitAnnot() {
  annotErrors.annotator = annotator.value.trim() ? '' : '请填写标注人'
  annotErrors.correctAnswer = annotStatus.value === 'wrong' && !correctAnswer.value.trim() ? '标记为错误时请填写正确答案' : ''
  annotErrors.form = ''
  if (annotErrors.annotator || annotErrors.correctAnswer || !annotTarget.value) return

  submitLoading.value = true
  const target = annotTarget.value
  try {
    await annotateDiagnosis(target.id, {
      annot_status: annotStatus.value,
      correct_answer: annotStatus.value === 'wrong' ? correctAnswer.value.trim() : null,
      annotator: annotator.value.trim(),
    })
    message.success('标注已保存')
    annotModalOpen.value = false
    const changes = {
      annot_status: annotStatus.value,
      correct_answer: annotStatus.value === 'wrong' ? correctAnswer.value.trim() : null,
      annotator: annotator.value.trim(),
    }
    items.value = items.value.map((item) => item.id === target.id ? { ...item, ...changes } : item)
    if (detail.value?.id === target.id) detail.value = { ...detail.value, ...changes }
    void load()
  } catch (error) {
    annotErrors.form = error instanceof ApiError ? `标注保存失败：${error.message}` : '标注保存失败，请稍后重试'
  } finally {
    submitLoading.value = false
  }
}
</script>

<template>
  <div class="page-shell">
    <PageHeader
      title="历史诊断"
      description="按来源、类型、日期和标注状态追溯诊断记录。筛选与页码会保留在地址栏，便于返回和内部共享。"
    />

    <a-card class="history-filter-card" :class="{ 'filters-collapsed': !filtersExpanded }">
      <div class="mobile-filter-bar">
        <span>筛选条件 <a-tag v-if="activeFilterCount" color="blue">{{ activeFilterCount }}</a-tag></span>
        <a-button type="text" size="small" @click="filtersExpanded = !filtersExpanded">
          {{ filtersExpanded ? '收起' : '展开筛选' }}
        </a-button>
      </div>
      <a-form layout="vertical" @submit.prevent="search">
        <div class="history-filter-grid">
          <a-form-item label="来源">
            <a-select v-model:value="source" allow-clear show-search option-filter-prop="label" :options="sourceOptions" placeholder="全部来源" />
          </a-form-item>
          <a-form-item label="分类">
            <a-select v-model:value="diagClass" allow-clear :options="classOptions" placeholder="全部分类" />
          </a-form-item>
          <a-form-item label="问题类型">
            <a-select
              v-model:value="diagType"
              allow-clear
              show-search
              option-filter-prop="label"
              :options="ruleOptions"
              :loading="rulesLoading"
              placeholder="全部类型"
            />
            <div v-if="rulesError" class="filter-help">类型选项加载失败，其他筛选仍可使用。<a @click="loadRules">重试</a></div>
          </a-form-item>
          <a-form-item label="人工标注">
            <a-select v-model:value="annotFilter" allow-clear :options="annotOptions" placeholder="全部标注状态" />
          </a-form-item>
          <a-form-item label="业务日期范围" class="date-range-item" :validate-status="dateError ? 'error' : ''" :help="dateError">
            <a-range-picker v-model:value="dates" value-format="YYYYMMDD" format="YYYY-MM-DD" class="full-width" @change="dateError = ''" />
          </a-form-item>
          <a-form-item label="记录范围" class="scope-item">
            <div class="scope-options">
              <a-checkbox v-model:checked="anomalyOnly">仅真实异常</a-checkbox>
              <a-checkbox v-model:checked="dimpleOnly">仅 Dimple</a-checkbox>
            </div>
          </a-form-item>
          <a-form-item label=" " class="filter-button-item">
            <a-space>
              <a-button type="primary" html-type="submit">查询</a-button>
              <a-button @click="reset">重置</a-button>
            </a-space>
          </a-form-item>
        </div>
      </a-form>
    </a-card>

    <a-alert v-if="errorMsg && items.length" type="error" show-icon :message="errorMsg" class="list-alert" />
    <a-card class="history-table-card">
      <template #title>诊断记录</template>
      <template #extra><span class="record-count">共 {{ total }} 条</span></template>
      <StateBlock v-if="loading && !items.length" loading :loading-rows="7" />
      <StateBlock v-else-if="errorMsg && !items.length" :error="errorMsg" @retry="load" />
      <a-empty v-else-if="!items.length" description="没有符合当前条件的诊断记录，请调整筛选或日期范围" />
      <div v-else class="responsive-records">
        <div class="desktop-records">
          <a-table
            :columns="columns"
            :data-source="items"
            :loading="loading"
            row-key="id"
            :scroll="{ x: 1640 }"
            :pagination="{ current: page, pageSize: PAGE_SIZE, total, showSizeChanger: false }"
            @change="onTableChange"
          >
            <template #bodyCell="{ column, record }">
              <span v-if="column.dataIndex === 'business_date'">{{ formatBusinessDate(record.business_date) }}</span>
              <span v-else-if="column.dataIndex === 'source'" :title="record.source">{{ SOURCE_LABELS[record.source ?? ''] ?? record.source ?? '—' }}</span>
              <StatusTag v-else-if="column.dataIndex === 'diag_class'" :status="record.diag_class" />
              <span v-else-if="column.dataIndex === 'diag_type'">{{ ruleTypeLabel(record.diag_type, rules) }}</span>
              <span v-else-if="column.dataIndex === 'root_cause'" class="cell-text" :title="record.root_cause">{{ record.root_cause || record.error_text || '—' }}</span>
              <span v-else-if="column.dataIndex === 'confidence'" class="numeric-cell">{{ formatConfidence(record.confidence) }}</span>
              <StatusTag
                v-else-if="column.dataIndex === 'diag_status'"
                :status="record.diag_status"
                :label="record.diag_status === 'success' ? '诊断完成' : '诊断失败'"
                :tone="record.diag_status === 'success' ? 'success' : 'error'"
              />
              <StatusTag v-else-if="column.dataIndex === 'annot_status'" :status="record.annot_status || 'unannotated'" />
              <span v-else-if="column.dataIndex === 'created_at'" class="numeric-cell">{{ formatDateTime(record.created_at) }}</span>
              <a-space v-else-if="column.key === 'action'" :size="0">
                <a-button type="link" size="small" @click="openDetail(record)">详情</a-button>
                <a-button type="link" size="small" @click="openAnnot(record)">标注</a-button>
              </a-space>
            </template>
          </a-table>
        </div>
        <div class="mobile-records">
          <article v-for="record in items" :key="record.id" class="mobile-record-card">
            <button type="button" class="mobile-record-main" @click="openDetail(record)">
              <span class="mobile-record-top">
                <span class="mobile-record-source">{{ SOURCE_LABELS[record.source ?? ''] ?? record.source ?? '未知来源' }} · #{{ record.id }}</span>
                <StatusTag
                  :status="record.diag_status"
                  :label="record.diag_status === 'success' ? '诊断完成' : '诊断失败'"
                  :tone="record.diag_status === 'success' ? 'success' : 'error'"
                />
              </span>
              <strong>{{ ruleTypeLabel(record.diag_type, rules) }}</strong>
              <span class="mobile-record-description">{{ record.root_cause || record.error_text || '暂无根因摘要' }}</span>
              <span class="mobile-record-meta">{{ formatBusinessDate(record.business_date) }} · 置信度 {{ formatConfidence(record.confidence) }}</span>
              <StatusTag :status="record.annot_status || 'unannotated'" />
            </button>
            <div class="mobile-record-actions">
              <a-button size="small" @click="openAnnot(record)"><EditOutlined /> 标注</a-button>
              <a-button size="small" type="primary" ghost @click="openDetail(record)">查看详情</a-button>
            </div>
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

    <ResponsiveDrawer v-model:open="drawerOpen" title="历史诊断详情" :width="820" @close="closeDetail">
      <StateBlock v-if="detailLoading" loading :loading-rows="8" />
      <StateBlock v-else-if="detailError" :error="detailError" error-title="无法打开诊断详情" @retry="retryDetail" />
      <template v-else-if="detail">
        <section class="detail-summary">
          <div class="detail-title-row">
            <div>
              <span class="detail-source">{{ SOURCE_LABELS[detail.source ?? ''] ?? detail.source ?? '未知来源' }} · #{{ detail.id }}</span>
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
            <div><dt>触发方式</dt><dd>{{ detail.trigger_type || '—' }} / {{ detail.input_mode || '—' }}</dd></div>
            <div><dt>诊断路径</dt><dd>{{ detail.diag_path || '—' }}</dd></div>
          </dl>
          <div class="annotation-summary">
            <StatusTag :status="detail.annot_status || 'unannotated'" />
            <span v-if="detail.annotator">{{ detail.annotator }}<template v-if="detail.annotated_at"> · {{ formatDateTime(detail.annotated_at) }}</template></span>
            <a-button size="small" @click="openAnnot(detail)"><EditOutlined /> {{ detail.annot_status ? '修改标注' : '添加标注' }}</a-button>
          </div>
          <p v-if="detail.annot_status === 'wrong' && detail.correct_answer" class="correct-answer"><strong>人工正确答案：</strong>{{ detail.correct_answer }}</p>
        </section>

        <a-alert
          v-if="parsed.error"
          type="warning"
          show-icon
          :message="parsed.error"
          description="已保存的摘要仍可参考；完整动作与证据暂不可展示。"
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
      </template>
    </ResponsiveDrawer>

    <a-modal
      v-model:open="annotModalOpen"
      :title="annotTarget?.annot_status ? '修改人工标注' : '添加人工标注'"
      :confirm-loading="submitLoading"
      ok-text="保存标注"
      cancel-text="取消"
      @ok="submitAnnot"
    >
      <a-form layout="vertical" @submit.prevent="submitAnnot">
        <a-alert v-if="annotErrors.form" type="error" show-icon :message="annotErrors.form" class="annot-alert" />
        <a-form-item label="标注结论" required>
          <a-radio-group v-model:value="annotStatus" @change="annotErrors.correctAnswer = ''">
            <a-radio value="correct">标记为正确</a-radio>
            <a-radio value="wrong">标记为错误</a-radio>
          </a-radio-group>
          <p class="annot-help">这是你对诊断结论的人工评价，不会重新执行诊断。</p>
        </a-form-item>
        <a-form-item label="标注人" required :validate-status="annotErrors.annotator ? 'error' : ''" :help="annotErrors.annotator">
          <a-input v-model:value="annotator" placeholder="请输入姓名或工号" @input="annotErrors.annotator = ''" />
        </a-form-item>
        <a-form-item v-if="annotStatus === 'wrong'" label="正确答案" required :validate-status="annotErrors.correctAnswer ? 'error' : ''" :help="annotErrors.correctAnswer">
          <a-textarea v-model:value="correctAnswer" :rows="4" placeholder="请填写正确结论或建议处理方式" @input="annotErrors.correctAnswer = ''" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.history-filter-card {
  margin-bottom: 20px;
}

.mobile-filter-bar {
  display: none;
}

.history-filter-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(160px, 1fr));
  gap: 0 16px;
}

.history-filter-grid :deep(.ant-form-item) {
  margin-bottom: 16px;
}

.date-range-item {
  grid-column: span 2;
}

.full-width {
  width: 100%;
}

.scope-options {
  display: flex;
  min-height: 38px;
  gap: 16px;
  align-items: center;
}

.filter-help {
  color: var(--warning);
  font-size: 11px;
  line-height: 1.5;
}

.filter-help a {
  margin-left: 4px;
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
  margin: 0 0 16px;
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

.annotation-summary {
  display: flex;
  padding-top: 12px;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  border-top: 1px solid var(--border-soft);
  color: var(--text-secondary);
  font-size: 12px;
}

.annotation-summary .ant-btn {
  margin-left: auto;
}

.correct-answer {
  margin: 12px 0 0 !important;
  padding: 10px 12px;
  background: var(--warning-soft);
  border-radius: 8px;
}

.snapshot-alert {
  margin-bottom: 16px;
}

.fallback-detail {
  padding: 20px 0;
}

.report-fallback {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.report-fallback > div:last-child {
  grid-column: 1 / -1;
}

.annot-alert {
  margin-bottom: 16px;
}

.annot-help {
  margin: 8px 0 0;
  color: var(--text-muted);
  font-size: 12px;
}

@media (max-width: 1199px) {
  .history-filter-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
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
    align-items: flex-start;
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
    width: 100%;
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

  .mobile-record-actions {
    display: flex;
    padding: 10px 15px;
    gap: 8px;
    justify-content: flex-end;
    background: var(--surface-subtle);
    border-top: 1px solid var(--border-soft);
  }

  .mobile-records :deep(.ant-pagination) {
    justify-content: center;
    margin-top: 4px;
  }
}

@media (max-width: 640px) {
  .mobile-filter-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 500;
  }

  .history-filter-card.filters-collapsed .history-filter-grid {
    display: none;
  }

  .history-filter-card.filters-collapsed :deep(.ant-card-body) {
    padding: 10px 14px;
  }

  .history-filter-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .date-range-item {
    grid-column: auto;
  }

  .filter-button-item :deep(.ant-space),
  .filter-button-item :deep(.ant-btn) {
    width: 100%;
  }

  .detail-meta,
  .report-fallback {
    grid-template-columns: minmax(0, 1fr);
  }

  .report-fallback > div:last-child {
    grid-column: auto;
  }

  .annotation-summary .ant-btn {
    width: 100%;
    margin-left: 0;
  }
}
</style>
