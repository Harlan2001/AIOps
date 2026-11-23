<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { ClearOutlined, ExperimentOutlined } from '@ant-design/icons-vue'

import { diagnose } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import PageHeader from '@/components/PageHeader.vue'
import ResultCard from '@/components/ResultCard.vue'
import { DIAGNOSE_SOURCES } from '@/constants/sources'
import { SOURCE_KEYS } from '@/constants/sourceKeys'
import type { DiagnosisResult } from '@/types/contract'

const mode = ref<'text' | 'record'>('text')
const text = ref('')
const ldate = ref('')
const source = ref(DIAGNOSE_SOURCES[0].id)
const date = ref('')
const keyMode = ref<'fields' | 'json'>('fields')
const keyValues = reactive<Record<string, string>>({})
const keyText = ref('')
const escalate = ref(false)
const loading = ref(false)
const errorMsg = ref('')
const result = ref<DiagnosisResult | null>(null)
const errors = reactive<Record<string, string>>({})
const resultSection = ref<HTMLElement | null>(null)
let generation = 0

const keyMeta = computed(() => SOURCE_KEYS[source.value])
const keyLabels: Record<string, string> = {
  trader_no: '交易员代码',
  local_no: '本地委托号',
  purpose_code: '交易用途',
  seq_no: '序号',
  alarm_type: '报警类型',
  member_id: '会员代码',
  flow_code: '流程代码',
  exch_code: '交易所',
}

function clearErrors() {
  Object.keys(errors).forEach((key) => delete errors[key])
}

watch(source, () => {
  Object.keys(keyValues).forEach((key) => delete keyValues[key])
  keyText.value = ''
  delete errors.key
})

watch(mode, clearErrors)

function fillSample() {
  if (keyMode.value === 'json') {
    keyText.value = JSON.stringify(keyMeta.value.sample, null, 2)
  } else {
    Object.entries(keyMeta.value.sample).forEach(([key, value]) => {
      keyValues[key] = value
    })
  }
  delete errors.key
}

function validDate(value: string) {
  const match = /^(\d{4})(\d{2})(\d{2})$/.exec(value)
  if (!match) return false
  const year = Number(match[1])
  const month = Number(match[2])
  const day = Number(match[3])
  const parsed = new Date(Date.UTC(year, month - 1, day))
  return parsed.getUTCFullYear() === year && parsed.getUTCMonth() === month - 1 && parsed.getUTCDate() === day
}

function buildKey(): Record<string, unknown> | null {
  if (keyMode.value === 'fields') {
    return Object.fromEntries(keyMeta.value.requiredKeys.map((key) => [key, keyValues[key]?.trim() ?? '']))
  }
  try {
    const parsed: unknown = keyText.value ? JSON.parse(keyText.value) : {}
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      errors.key = '主键 JSON 需要是对象，例如 {"seq_no":"1"}'
      return null
    }
    return parsed as Record<string, unknown>
  } catch {
    errors.key = '主键 JSON 格式错误，请检查引号、逗号和括号'
    return null
  }
}

function validate() {
  clearErrors()
  if (mode.value === 'text') {
    if (!text.value.trim()) errors.text = '请粘贴需要诊断的报错文本'
    if (ldate.value && !validDate(ldate.value)) errors.ldate = '请选择有效的业务日期'
    return !Object.keys(errors).length
  }

  if (!date.value || !validDate(date.value)) errors.date = '请选择有效的业务日期'
  const key = buildKey()
  if (!key) return false
  const missing = keyMeta.value.requiredKeys.filter(
    (field) => key[field] === undefined || key[field] === null || String(key[field]).trim() === '',
  )
  if (missing.length) errors.key = `请补充：${missing.map((field) => keyLabels[field] ?? field).join('、')}`
  return !Object.keys(errors).length
}

async function scrollToResult() {
  await nextTick()
  if (window.matchMedia('(max-width: 1199px)').matches) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    resultSection.value?.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' })
  }
}

async function run() {
  if (!validate()) return
  const requestGeneration = ++generation
  loading.value = true
  errorMsg.value = ''
  try {
    let response: DiagnosisResult
    if (mode.value === 'text') {
      response = await diagnose({
        text: text.value.trim(),
        ldate: ldate.value || undefined,
        escalate: escalate.value,
      })
    } else {
      response = await diagnose({
        record: { source: source.value, date: date.value, key: buildKey() ?? {} },
        escalate: escalate.value,
      })
    }
    if (requestGeneration !== generation) return
    result.value = response
    await scrollToResult()
  } catch (error) {
    if (requestGeneration !== generation) return
    if (error instanceof ApiError) {
      errorMsg.value = error.status === 409
        ? '当前部署未开启大模型升级。可关闭高级选项中的升级开关后重试。'
        : error.status === 0
          ? `无法连接诊断服务：${error.message}`
          : `诊断请求未完成（${error.status}）：${error.message}`
    } else {
      errorMsg.value = '诊断请求异常，请检查输入后重试'
    }
    await scrollToResult()
  } finally {
    if (requestGeneration === generation) loading.value = false
  }
}

function clearForm() {
  generation += 1
  loading.value = false
  text.value = ''
  ldate.value = ''
  date.value = ''
  keyText.value = ''
  Object.keys(keyValues).forEach((key) => delete keyValues[key])
  escalate.value = false
  result.value = null
  errorMsg.value = ''
  clearErrors()
}
</script>

<template>
  <div class="page-shell">
    <PageHeader
      title="单条诊断"
      description="粘贴一段报错，或按来源定位原始记录。默认使用规则引擎，结论、处理建议和取证过程会一起呈现。"
    >
      <template #extra>
        <a-button @click="clearForm"><ClearOutlined /> 清空</a-button>
      </template>
    </PageHeader>

    <div class="diagnose-workspace">
      <a-card class="input-card" :bordered="true">
        <template #title><span class="card-title"><span class="step">1</span>诊断输入</span></template>
        <a-radio-group v-model:value="mode" class="mode-group" option-type="button" button-style="solid">
          <a-radio-button value="text">粘贴报错</a-radio-button>
          <a-radio-button value="record">从来源取数</a-radio-button>
        </a-radio-group>

        <a-form layout="vertical" @submit.prevent="run">
          <template v-if="mode === 'text'">
            <a-form-item label="报错文本" required :validate-status="errors.text ? 'error' : ''" :help="errors.text">
              <a-textarea
                v-model:value="text"
                :rows="8"
                placeholder="例如：ORA-00001: unique constraint ..."
                @input="delete errors.text"
              />
              <p class="field-hint">可粘贴完整错误栈，原始文本只用于本次诊断，不会写入浏览器存储。</p>
            </a-form-item>
            <a-form-item label="业务日期（可选）" :validate-status="errors.ldate ? 'error' : ''" :help="errors.ldate">
              <a-date-picker
                v-model:value="ldate"
                value-format="YYYYMMDD"
                format="YYYY-MM-DD"
                placeholder="选择业务日期"
                class="full-width"
              />
            </a-form-item>
          </template>

          <template v-else>
            <a-form-item label="错误来源" required>
              <a-select v-model:value="source" :options="DIAGNOSE_SOURCES.map((item) => ({ value: item.id, label: `${item.label}（${item.id}）` }))" />
              <p class="field-hint">这里仅展示支持单条取数的历史错误来源。</p>
            </a-form-item>
            <a-form-item label="业务日期" required :validate-status="errors.date ? 'error' : ''" :help="errors.date">
              <a-date-picker
                v-model:value="date"
                value-format="YYYYMMDD"
                format="YYYY-MM-DD"
                placeholder="选择记录日期"
                class="full-width"
              />
            </a-form-item>

            <div class="key-heading">
              <span>记录主键</span>
              <a-radio-group v-model:value="keyMode" size="small">
                <a-radio-button value="fields">逐项填写</a-radio-button>
                <a-radio-button value="json">JSON</a-radio-button>
              </a-radio-group>
            </div>
            <a-form-item :validate-status="errors.key ? 'error' : ''" :help="errors.key">
              <div v-if="keyMode === 'fields'" class="key-fields">
                <label v-for="field in keyMeta.requiredKeys" :key="field" class="key-field">
                  <span>{{ keyLabels[field] ?? field }} <code>{{ field }}</code></span>
                  <a-input
                    v-model:value="keyValues[field]"
                    :placeholder="keyMeta.sample[field] ? `示例：${keyMeta.sample[field]}` : `请输入 ${field}`"
                    @input="delete errors.key"
                  />
                </label>
              </div>
              <a-textarea
                v-else
                v-model:value="keyText"
                :rows="6"
                placeholder='{"trader_no":"trader1","local_no":"0001"}'
                @input="delete errors.key"
              />
              <div class="key-help">
                <span>日期字段 {{ keyMeta.dateCol }} 由上方日期自动补全</span>
                <a-button type="link" size="small" @click="fillSample">填充示例</a-button>
              </div>
            </a-form-item>
          </template>

          <a-collapse ghost class="advanced-options">
            <a-collapse-panel key="advanced" header="高级诊断选项">
              <a-checkbox v-model:checked="escalate">允许使用大模型升级诊断</a-checkbox>
              <p class="field-hint">
                默认仅运行规则诊断。升级可能耗时更长，并取决于部署方是否允许；不可用时会明确标注规则兜底，不会静默伪装成 AI 结论。
              </p>
            </a-collapse-panel>
          </a-collapse>

          <a-button type="primary" size="large" html-type="submit" :loading="loading" block>
            <ExperimentOutlined /> {{ result ? '重新诊断' : '开始诊断' }}
          </a-button>
        </a-form>
      </a-card>

      <section id="diagnosis-result" ref="resultSection" class="result-panel">
        <a-card :bordered="true">
          <template #title>
            <span class="card-title"><span class="step">2</span>诊断报告</span>
          </template>
          <template v-if="loading && !result">
            <a-alert type="info" show-icon message="正在执行规则识别与查库取证，请稍候" class="loading-notice" />
            <a-skeleton active :paragraph="{ rows: 9 }" />
          </template>
          <template v-else>
            <a-alert
              v-if="loading && result"
              type="info"
              show-icon
              message="正在生成新诊断，下方暂时保留上次结果"
              class="loading-notice"
            />
            <a-alert
              v-if="errorMsg"
              type="error"
              show-icon
              closable
              :message="errorMsg"
              class="error-notice"
              @close="errorMsg = ''"
            />
            <div v-if="result" :class="{ 'stale-result': loading }">
              <ResultCard :result="result" />
            </div>
            <div v-else-if="!errorMsg" class="result-empty">
              <a-empty description="">
                <template #description>
                  <h3>诊断结果会显示在这里</h3>
                  <p>完成左侧输入后开始诊断，你将看到根因、处理建议和每一步取证依据。</p>
                </template>
              </a-empty>
            </div>
          </template>
        </a-card>
      </section>
    </div>
  </div>
</template>

<style scoped>
.diagnose-workspace {
  display: grid;
  grid-template-columns: minmax(340px, 410px) minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.card-title {
  display: inline-flex;
  gap: 10px;
  align-items: center;
}

.step {
  display: inline-flex;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
  color: var(--brand-hover);
  background: var(--brand-soft);
  border-radius: 7px;
  font-size: 12px;
}

.mode-group {
  display: flex;
  width: 100%;
  margin-bottom: 24px;
}

.mode-group :deep(.ant-radio-button-wrapper) {
  flex: 1;
  text-align: center;
}

.full-width {
  width: 100%;
}

.field-hint {
  margin: 8px 0 0;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.6;
}

.key-heading {
  display: flex;
  margin-bottom: 12px;
  align-items: center;
  justify-content: space-between;
  color: var(--text-primary);
  font-weight: 500;
}

.key-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.key-field > span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 12px;
}

.key-field code {
  margin-left: 4px;
  color: var(--text-muted);
  font-size: 11px;
}

.key-help {
  display: flex;
  margin-top: 6px;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  color: var(--text-muted);
  font-size: 11px;
}

.advanced-options {
  margin: 0 -12px 16px;
}

.result-panel {
  min-width: 0;
  scroll-margin-top: 84px;
}

.result-panel > .ant-card {
  min-height: 560px;
}

.loading-notice,
.error-notice {
  margin-bottom: 18px;
}

.stale-result {
  opacity: 0.62;
}

.result-empty {
  display: grid;
  min-height: 460px;
  place-items: center;
}

.result-empty h3 {
  margin: 12px 0 8px;
  color: var(--text-primary);
  font-size: 17px;
}

.result-empty p {
  max-width: 360px;
  color: var(--text-muted);
  line-height: 1.7;
}

@media (max-width: 1199px) {
  .diagnose-workspace {
    grid-template-columns: minmax(0, 1fr);
  }

  .result-panel > .ant-card {
    min-height: 360px;
  }
}
</style>
