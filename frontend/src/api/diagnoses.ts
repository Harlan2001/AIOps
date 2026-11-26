import { http } from './client'
import type { AxiosRequestConfig } from 'axios'
import type {
  DiagListResponse,
  DiagLogItem,
  DiagStats,
  DiagnosisResult,
} from '@/types/contract'

export interface DiagListParams {
  source?: string
  diag_class?: string
  diag_type?: string
  annot_status?: string
  start_date?: string
  end_date?: string
  anomaly_only?: boolean
  dimple_only?: boolean
  realtime_only?: boolean
  offset?: number
  limit?: number
}

export function getDiagnosisStats(
  startDate?: string,
  endDate?: string,
): Promise<DiagStats> {
  return http
    .get<DiagStats>('/v1/diagnoses/stats', {
      params: { start_date: startDate, end_date: endDate },
    })
    .then((res) => res.data)
}

export function getDiagnoses(
  params: DiagListParams = {},
): Promise<DiagListResponse> {
  return http
    .get<DiagListResponse>('/v1/diagnoses', { params })
    .then((res) => res.data)
}

export function getDiagnosisDetail(id: number): Promise<DiagLogItem> {
  return http
    .get<DiagLogItem>(`/v1/diagnoses/${id}`)
    .then((res) => res.data)
}

// 已有日志的临时升级预览：后端不新增诊断事件，也不覆盖原始记录。
export function escalateDiagnosis(
  id: number,
  config?: AxiosRequestConfig,
): Promise<DiagnosisResult> {
  return http
    .post<DiagnosisResult>(`/v1/diagnoses/${id}/escalate`, undefined, config)
    .then((res) => res.data)
}

export interface AnnotationPayload {
  annot_status: 'correct' | 'wrong'
  correct_answer?: string | null
  annotator: string
}

export function annotateDiagnosis(
  id: number,
  payload: AnnotationPayload,
): Promise<{ status: string }> {
  return http
    .post(`/v1/diagnoses/${id}/annotation`, payload)
    .then((res) => res.data)
}
