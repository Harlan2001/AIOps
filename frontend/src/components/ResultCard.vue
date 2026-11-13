<script setup lang="ts">
import { computed } from 'vue'

import type { DiagnosisResult } from '@/types/contract'

const props = defineProps<{ result: DiagnosisResult }>()

const ruleRes = computed(() => props.result.rule_res)
const answer = computed(() => props.result.answer)
const evidence = computed(() => ruleRes.value?.evidence ?? [])
const missingParams = computed(() => ruleRes.value?.missing_params ?? [])
const sqlErrors = computed(() => ruleRes.value?.sql_errors ?? [])
const hasDegrade = computed(
  () => missingParams.value.length > 0 || sqlErrors.value.length > 0,
)
const kbCards = computed(() => props.result.kb_card?.cards ?? [])

function evidenceColumns(cols?: string[]) {
  return (cols ?? []).map((c) => ({ title: c, dataIndex: c, key: c }))
}

// 证据行无唯一业务字段，用行下标生成稳定且不重复的 key。
function evidenceRowKey(
  _record: Record<string, unknown>,
  idx: number,
): string {
  return String(idx)
}

// 后端 rows 是按 cols 顺序对齐的数组，Ant Table 需要对象，按列名映射为键值对象。
function evidenceRows(
  cols?: string[],
  rows?: unknown[][],
): Array<Record<string, unknown>> {
  const c = cols ?? []
  return (rows ?? []).map((row) => {
    const obj: Record<string, unknown> = {}
    c.forEach((col, i) => {
      obj[col] = row[i]
    })
    return obj
  })
}
</script>

<template>
  <a-descriptions :column="2" bordered size="small" class="meta-desc">
    <a-descriptions-item label="报错文本" :span="2">
      {{ result.text }}
    </a-descriptions-item>
    <a-descriptions-item label="业务日期">
      {{ result.ldate || '-' }}
    </a-descriptions-item>
    <a-descriptions-item label="位置">{{ result.loc || '-' }}</a-descriptions-item>
    <a-descriptions-item v-if="ruleRes?.type" label="问题类型" :span="2">
      {{ ruleRes.type.title }}（{{ ruleRes.type.id }}）
    </a-descriptions-item>
    <a-descriptions-item label="结论来源" :span="2">
      {{ result.source }}
      <a-tag v-if="result.escalated" color="purple" class="tag">已升级</a-tag>
    </a-descriptions-item>
  </a-descriptions>

  <a-alert
    v-if="hasDegrade"
    type="warning"
    show-icon
    class="block"
    message="部分取证未成功，结论可能基于不完整证据，请谨慎采信"
  >
    <template #description>
      <div v-for="(m, i) in missingParams" :key="'m' + i">
        步骤 {{ m.step }}：缺少参数 {{ (m.missing ?? []).join('、') }}
      </div>
      <div v-for="(e, i) in sqlErrors" :key="'e' + i">
        步骤 {{ e.step }}：{{ e.error }}
      </div>
    </template>
  </a-alert>

  <div class="block">
    <h4>问题是什么</h4>
    <p>{{ answer?.root }}</p>
    <a-tag color="blue">置信度 {{ answer?.confidence }}</a-tag>
    <p v-if="answer?.evidence_note" class="note">{{ answer.evidence_note }}</p>
  </div>

  <div class="block">
    <h4>怎么解决</h4>
    <ol v-if="answer && answer.actions.length">
      <li v-for="(a, i) in answer.actions" :key="i">{{ a }}</li>
    </ol>
    <a-empty v-else description="无规则处置动作，请按上述方向人工确认" />
  </div>

  <div v-if="evidence.length" class="block">
    <h4>取证证据</h4>
    <a-collapse>
      <a-collapse-panel
        v-for="(ev, i) in evidence"
        :key="i"
        :header="ev.title"
      >
        <template v-if="ev.r?.status === 'missing_params'">
          缺少参数 {{ (ev.r.missing ?? []).join('、') }}，已跳过
        </template>
        <template v-else-if="ev.r?.status === 'error'">
          取证失败：{{ ev.r.error }}
        </template>
        <template v-else>
          <a-table
            size="small"
            :columns="evidenceColumns(ev.r?.cols)"
            :data-source="evidenceRows(ev.r?.cols, ev.r?.rows)"
            :pagination="false"
            :row-key="evidenceRowKey"
          />
        </template>
      </a-collapse-panel>
    </a-collapse>
  </div>

  <div v-if="kbCards.length" class="block">
    <h4>知识库机制卡</h4>
    <a-card v-for="(c, i) in kbCards" :key="i" size="small" class="kb-card">
      <p><strong>{{ c.title }}</strong></p>
      <p class="note">机制要点：{{ (c.required_facts ?? []).join('；') }}</p>
    </a-card>
  </div>
</template>

<style scoped>
.meta-desc {
  margin-bottom: 16px;
}

.block {
  margin-top: 16px;
}

.block h4 {
  margin-bottom: 8px;
}

.tag {
  margin-left: 8px;
}

.note {
  color: #888;
  font-size: 13px;
}

.kb-card {
  margin-bottom: 8px;
}
</style>
