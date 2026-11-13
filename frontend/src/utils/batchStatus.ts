import type { BatchItem } from '@/types/contract'

export type BatchStatus = 'error' | 'degraded' | 'normal'

// 逐项隔离的异常/无结果显式归为 error；缺参或 SQL 失败归为 degraded；其余正常。
export function classifyBatchItem(item: BatchItem): BatchStatus {
  if (item.error || !item.result) {
    return 'error'
  }
  const ruleRes = item.result.rule_res
  const hasDegrade =
    (ruleRes?.missing_params?.length ?? 0) > 0 ||
    (ruleRes?.sql_errors?.length ?? 0) > 0
  return hasDegrade ? 'degraded' : 'normal'
}
