import { getDiagnoses, getDiagnosisDetail } from './diagnoses'
import type { DiagListResponse, DiagLogItem } from '@/types/contract'

// 拉取 Dimple 各实时来源的诊断结果（落库后经 /v1/diagnoses 读取，按 id 倒序）。
// 当前落库记录均为 Dimple 实时来源，故不按单一 source 过滤，统一展示全部。
export function getRealtimeAlarms(
  offset = 0,
  limit = 20,
): Promise<DiagListResponse> {
  return getDiagnoses({ offset, limit })
}

// 单条实时预警详情（含完整结果快照）。
export function getRealtimeDetail(id: number): Promise<DiagLogItem> {
  return getDiagnosisDetail(id)
}
