<script setup lang="ts">
import { computed, ref } from 'vue'
import { message } from 'ant-design-vue'

import { batchByItems, diagnose } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import ResultCard from '@/components/ResultCard.vue'
import { SOURCES } from '@/constants/sources'
import { SOURCE_KEYS } from '@/constants/sourceKeys'
import { TEXT_SAMPLES } from '@/constants/textSamples'
import { extractBusinessDate, splitRecords } from '@/utils/textParse'
import type { DiagnosisResult } from '@/types/contract'

const mode = ref<'text' | 'record'>('text')

// ---------- 文本模式：输入状态 ----------
const text = ref('')
const manualDate = ref('')
const multiMode = ref(false)
const escalate = ref(false)
const loading = ref(false)
const errorMsg = ref('')

// 业务日期：手动优先，否则从文本自动提取
const autoDate = computed(() => extractBusinessDate(text.value))
const effectiveDate = computed(() => manualDate.value.trim() || autoDate.value)
const dateSource = computed(() =>
  manualDate.value.trim() ? '手动' : autoDate.value ? '自动识别' : '未识别')
const lineCount = computed(() => splitRecords(text.value).length)

// ---------- 本次会话历史（单条/多条统一展开） ----------
interface HistoryEntry {
  id: number
  text: string
  result: DiagnosisResult | null
  error: string
}
const history = ref<HistoryEntry[]>([])
const activeId = ref<number | null>(null)
let seq = 0

const activeEntry = computed(
  () => history.value.find((h) => h.id === activeId.value) ?? null,
)

function fillSample(sampleText: string) {
  text.value = sampleText
  manualDate.value = ''
  errorMsg.value = ''
}

function clearText() {
  text.value = ''
  manualDate.value = ''
  errorMsg.value = ''
}

function addEntries(
  items: Array<{ text: string; result: DiagnosisResult | null; error: string }>,
) {
  const created: HistoryEntry[] = []
  for (const it of items) {
    seq += 1
    const entry: HistoryEntry = { id: seq, ...it }
    history.value.unshift(entry)
    created.push(entry)
  }
  activeId.value = created[0].id
}

async function run() {
  errorMsg.value = ''
  const lines = (multiMode.value ? splitRecords(text.value) : [text.value.trim()])
    .map((s) => s.trim())
    .filter(Boolean)
  if (!lines.length) {
    errorMsg.value = '请输入报错文本'
    return
  }
  loading.value = true
  try {
    if (lines.length === 1) {
      const res = await diagnose({
        text: lines[0], ldate: effectiveDate.value, escalate: escalate.value,
      })
      addEntries([{ text: lines[0], result: res, error: '' }])
    } else {
      const payloads = lines.map((t) => ({
        text: t, ldate: effectiveDate.value, escalate: escalate.value,
      }))
      const res = await batchByItems(payloads)
      addEntries(
        res.results.map((bi, i) => ({
          text: lines[i], result: bi.result ?? null, error: bi.error ?? '',
        })),
      )
    }
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError
        ? `请求失败（${e.status}）：${e.message}`
        : '请求异常，请检查输入'
  } finally {
    loading.value = false
  }
}

async function copyResult() {
  const e = activeEntry.value
  if (!e) return
  const a = e.result?.answer
  const txt = [
    '报错：' + e.text,
    '根因：' + (a?.root ?? ''),
    '建议：' + (a?.actions?.join('；') ?? ''),
    '置信度：' + (a?.confidence ?? ''),
  ].join('\n')
  try {
    await navigator.clipboard.writeText(txt)
    message.success('已复制当前结论')
  } catch {
    message.error('复制失败，请手动选择文本')
  }
}

function exportHistory() {
  const blob = new Blob([JSON.stringify(history.value, null, 2)], {
    type: 'application/json',
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = '文本诊断记录.json'
  a.click()
  URL.revokeObjectURL(url)
}

function entryTitle(e: HistoryEntry): string {
  return e.result?.rule_res?.type?.title
    ?? e.result?.answer?.root
    ?? (e.error ? '诊断异常' : '未识别')
}

// ---------- 来源取数模式（保留原有逻辑） ----------
const source = ref(SOURCES[0].id)
const date = ref('')
const keyText = ref('')
const keyMeta = computed(() => SOURCE_KEYS[source.value])

function fillKeySample() {
  keyText.value = JSON.stringify(keyMeta.value.sample, null, 2)
}
</script>

<template>
  <a-card>
    <a-radio-group v-model:value="mode" class="mode-group">
      <a-radio-button value="text">自由文本</a-radio-button>
      <a-radio-button value="record">来源取数</a-radio-button>
    </a-radio-group>

    <!-- ============ 自由文本：左右分栏 ============ -->
    <a-row v-if="mode === 'text'" :gutter="16">
      <!-- 左：输入区 -->
      <a-col :span="10">
        <a-form layout="vertical">
          <a-form-item>
            <template #label>
              <a-space>
                <span>报错文本</span>
                <a-tag>{{ text.length }} 字符</a-tag>
                <a-tag v-if="multiMode">{{ lineCount }} 条</a-tag>
              </a-space>
            </template>
            <a-textarea
              v-model:value="text"
              :rows="12"
              placeholder="粘贴单条报错；多条模式下按行或空行分隔"
            />
            <div class="input-actions">
              <a-button size="small" @click="clearText">清空</a-button>
            </div>
          </a-form-item>

          <a-form-item label="常用示例（点击填充）">
            <div class="sample-list">
              <a-button
                v-for="s in TEXT_SAMPLES"
                :key="s.id"
                size="small"
                class="sample-btn"
                @click="fillSample(s.text)"
              >
                {{ s.label }}
              </a-button>
            </div>
            <a-alert
              v-if="text"
              type="info"
              show-icon
              class="hint-block"
              :message="TEXT_SAMPLES.find((x) => x.text === text)?.hint || ''"
            />
          </a-form-item>

          <a-form-item label="业务日期 YYYYMMDD">
            <a-input
              v-model:value="manualDate"
              :placeholder="autoDate || '留空则自动识别，识别不到归当天'"
            />
            <p class="hint">当前日期：{{ effectiveDate || '（空）' }}（{{ dateSource }}）</p>
          </a-form-item>

          <a-form-item>
            <a-space wrap>
              <a-checkbox v-model:checked="multiMode">多条模式</a-checkbox>
              <a-checkbox v-model:checked="escalate">
                允许 LLM 升级（受部署开关约束）
              </a-checkbox>
            </a-space>
          </a-form-item>

          <a-button
            type="primary"
            block
            :loading="loading"
            @click="run"
          >
            开始诊断
          </a-button>
        </a-form>
      </a-col>

      <!-- 右：结果区 -->
      <a-col :span="14">
        <a-alert
          v-if="errorMsg"
          type="error"
          show-icon
          :message="errorMsg"
          class="hint-block"
        />
        <a-empty
          v-if="!history.length"
          description="诊断结果将展示在这里"
          style="padding: 60px 0"
        />
        <template v-else>
          <div class="result-toolbar">
            <span class="toolbar-title">本次记录（{{ history.length }}）</span>
            <a-space>
              <a-button size="small" @click="copyResult">复制结论</a-button>
              <a-button size="small" @click="exportHistory">导出 JSON</a-button>
            </a-space>
          </div>
          <div class="history-list">
            <div
              v-for="h in history"
              :key="h.id"
              class="history-item"
              :class="{ active: h.id === activeId }"
              @click="activeId = h.id"
            >
              <span class="history-no">#{{ h.id }}</span>
              <span class="history-title">{{ entryTitle(h) }}</span>
              <a-tag v-if="h.result?.answer?.confidence != null" color="blue">
                {{ Number(h.result!.answer!.confidence).toFixed(2) }}
              </a-tag>
            </div>
          </div>
          <div v-if="activeEntry" class="result-detail">
            <a-alert
              v-if="activeEntry.error"
              type="warning"
              show-icon
              :message="'该条诊断异常：' + activeEntry.error"
              class="hint-block"
            />
            <ResultCard
              v-if="activeEntry.result"
              :result="activeEntry.result"
            />
          </div>
        </template>
      </a-col>
    </a-row>

    <!-- ============ 来源取数（保留原表单） ============ -->
    <a-row v-else :gutter="16">
      <a-col :span="12">
        <a-form layout="vertical">
          <a-form-item label="错误来源">
            <a-select v-model:value="source">
              <a-select-option
                v-for="s in SOURCES"
                :key="s.id"
                :value="s.id"
              >
                {{ s.label }}（{{ s.id }}）
              </a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="业务日期 YYYYMMDD">
            <a-input v-model:value="date" />
          </a-form-item>
          <a-form-item>
            <template #label>
              <a-space>
                <span>主键 JSON（必填：{{ keyMeta.requiredKeys.join('、') }}）</span>
                <a-button type="link" size="small" @click="fillKeySample">
                  填充示例
                </a-button>
              </a-space>
            </template>
            <a-textarea v-model:value="keyText" :rows="4" />
            <p class="hint">
              日期列 {{ keyMeta.dateCol }} 由上方业务日期自动补全，无需写入。
            </p>
          </a-form-item>
          <a-button type="primary" :loading="loading" @click="run">
            开始诊断
          </a-button>
        </a-form>
      </a-col>
    </a-row>
  </a-card>
</template>

<style scoped>
.mode-group {
  margin-bottom: 16px;
}

.input-actions {
  margin-top: 6px;
  text-align: right;
}

.sample-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.sample-btn {
  margin: 0;
}

.hint {
  margin-top: 4px;
  color: #888;
  font-size: 12px;
}

.hint-block {
  margin-top: 10px;
}

.result-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.toolbar-title {
  font-weight: 600;
}

.history-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  margin-bottom: 14px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item.active {
  background: #e6f4ff;
}

.history-no {
  color: #999;
  font-size: 12px;
  flex: none;
}

.history-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
