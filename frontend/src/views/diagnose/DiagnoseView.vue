<script setup lang="ts">
import { computed, ref } from 'vue'

import { diagnose } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import ResultCard from '@/components/ResultCard.vue'
import { SOURCES } from '@/constants/sources'
import { SOURCE_KEYS } from '@/constants/sourceKeys'
import type { DiagnosisResult } from '@/types/contract'

const mode = ref<'text' | 'record'>('text')
const text = ref('')
const ldate = ref('')
const source = ref(SOURCES[0].id)
const date = ref('')
const keyText = ref('')
const escalate = ref(false)
const loading = ref(false)
const errorMsg = ref('')
const result = ref<DiagnosisResult | null>(null)

const keyMeta = computed(() => SOURCE_KEYS[source.value])

function fillSample() {
  keyText.value = JSON.stringify(keyMeta.value.sample, null, 2)
}

async function run() {
  loading.value = true
  errorMsg.value = ''
  result.value = null
  try {
    if (mode.value === 'text') {
      result.value = await diagnose({
        text: text.value,
        ldate: ldate.value,
        escalate: escalate.value,
      })
    } else {
      let key: Record<string, unknown>
      try {
        key = keyText.value ? JSON.parse(keyText.value) : {}
      } catch {
        errorMsg.value = '主键 JSON 格式错误，请检查后重试'
        loading.value = false
        return
      }
      // 前端按所选来源校验必填主键，避免留空/缺字段被后端 422 拒绝
      const missing = keyMeta.value.requiredKeys.filter(
        (k) => key[k] === undefined || key[k] === null || key[k] === '',
      )
      if (missing.length) {
        errorMsg.value = `来源 ${source.value} 缺少必需主键：${missing.join(
          '、',
        )}（日期列 ${keyMeta.value.dateCol} 已由业务日期自动补全）`
        loading.value = false
        return
      }
      result.value = await diagnose({
        record: { source: source.value, date: date.value, key },
        escalate: escalate.value,
      })
    }
  } catch (e) {
    if (e instanceof ApiError) {
      errorMsg.value =
        e.status === 409
          ? `升级被拒绝（409）：${e.message}`
          : `请求失败（${e.status}）：${e.message}`
    } else {
      errorMsg.value = '请求异常，请检查输入'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <a-card title="单条诊断">
    <a-radio-group v-model:value="mode" class="mode-group">
      <a-radio-button value="text">文本直输</a-radio-button>
      <a-radio-button value="record">来源取数</a-radio-button>
    </a-radio-group>

    <a-form layout="vertical">
      <template v-if="mode === 'text'">
        <a-form-item label="报错文本" required>
          <a-textarea v-model:value="text" :rows="3" placeholder="粘贴报错文本" />
        </a-form-item>
        <a-form-item label="业务日期 YYYYMMDD">
          <a-input v-model:value="ldate" style="max-width: 240px" />
        </a-form-item>
      </template>

      <template v-else>
        <a-row :gutter="16">
          <a-col :span="12">
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
          </a-col>
          <a-col :span="12">
            <a-form-item label="业务日期 YYYYMMDD">
              <a-input v-model:value="date" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item>
          <template #label>
            主键 JSON（必填：{{ keyMeta.requiredKeys.join('、') }}）
            <a-button type="link" size="small" @click="fillSample">
              填充示例
            </a-button>
          </template>
          <a-textarea v-model:value="keyText" :rows="3" />
          <p class="hint">
            日期列 {{ keyMeta.dateCol }} 由上方业务日期自动补全，无需写入；
            该来源完整主键为 {{ keyMeta.dateCol }}、{{ keyMeta.requiredKeys.join('、') }}。
          </p>
        </a-form-item>
      </template>

      <a-form-item>
        <a-checkbox v-model:checked="escalate">
          允许 LLM 升级（escalate；受部署开关约束）
        </a-checkbox>
      </a-form-item>

      <a-button type="primary" :loading="loading" @click="run">
        开始诊断
      </a-button>
    </a-form>

    <a-alert
      v-if="errorMsg"
      type="error"
      show-icon
      :message="errorMsg"
      class="result-block"
    />
    <div v-if="result" class="result-block">
      <ResultCard :result="result" />
    </div>
  </a-card>
</template>

<style scoped>
.mode-group {
  margin-bottom: 16px;
}

.result-block {
  margin-top: 24px;
}

.hint {
  margin-top: 4px;
  color: #888;
  font-size: 12px;
}
</style>
