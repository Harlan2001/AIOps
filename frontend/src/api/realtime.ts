import { getDiagnoses, getDiagnosisDetail } from './diagnoses'
import type { DiagListResponse, DiagLogItem } from '@/types/contract'

// 拉取 Dimple 各实时来源的诊断结果（落库后经 /v1/diagnoses 读取，按 id 倒序）。
// anomalyOnly=true（默认）：只看真实异常；false：含行情/持仓等业务数据的全部记录。
export function getRealtimeAlarms(
  offset = 0,
  limit = 20,
  anomalyOnly = true,
): Promise<DiagListResponse> {
  return getDiagnoses({
    offset,
    limit,
    anomaly_only: anomalyOnly,
    dimple_only: true,
  })
}

// 单条实时预警详情（含完整结果快照）。
export function getRealtimeDetail(id: number): Promise<DiagLogItem> {
  return getDiagnosisDetail(id)
}
