<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'

import { getRealtimeAlarms, getRealtimeDetail } from '@/api/realtime'
import { diagnose } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import type {
  Answer,
  DiagLogItem,
  DiagnosisResult,
  EvidenceRow,
} from '@/types/contract'
import { labelNull } from '@/utils/label'
import { REALTIME_SOURCE_LABELS } from '@/constants/sources'
import { Empty } from 'ant-design-vue'

const simpleImage = Empty.PRESENTED_IMAGE_SIMPLE

const PAGE_SIZE = 10

// 视图模式：anomaly=只看真实异常（默认）；all=全部记录（含业务数据，可核对）。
const viewMode = ref<'anomaly' | 'all'>('anomaly')

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
  { title: '预警内容', dataIndex: 'error_text', width: 320, ellipsis: true },
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

// AI 大模型按需诊断（默认关闭，不耗 token；打开开关才调用一次 LLM）
const llmEnabled = ref(false)
const llmLoading = ref(false)
const llmAnswer = ref<Answer | null>(null)
const llmError = ref('')
const LLM_TIMEOUT = 180000

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
      viewMode.value === 'anomaly',
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

function onRadioChange(e: { target: { value: 'anomaly' | 'all' } }) {
  onViewModeChange(e.target.value)
}

function onViewModeChange(mode: 'anomaly' | 'all') {
  viewMode.value = mode
  page.value = 1
  load()
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
  resetLlm()
  try {
    detail.value = await getRealtimeDetail(record.id)
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError ? `详情加载失败：${e.message}` : '详情加载失败'
  } finally {
    detailLoading.value = false
  }
}

function resetLlm() {
  llmEnabled.value = false
  llmLoading.value = false
  llmAnswer.value = null
  llmError.value = ''
}

// 开关变化：关闭则清空；打开则调用大模型对当前这条报错做一次升级诊断。
async function onLlmToggle(enabled: boolean) {
  llmEnabled.value = enabled
  if (!enabled) {
    llmAnswer.value = null
    llmError.value = ''
    return
  }
  if (!detail.value) return
  llmLoading.value = true
  llmError.value = ''
  llmAnswer.value = null
  try {
    const res: DiagnosisResult = await diagnose(
      {
        text: detail.value.error_text ?? '',
        ldate: detail.value.business_date ?? '',
        escalate: true,
      },
      { timeout: LLM_TIMEOUT },
    )
    llmAnswer.value = res.answer
    if (!res.answer) llmError.value = '大模型未返回有效结论（可能已降级为规则结果）'
  } catch (e) {
    llmEnabled.value = false
    llmError.value =
      e instanceof ApiError
        ? e.status === 409
          ? '当前部署未开启大模型升级（allow_escalation=false）'
          : `大模型调用失败（${e.status}）：${e.message}`
        : '大模型调用异常，请稍后重试'
  } finally {
    llmLoading.value = false
  }
}

// 解析详情里的完整诊断快照（含根因、处理建议、取证证据）。
const parsed = computed<DiagnosisResult | null>(() => {
  if (!detail.value?.result_json) return null
  try {
    return JSON.parse(detail.value.result_json) as DiagnosisResult
  } catch {
    return null
  }
})

// 处理建议（来自诊断 answer.actions）。
const actions = computed<string[]>(
  () => parsed.value?.answer?.actions ?? [],
)

// 取证证据列表（来自 rule_res.evidence）。
const evidenceList = computed<EvidenceRow[]>(
  () => parsed.value?.rule_res?.evidence ?? [],
)

// 证据列定义与数据行（后端返回 cols 列名 + rows 二维数组，转成表格需要的对象）。
function evidenceColumns(ev: EvidenceRow) {
  return (ev.r?.cols ?? []).map((c) => ({ title: c, dataIndex: c }))
}
function evidenceData(ev: EvidenceRow) {
  const cols = ev.r?.cols ?? []
  return (ev.r?.rows ?? []).map((row) => {
    const obj: Record<string, unknown> = {}
    cols.forEach((c, i) => {
      obj[c] = (row as unknown[])[i]
    })
    return obj
  })
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

    <div class="view-bar">
      <a-radio-group
        :value="viewMode"
        option-type="button"
        button-style="solid"
        @change="onRadioChange"
      >
        <a-radio-button value="anomaly">真实异常</a-radio-button>
        <a-radio-button value="all">全部记录（含业务数据）</a-radio-button>
      </a-radio-group>
      <span class="view-tip">
        {{ viewMode === 'anomaly'
          ? '仅展示需要运维处理的报错/告警，正常业务数据见全部记录'
          : '展示 Dimple 子系统全部落库记录，可逐条核对过滤是否正确。' }}
      </span>
    </div>

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
        <a
          v-else-if="column.dataIndex === 'error_text'"
          class="link-text cell-ellipsis"
          :title="record.error_text"
          @click="openDetail(record)"
        >
          {{ record.error_text }}
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
      :description="viewMode === 'anomaly'
        ? '暂无真实异常（Dimple 产生合规预警、自成交、违规委托或错单后将自动出现在这里）'
        : '当前没有任何落库记录'"
    />
  </a-card>

  <a-drawer v-model:open="drawerOpen" title="实时预警详情" width="680">
    <a-spin :spinning="detailLoading">
      <template v-if="detail">
        <!-- 一、基本信息 -->
        <a-descriptions :column="1" bordered size="small" class="detail-section">
          <a-descriptions-item label="ID">{{ detail.id }}</a-descriptions-item>
          <a-descriptions-item label="来源 / 日期">
            {{ sourceLabel(detail.source) }} / {{ detail.business_date }}
          </a-descriptions-item>
          <a-descriptions-item label="预警文本">{{ detail.error_text }}</a-descriptions-item>
          <a-descriptions-item label="分类 / 类型">
            {{ labelNull(detail.diag_class) }} /
            {{ parsed?.rule_res?.type?.title ?? labelNull(detail.diag_type) }}
          </a-descriptions-item>
          <a-descriptions-item label="置信度">
            {{ fmtConf(detail.confidence) }}
          </a-descriptions-item>
          <a-descriptions-item label="诊断路径 / 状态">
            {{ labelNull(detail.diag_path) }} / {{ detail.diag_status }}
          </a-descriptions-item>
          <a-descriptions-item label="是否升级">
            <a-tag :color="detail.escalated ? 'red' : 'green'">
              {{ detail.escalated ? '已升级' : '未升级' }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="诊断时间">{{ detail.created_at }}</a-descriptions-item>
        </a-descriptions>

        <!-- 二、问题是什么 -->
        <div class="detail-section">
          <div class="section-title">问题是什么</div>
          <a-alert
            type="error"
            show-icon
            :message="parsed?.answer?.root || detail.root_cause || '暂无根因结论'"
          />
          <div v-if="parsed?.rule_res?.verdict" class="verdict">
            诊断结论：{{ parsed.rule_res.verdict }}
          </div>
        </div>

        <!-- 三、怎么解决 -->
        <div class="detail-section">
          <div class="section-title">怎么解决（处理建议）</div>
          <a-empty
            v-if="actions.length === 0"
            :image="simpleImage"
            description="暂无具体处理建议"
          />
          <ol v-else class="action-list">
            <li v-for="(a, i) in actions" :key="i">{{ a }}</li>
          </ol>
        </div>

        <!-- 四、取证证据 -->
        <div class="detail-section">
          <div class="section-title">
            取证证据（{{ evidenceList.length }} 步）
          </div>
          <a-empty
            v-if="evidenceList.length === 0"
            :image="simpleImage"
            description="该记录无取证明细"
          />
          <div
            v-for="(ev, i) in evidenceList"
            :key="i"
            class="evidence-block"
          >
            <div class="evidence-head">
              <span class="evidence-title">
                {{ i + 1 }}. {{ ev.title }}
              </span>
              <a-tag
                :color="ev.r?.status === 'ok' ? 'green' : 'orange'"
              >
                {{ ev.r?.status ?? '未知' }}
              </a-tag>
              <a-tag v-if="ev.primary" color="blue">主证据</a-tag>
            </div>
            <div v-if="ev.r?.error" class="evidence-err">错误：{{ ev.r.error }}</div>
            <div v-if="ev.r?.missing && ev.r.missing.length" class="evidence-err">
              缺失参数：{{ ev.r.missing.join(', ') }}
            </div>
            <a-table
              v-if="ev.r?.cols && ev.r.rows && ev.r.rows.length"
              size="small"
              :columns="evidenceColumns(ev)"
              :data-source="evidenceData(ev)"
              :pagination="false"
              :scroll="{ x: 'max-content' }"
              row-key="(record, idx) => String(idx)"
            />
          </div>
        </div>

        <!-- 五、AI 大模型诊断（按需，默认关闭，打开才调用并消耗 token） -->
        <div class="detail-section llm-section">
          <div class="llm-head">
            <div class="section-title">AI 大模型诊断</div>
            <a-space>
              <a-switch
                :checked="llmEnabled"
                checked-children="开"
                un-checked-children="关"
                @change="onLlmToggle"
              />
              <span class="llm-hint">默认关闭，打开后由大模型分析这条报错</span>
            </a-space>
          </div>

          <a-spin :spinning="llmLoading" tip="大模型分析中…">
            <a-alert
              v-if="llmError"
              type="error"
              show-icon
              :message="llmError"
              class="llm-error"
            />
            <div v-if="llmAnswer" class="llm-result">
              <div class="llm-root">
                <span class="llm-label">问题判断：</span>{{ llmAnswer.root }}
              </div>
              <div v-if="llmAnswer.actions.length" class="llm-actions">
                <div class="llm-label">处理建议：</div>
                <ol class="action-list">
                  <li
                    v-for="(a, i) in llmAnswer.actions"
                    :key="i"
                  >
                    {{ a }}
                  </li>
                </ol>
              </div>
              <div class="llm-meta">
                <a-tag color="purple">
                  大模型置信度 {{ fmtConf(llmAnswer.confidence) }}
                </a-tag>
                <span v-if="llmAnswer.evidence_note" class="llm-note">
                  依据：{{ llmAnswer.evidence_note }}
                </span>
              </div>
            </div>
          </a-spin>
        </div>
      </template>
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

.view-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.view-tip {
  color: #888;
  font-size: 13px;
}

.link-text {
  color: #1677ff;
  cursor: pointer;
}

.link-text:hover {
  text-decoration: underline;
}

.cell-ellipsis {
  display: block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-section {
  margin-bottom: 20px;
}

.section-title {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 10px;
  padding-left: 8px;
  border-left: 3px solid #1677ff;
}

.verdict {
  margin-top: 8px;
  color: #555;
  font-size: 13px;
}

.action-list {
  margin: 0;
  padding-left: 22px;
  line-height: 1.9;
}

.action-list li {
  margin-bottom: 4px;
}

.evidence-block {
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  padding: 10px 12px;
  margin-bottom: 12px;
}

.evidence-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.evidence-title {
  font-weight: 500;
}

.evidence-err {
  color: #d4380d;
  font-size: 13px;
  margin-bottom: 6px;
}

.llm-section {
  border-top: 1px dashed #e0e0e0;
  padding-top: 16px;
}

.llm-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.llm-head .section-title {
  margin-bottom: 0;
}

.llm-hint {
  color: #999;
  font-size: 12px;
}

.llm-error {
  margin-bottom: 12px;
}

.llm-root {
  margin-bottom: 10px;
  line-height: 1.7;
}

.llm-label {
  font-weight: 600;
  color: #333;
}

.llm-actions {
  margin-bottom: 10px;
}

.llm-meta {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  flex-wrap: wrap;
}

.llm-note {
  color: #888;
  font-size: 12px;
  line-height: 1.6;
  flex: 1;
  min-width: 200px;
}
</style>
