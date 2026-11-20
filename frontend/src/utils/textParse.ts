// 自由文本解析纯函数：业务日期提取、多条拆分（便于单测）。

// 从文本提取业务日期：支持 YYYY-MM-DD / YYYY/MM/DD 与连续 8 位数字（YYYYMMDD）。
export function extractBusinessDate(text: string): string {
  const t = text || ''
  const m1 = t.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/)
  if (m1) {
    return m1[1] + m1[2].padStart(2, '0') + m1[3].padStart(2, '0')
  }
  const m2 = t.match(/(?<!\d)(\d{8})(?!\d)/)
  return m2 ? m2[1] : ''
}

// 拆分为多条：有空行按空行分段（段内换行属同一条）；否则每个非空行一条。
export function splitRecords(text: string): string[] {
  const t = (text || '').trim()
  if (!t) return []
  if (/\n\s*\n/.test(t)) {
    return t.split(/\n\s*\n/).map((s) => s.trim()).filter(Boolean)
  }
  return t.split(/\n/).map((s) => s.trim()).filter(Boolean)
}
