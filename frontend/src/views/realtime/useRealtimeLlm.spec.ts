import { ref } from 'vue'
import { describe, expect, it } from 'vitest'

import type { DiagLogItem, DiagnosisResult } from '@/types/contract'
import { useRealtimeLlm } from './useRealtimeLlm'

function makeLog(id: number): DiagLogItem {
  return {
    id,
    trigger_type: 'scheduled',
    input_mode: 'record',
    source: 'dimple_compliance_alarm',
    error_text: `alarm-${id}`,
    escalated: false,
    evidence_count: 0,
    diag_status: 'success',
  }
}

function makeResult(escalated: boolean, root: string): DiagnosisResult {
  return {
    text: 'alarm',
    errcode: 0,
    ldate: '20261120',
    loc: '',
    rule_res: null,
    kb_card: null,
    answer: { root, actions: [], confidence: 0.8, secondary: [] },
    source: escalated ? 'LLM 诊断' : '规则兜底（LLM 未配置/不可用）',
    escalated,
  }
}

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((res) => {
    resolve = res
  })
  return { promise, resolve }
}

describe('useRealtimeLlm', () => {
  it('仅展示实际走完 LLM 路径的结论', async () => {
    const state = useRealtimeLlm(
      ref(makeLog(1)),
      async () => makeResult(true, 'LLM 根因'),
    )

    await state.onLlmToggle(true)

    expect(state.llmEnabled.value).toBe(true)
    expect(state.llmAnswer.value?.root).toBe('LLM 根因')
    expect(state.llmNotice.value).toBe('')
    expect(state.llmLoading.value).toBe(false)
  })

  it('规则结果或降级兜底不冒充 LLM 结论', async () => {
    const state = useRealtimeLlm(
      ref(makeLog(1)),
      async () => makeResult(false, '规则根因'),
    )

    await state.onLlmToggle(true)

    expect(state.llmEnabled.value).toBe(false)
    expect(state.llmAnswer.value).toBeNull()
    expect(state.llmNotice.value).toContain('未实际调用大模型')
    expect(state.llmNotice.value).toContain('规则兜底')
    expect(state.llmLoading.value).toBe(false)
  })

  it('切换详情后忽略旧请求，且旧请求不会结束新请求的加载态', async () => {
    const first = deferred<DiagnosisResult>()
    const second = deferred<DiagnosisResult>()
    let calls = 0
    const detail = ref<DiagLogItem | null>(makeLog(1))
    const state = useRealtimeLlm(detail, async () => {
      calls += 1
      return (calls === 1 ? first : second).promise
    })

    const firstRequest = state.onLlmToggle(true)
    state.resetLlm()
    detail.value = makeLog(2)
    const secondRequest = state.onLlmToggle(true)

    first.resolve(makeResult(true, '告警 A 的 LLM 结果'))
    await firstRequest
    expect(state.llmAnswer.value).toBeNull()
    expect(state.llmLoading.value).toBe(true)

    second.resolve(makeResult(true, '告警 B 的 LLM 结果'))
    await secondRequest
    expect(state.llmAnswer.value?.root).toBe('告警 B 的 LLM 结果')
    expect(state.llmLoading.value).toBe(false)
  })

  it('关闭开关后忽略未完成响应', async () => {
    const pending = deferred<DiagnosisResult>()
    const state = useRealtimeLlm(ref(makeLog(1)), async () => pending.promise)

    const request = state.onLlmToggle(true)
    await state.onLlmToggle(false)
    pending.resolve(makeResult(true, '过期结果'))
    await request

    expect(state.llmEnabled.value).toBe(false)
    expect(state.llmAnswer.value).toBeNull()
    expect(state.llmLoading.value).toBe(false)
  })
})
