import { describe, expect, it } from 'vitest'

import {
  formatBusinessDate,
  formatConfidence,
  formatPercent,
  parseDiagnosisResult,
} from './diagnosis'

describe('历史诊断快照解析', () => {
  it('解析有效 JSON 对象', () => {
    const parsed = parseDiagnosisResult('{"text":"demo","escalated":false}')
    expect(parsed.error).toBe('')
    expect(parsed.result?.text).toBe('demo')
  })

  it('空值、无效 JSON 与非对象均返回可读错误', () => {
    expect(parseDiagnosisResult(null).result).toBeNull()
    expect(parseDiagnosisResult('{bad').error).toContain('无法解析')
    expect(parseDiagnosisResult('[]').error).toContain('不完整')
  })
})

describe('诊断数字与日期格式', () => {
  it('按 0 到 1 的契约格式化置信度和比率', () => {
    expect(formatConfidence(0.86)).toBe('86%')
    expect(formatPercent(0.125)).toBe('12.5%')
    expect(formatPercent(0)).toBe('0.0%')
    expect(formatPercent(1.2)).toBe('—')
    expect(formatConfidence(null)).toBe('—')
  })

  it('格式化 YYYYMMDD 业务日期并保留其他原始值', () => {
    expect(formatBusinessDate('20261123')).toBe('2026-11-23')
    expect(formatBusinessDate('2026/11/23')).toBe('2026/11/23')
    expect(formatBusinessDate(null)).toBe('—')
  })
})
