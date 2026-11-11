// 与后端 pydantic 契约（DiagnosisResult 等）对齐的前端类型定义。

export interface Answer {
  root?: string | null
  actions: string[]
  confidence?: number | null
  secondary: Array<Record<string, unknown>>
  evidence_note?: string | null
}

export interface EvidenceRow {
  title?: string
  r?: {
    status?: string
    missing?: string[]
    error?: string
    rows?: Array<Record<string, unknown>>
    cols?: string[]
  }
}

export interface MissingParam {
  step?: string
  missing?: string[]
}

export interface SqlError {
  step?: string
  error?: string
}

export interface RuleResult {
  class?: string
  verdict?: string
  type?: { id?: string; title?: string } | null
  evidence?: EvidenceRow[]
  evidence_complete?: boolean
  primary_evidence_ok?: boolean
  missing_params?: MissingParam[]
  sql_errors?: SqlError[]
  [key: string]: unknown
}

export interface KbCard {
  cards?: Array<{
    title?: string
    required_facts?: string[]
    readonly_queries?: Array<Record<string, unknown>>
  }>
  [key: string]: unknown
}

export interface DiagnosisResult {
  text: string
  errcode: number
  ldate: string
  loc: string
  rule_res: RuleResult | null
  kb_card: KbCard | null
  answer: Answer | null
  source: string
  escalated: boolean
  telemetry?: Record<string, unknown> | null
  report?: string | null
}

export interface RecordSummary {
  text: string
  ldate: string
  source?: string
  source_label?: string
  errcode: number
  key?: Record<string, unknown> | null
}

export interface BatchItem {
  record: RecordSummary
  result?: DiagnosisResult | null
  error?: string | null
}

export interface BatchResponse {
  count: number
  truncated: boolean
  max_batch: number
  results: BatchItem[]
}

export interface HealthStatus {
  status: 'ok' | 'degraded'
  service: string
  gauss: { ok: boolean; msg: string }
  rules_count: number
  noise_keywords: number
  time: string
}

export interface RuleItem {
  id: string
  title: string
  runbook: string
  keywords: string[]
  err_codes: number[]
}

export interface RulesResponse {
  total: number
  noise_keywords: string[]
  rules: RuleItem[]
  coverage: string
}

export interface RecordsResponse {
  count: number
  limit: number
  records: RecordSummary[]
}
