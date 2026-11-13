import { http } from './client'
import type { BatchResponse, DiagnosisResult } from '@/types/contract'

export interface DiagnosePayload {
  text?: string
  ldate?: string
  errcode?: number
  lsection?: string
  record?: { source: string; date: string; key?: Record<string, unknown> }
  include_report?: boolean
  escalate?: boolean
}

export function diagnose(payload: DiagnosePayload) {
  return http
    .post<DiagnosisResult>('/v1/diagnose', payload)
    .then((res) => res.data)
}

// 批量回放需对每条记录跑取证，耗时较长，单独放宽到 5 分钟。
const BATCH_TIMEOUT = 300000

export function batchByItems(
  items: DiagnosePayload[],
): Promise<BatchResponse> {
  return http
    .post<BatchResponse>('/v1/batch-diagnose', { items }, {
      timeout: BATCH_TIMEOUT,
    })
    .then((res) => res.data)
}

export function batchReplay(
  source: string,
  date: string,
): Promise<BatchResponse> {
  return http
    .post<BatchResponse>('/v1/batch-diagnose', { source, date }, {
      timeout: BATCH_TIMEOUT,
    })
    .then((res) => res.data)
}
