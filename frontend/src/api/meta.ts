import { http } from './client'
import type {
  HealthStatus,
  RecordsResponse,
  RulesResponse,
} from '@/types/contract'

export function getHealth(): Promise<HealthStatus> {
  return http.get<HealthStatus>('/healthz').then((res) => res.data)
}

export function getRecords(
  source: string,
  date: string,
  limit?: number,
): Promise<RecordsResponse> {
  return http
    .get<RecordsResponse>('/v1/records', { params: { source, date, limit } })
    .then((res) => res.data)
}

export function getRules(): Promise<RulesResponse> {
  return http.get<RulesResponse>('/v1/rules').then((res) => res.data)
}
