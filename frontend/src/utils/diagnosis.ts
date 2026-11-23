import type { DiagnosisResult } from '@/types/contract'

export interface ParsedDiagnosis {
  result: DiagnosisResult | null
  error: string
}

export function parseDiagnosisResult(raw?: string | null): ParsedDiagnosis {
  if (!raw) return { result: null, error: '该记录没有完整诊断快照' }
  try {
    const parsed: unknown = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return { result: null, error: '诊断快照格式不完整' }
    }
    return { result: parsed as DiagnosisResult, error: '' }
  } catch {
    return { result: null, error: '诊断快照无法解析，当前仅展示已保存的摘要' }
  }
}

export function formatPercent(value?: number | null, digits = 1): string {
  if (value === null || value === undefined || !Number.isFinite(value) || value < 0 || value > 1) {
    return '—'
  }
  return `${(value * 100).toFixed(digits)}%`
}

export function formatConfidence(value?: number | null): string {
  return formatPercent(value, 0)
}

export function formatBusinessDate(value?: string | null): string {
  if (!value) return '—'
  const match = /^(\d{4})(\d{2})(\d{2})$/.exec(value)
  return match ? `${match[1]}-${match[2]}-${match[3]}` : value
}

export function formatDateTime(value?: string | null): string {
  if (!value) return '—'
  const date = new Date(value)
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleString('zh-CN', { hour12: false })
}
