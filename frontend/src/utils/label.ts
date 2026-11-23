// 空/未识别标签归一化（纯函数，便于单测）。
export function labelNull(key: string | null | undefined): string {
  return key === null || key === undefined || key === '' ? '未识别' : key
}

const DIAG_CLASS_LABELS: Record<string, string> = {
  biz: '业务报错',
  noise: '噪音',
  ora: 'DBA 技术错误',
  other: '其他/未识别',
}

export function diagnosisClassLabel(key: string | null | undefined): string {
  if (key === null || key === undefined || key === '') return '未识别'
  return DIAG_CLASS_LABELS[key] ?? key
}

export function ruleTypeLabel(
  key: string | null | undefined,
  rules: Array<{ id: string; title: string }> = [],
): string {
  if (key === null || key === undefined || key === '') return '未识别'
  return rules.find((rule) => rule.id === key)?.title ?? key
}
