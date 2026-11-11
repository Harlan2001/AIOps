<script setup lang="ts">
import { ref } from 'vue'

import { diagnose } from '@/api/diagnose'
import { ApiError } from '@/api/client'
import ResultCard from '@/components/ResultCard.vue'
import { SOURCES } from '@/constants/sources'
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
      const key = keyText.value ? JSON.parse(keyText.value) : {}
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
      errorMsg.value = '主键 JSON 格式错误或请求异常，请检查输入'
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
        <a-form-item label="主键 JSON（可选，留空按日期/默认条件）">
          <a-textarea
            v-model:value="keyText"
            :rows="2"
            placeholder='{"trader_no":"trader","local_no":"000001"}'
          />
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
</style>
