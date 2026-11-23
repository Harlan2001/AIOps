<script setup lang="ts">
import { computed } from 'vue'
import { message } from 'ant-design-vue'
import { CopyOutlined } from '@ant-design/icons-vue'

import StatusTag from '@/components/StatusTag.vue'
import type { DiagnosisResult, EvidenceRow } from '@/types/contract'
import { formatBusinessDate, formatConfidence } from '@/utils/diagnosis'
import { labelNull } from '@/utils/label'

const props = withDefaults(defineProps<{
  result: DiagnosisResult
  showInput?: boolean
}>(), {
  showInput: true,
})

const ruleRes = computed(() => props.result.rule_res)
const answer = computed(() => props.result.answer)
const evidence = computed(() => ruleRes.value?.evidence ?? [])
const missingParams = computed(() => ruleRes.value?.missing_params ?? [])
const sqlErrors = computed(() => ruleRes.value?.sql_errors ?? [])
const hasEvidenceDegrade = computed(
  () => missingParams.value.length > 0 || sqlErrors.value.length > 0,
)
const kbCards = computed(() => props.result.kb_card?.cards ?? [])
const isFallback = computed(() => !props.result.escalated && props.result.source.includes('兜底'))
const sourceLabel = computed(() => {
  if (props.result.escalated) return '大模型升级结论'
  return isFallback.value ? '规则兜底结论' : '规则诊断结论'
})
const sourceTone = computed(() => {
  if (props.result.escalated) return 'processing' as const
  return isFallback.value ? 'warning' as const : 'neutral' as const
})
const confidencePercent = computed(() => {
  const value = answer.value?.confidence
  return value !== null && value !== undefined && value >= 0 && value <= 1
    ? Math.round(value * 100)
    : 0
})
const secondaryText = computed(() => {
  const rows = answer.value?.secondary ?? []
  return rows.length ? JSON.stringify(rows, null, 2) : ''
})

function evidenceColumns(cols?: string[]) {
  return (cols ?? []).map((col) => ({ title: col, dataIndex: col, key: col }))
}

function evidenceRows(cols?: string[], rows?: unknown[][]) {
  const columns = cols ?? []
  return (rows ?? []).map((row, rowIndex) => {
    const values = Array.isArray(row) ? row : []
    return {
      ...Object.fromEntries(columns.map((col, index) => [col, values[index] ?? '—'])),
      __index: String(rowIndex),
    }
  })
}

function evidenceStatus(ev: EvidenceRow) {
  if (ev.r?.status === 'ok') return { label: '已完成', tone: 'success' as const }
  if (ev.r?.status === 'error') return { label: '取证失败', tone: 'error' as const }
  if (ev.r?.status === 'missing_params') return { label: '缺少参数', tone: 'warning' as const }
  return { label: ev.r?.status || '状态未知', tone: 'neutral' as const }
}

async function writeClipboard(value: string) {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(value)
      return
    } catch {
      // 内网 HTTP 或浏览器拒绝授权时，继续尝试兼容复制方式。
    }
  }
  const textarea = document.createElement('textarea')
  textarea.value = value
  textarea.readOnly = true
  textarea.setAttribute('aria-hidden', 'true')
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.select()
  try {
    if (!document.execCommand('copy')) throw new Error('copy command failed')
  } finally {
    textarea.remove()
  }
}

async function copyConclusion() {
  const lines = [
    `诊断结论：${answer.value?.root || '暂无明确根因'}`,
    `置信度：${formatConfidence(answer.value?.confidence)}`,
    `结论来源：${props.result.source || sourceLabel.value}`,
    '处理建议：',
    ...(answer.value?.actions.length
      ? answer.value.actions.map((action, index) => `${index + 1}. ${action}`)
      : ['暂无具体处理建议，请结合证据人工确认。']),
  ]
  try {
    await writeClipboard(lines.join('\n'))
    message.success('诊断结论已复制')
  } catch {
    message.error('复制失败，请检查浏览器剪贴板权限')
  }
}
</script>

<template>
  <article class="diagnosis-report" aria-live="polite">
    <section class="report-hero" aria-labelledby="diagnosis-root">
      <div class="hero-topline">
        <div class="report-tags">
          <StatusTag :label="sourceLabel" :tone="sourceTone" />
          <StatusTag v-if="ruleRes?.class" :status="ruleRes.class" />
          <a-tag v-if="ruleRes?.type?.title" color="blue">{{ ruleRes.type.title }}</a-tag>
        </div>
        <a-button type="text" size="small" @click="copyConclusion">
          <CopyOutlined /> 复制结论
        </a-button>
      </div>
      <div class="hero-content">
        <div class="root-cause">
          <span class="section-eyebrow">问题判断</span>
          <h2 id="diagnosis-root">{{ answer?.root || '未形成明确根因，请结合原始报错与证据人工确认' }}</h2>
          <p v-if="ruleRes?.verdict" class="verdict">{{ ruleRes.verdict }}</p>
        </div>
        <div v-if="answer?.confidence !== null && answer?.confidence !== undefined" class="confidence">
          <span>诊断置信度</span>
          <strong>{{ formatConfidence(answer.confidence) }}</strong>
          <a-progress
            :percent="confidencePercent"
            :show-info="false"
            stroke-color="#2a78d6"
            trail-color="#e8eef6"
            :stroke-width="6"
          />
        </div>
      </div>
    </section>

    <a-alert
      v-if="isFallback"
      type="warning"
      show-icon
      message="本次未实际形成大模型升级结论"
      :description="`${result.source}。请按规则诊断结果和证据谨慎处理。`"
      class="report-alert"
    />
    <a-alert
      v-if="hasEvidenceDegrade"
      type="warning"
      show-icon
      message="部分取证未成功，结论可能基于不完整证据"
      class="report-alert"
    >
      <template #description>
        <div v-for="(item, index) in missingParams" :key="`missing-${index}`">
          步骤 {{ item.step || '未知' }}：缺少参数 {{ (item.missing ?? []).join('、') || '未知' }}
        </div>
        <div v-for="(item, index) in sqlErrors" :key="`sql-${index}`">
          步骤 {{ item.step || '未知' }}：{{ item.error || '取证 SQL 执行失败' }}
        </div>
      </template>
    </a-alert>

    <section class="report-section" aria-labelledby="diagnosis-actions">
      <div class="section-heading">
        <div>
          <span class="section-eyebrow">下一步</span>
          <h3 id="diagnosis-actions">建议这样处理</h3>
        </div>
        <span v-if="answer?.actions.length" class="action-count">{{ answer.actions.length }} 项建议</span>
      </div>
      <ol v-if="answer?.actions.length" class="action-list">
        <li v-for="(action, index) in answer.actions" :key="index">
          <span class="action-number">{{ index + 1 }}</span>
          <span>{{ action }}</span>
        </li>
      </ol>
      <a-empty v-else description="暂无规则处置动作，请结合证据人工确认" />
      <p v-if="answer?.evidence_note" class="evidence-note">
        <strong>判断依据：</strong>{{ answer.evidence_note }}
      </p>
    </section>

    <section class="report-section">
      <div class="section-heading">
        <div>
          <span class="section-eyebrow">可追溯</span>
          <h3>取证证据</h3>
        </div>
        <span class="action-count">{{ evidence.length }} 步</span>
      </div>
      <a-collapse v-if="evidence.length" ghost class="evidence-collapse">
        <a-collapse-panel v-for="(item, index) in evidence" :key="item.id || index">
          <template #header>
            <div class="evidence-header">
              <span>{{ index + 1 }}. {{ item.title || item.id || '取证步骤' }}</span>
              <a-tag v-if="item.primary" color="blue">主证据</a-tag>
              <StatusTag v-bind="evidenceStatus(item)" />
            </div>
          </template>
          <a-alert
            v-if="item.r?.status === 'missing_params'"
            type="warning"
            :message="`缺少参数：${(item.r.missing ?? []).join('、') || '未知'}，本步骤已跳过`"
          />
          <a-alert
            v-else-if="item.r?.status === 'error'"
            type="error"
            :message="item.r.error || '本步骤取证失败'"
          />
          <a-table
            v-else-if="item.r?.rows?.length"
            size="small"
            :columns="evidenceColumns(item.r.cols)"
            :data-source="evidenceRows(item.r.cols, item.r.rows)"
            :pagination="false"
            :scroll="{ x: 'max-content' }"
            row-key="__index"
          />
          <a-empty v-else description="本步骤没有返回数据行" />
        </a-collapse-panel>
      </a-collapse>
      <a-empty v-else description="该结果没有取证明细" />
    </section>

    <a-collapse ghost class="secondary-collapse">
      <a-collapse-panel v-if="secondaryText" key="secondary" header="查看次要判断">
        <pre class="raw-details">{{ secondaryText }}</pre>
      </a-collapse-panel>
      <a-collapse-panel v-if="kbCards.length" key="knowledge" :header="`知识库机制卡（${kbCards.length}）`">
        <div class="knowledge-list">
          <section v-for="(card, index) in kbCards" :key="index" class="knowledge-card">
            <h4>{{ card.title || '机制说明' }}</h4>
            <p>{{ (card.required_facts ?? []).join('；') || '暂无机制要点' }}</p>
          </section>
        </div>
      </a-collapse-panel>
      <a-collapse-panel v-if="showInput || result.report" key="metadata" header="原始输入与诊断元数据">
        <dl class="report-metadata">
          <div><dt>业务日期</dt><dd>{{ formatBusinessDate(result.ldate) }}</dd></div>
          <div><dt>调用位置</dt><dd>{{ result.loc || '—' }}</dd></div>
          <div><dt>问题分类</dt><dd>{{ labelNull(ruleRes?.class) }}</dd></div>
          <div><dt>问题类型</dt><dd>{{ ruleRes?.type?.title || labelNull(ruleRes?.type?.id) }}</dd></div>
          <div class="metadata-wide"><dt>结论来源</dt><dd>{{ result.source || sourceLabel }}</dd></div>
          <div v-if="showInput" class="metadata-wide"><dt>原始报错</dt><dd class="raw-input">{{ result.text || '—' }}</dd></div>
          <div v-if="result.report" class="metadata-wide"><dt>文本报告</dt><dd><pre class="raw-details">{{ result.report }}</pre></dd></div>
        </dl>
      </a-collapse-panel>
    </a-collapse>
  </article>
</template>

<style scoped>
.diagnosis-report {
  min-width: 0;
  color: var(--text-primary);
}

.report-hero {
  padding: 22px;
  background: linear-gradient(135deg, #f5f9ff 0%, #fbfdff 72%);
  border: 1px solid #dce9f8;
  border-radius: 12px;
}

.hero-topline,
.hero-content,
.section-heading,
.evidence-header {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.report-tags {
  display: flex;
  gap: 6px;
  align-items: center;
  flex-wrap: wrap;
}

.hero-content {
  align-items: flex-end;
  margin-top: 20px;
}

.root-cause {
  min-width: 0;
  flex: 1;
}

.section-eyebrow {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 650;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h2 {
  max-width: 760px;
  margin-bottom: 8px;
  font-size: clamp(18px, 2vw, 23px);
  font-weight: 650;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.verdict {
  margin-bottom: 0;
  color: var(--text-secondary);
  line-height: 1.65;
}

.confidence {
  width: 116px;
  flex: none;
  color: var(--text-secondary);
  font-size: 12px;
}

.confidence strong {
  display: block;
  margin: 4px 0 8px;
  color: var(--text-primary);
  font-size: 26px;
  line-height: 1;
}

.report-alert {
  margin-top: 16px;
}

.report-section {
  padding: 24px 2px;
  border-bottom: 1px solid var(--border-soft);
}

.section-heading {
  margin-bottom: 16px;
}

.section-heading h3 {
  margin-bottom: 0;
  font-size: 17px;
  font-weight: 650;
}

.action-count {
  color: var(--text-muted);
  font-size: 12px;
}

.action-list {
  display: flex;
  margin: 0;
  padding: 0;
  flex-direction: column;
  gap: 10px;
  list-style: none;
}

.action-list li {
  display: flex;
  padding: 13px 14px;
  gap: 12px;
  align-items: flex-start;
  background: var(--surface-subtle);
  border: 1px solid var(--border-soft);
  border-radius: 9px;
  line-height: 1.65;
}

.action-number {
  display: inline-flex;
  width: 23px;
  height: 23px;
  flex: none;
  align-items: center;
  justify-content: center;
  color: var(--brand-hover);
  background: var(--brand-soft);
  border-radius: 7px;
  font-size: 12px;
  font-weight: 650;
}

.evidence-note {
  margin: 16px 0 0;
  padding: 12px 14px;
  color: var(--text-secondary);
  background: #fafbfd;
  border-left: 3px solid #b8c8db;
  line-height: 1.65;
}

.evidence-collapse,
.secondary-collapse {
  margin-inline: -12px;
}

.evidence-header {
  justify-content: flex-start;
  flex-wrap: wrap;
}

.evidence-header > span:first-child {
  min-width: 160px;
  flex: 1;
}

.secondary-collapse {
  margin-top: 12px;
}

.knowledge-list {
  display: grid;
  gap: 10px;
}

.knowledge-card {
  padding: 14px;
  background: var(--surface-subtle);
  border-radius: 8px;
}

.knowledge-card h4 {
  margin-bottom: 6px;
}

.knowledge-card p {
  margin-bottom: 0;
  color: var(--text-secondary);
  line-height: 1.65;
}

.report-metadata {
  display: grid;
  margin: 0;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.report-metadata > div {
  min-width: 0;
}

.report-metadata dt {
  margin-bottom: 5px;
  color: var(--text-muted);
  font-size: 12px;
}

.report-metadata dd {
  margin: 0;
  overflow-wrap: anywhere;
}

.metadata-wide {
  grid-column: 1 / -1;
}

.raw-input,
.raw-details {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.raw-details {
  max-width: 100%;
  margin: 0;
  padding: 12px;
  overflow: auto;
  color: var(--text-secondary);
  background: var(--surface-subtle);
  border-radius: 8px;
  font: 12px/1.6 ui-monospace, SFMono-Regular, Consolas, monospace;
}

@media (max-width: 640px) {
  .report-hero {
    padding: 18px;
  }

  .hero-topline {
    align-items: flex-start;
  }

  .hero-content {
    align-items: flex-start;
    flex-direction: column;
  }

  .confidence {
    width: 100%;
  }

  .report-metadata {
    grid-template-columns: minmax(0, 1fr);
  }

  .metadata-wide {
    grid-column: auto;
  }

  .evidence-header :deep(.ant-tag) {
    margin-top: 4px;
  }
}
</style>
