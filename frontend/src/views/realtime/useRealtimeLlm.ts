import { ref, type Ref } from 'vue'

import { ApiError } from '@/api/client'
import { escalateDiagnosis } from '@/api/diagnoses'
import type { Answer, DiagLogItem } from '@/types/contract'

export const LLM_TIMEOUT = 180000

type EscalateFn = typeof escalateDiagnosis

// 已有告警的按需 LLM 状态。请求代次用于隔离关闭开关、切换详情和乱序响应。
export function useRealtimeLlm(
  detail: Ref<DiagLogItem | null>,
  escalate: EscalateFn = escalateDiagnosis,
) {
  const llmEnabled = ref(false)
  const llmLoading = ref(false)
  const llmAnswer = ref<Answer | null>(null)
  const llmError = ref('')
  const llmNotice = ref('')
  let generation = 0

  function resetLlm() {
    generation += 1
    llmEnabled.value = false
    llmLoading.value = false
    llmAnswer.value = null
    llmError.value = ''
    llmNotice.value = ''
  }

  async function onLlmToggle(enabled: boolean) {
    const requestGeneration = ++generation
    llmEnabled.value = enabled
    llmAnswer.value = null
    llmError.value = ''
    llmNotice.value = ''

    if (!enabled) {
      llmLoading.value = false
      return
    }
    const target = detail.value
    if (!target) {
      llmEnabled.value = false
      llmLoading.value = false
      return
    }

    llmLoading.value = true
    try {
      const res = await escalate(target.id, { timeout: LLM_TIMEOUT })
      if (requestGeneration !== generation) return

      // escalated=false 表示规则快路径或 LLM 不可用兜底，不能冒充 LLM 结论。
      if (!res.escalated) {
        llmEnabled.value = false
        llmNotice.value = res.source
          ? `本次未实际调用大模型（${res.source}），请以上方规则诊断为准。`
          : '本次未实际调用大模型，请以上方规则诊断为准。'
        return
      }
      llmAnswer.value = res.answer
      if (!res.answer) {
        llmEnabled.value = false
        llmError.value = '大模型未返回有效结论'
      }
    } catch (e) {
      if (requestGeneration !== generation) return
      llmEnabled.value = false
      llmError.value =
        e instanceof ApiError
          ? e.status === 409
            ? '当前部署未开启大模型升级（allow_escalation=false）'
            : `大模型调用失败（${e.status}）：${e.message}`
          : '大模型调用异常，请稍后重试'
    } finally {
      if (requestGeneration === generation) llmLoading.value = false
    }
  }

  return {
    llmEnabled,
    llmLoading,
    llmAnswer,
    llmError,
    llmNotice,
    onLlmToggle,
    resetLlm,
  }
}
