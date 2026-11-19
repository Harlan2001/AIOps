// 错误来源（与后端 error_records.SOURCES 对应，末尾为 Dimple 实时接口来源）。
export const SOURCES: Array<{ id: string; label: string }> = [
  { id: 'ftr_err', label: '期货错误委托' },
  { id: 'quote_err', label: '报价错误委托' },
  { id: 'alarm', label: '敞口/止损报警' },
  { id: 'quote_alarm', label: '报价风控预警' },
  { id: 'rule_alarm', label: '合规报警' },
  { id: 'data_check', label: '数据检查' },
  { id: 'flow_control', label: '结算流程控制' },
  { id: 'dimple_compliance_alarm', label: 'Dimple 合规预警（实时）' },
  { id: 'dimple_self_deal', label: 'Dimple 自成交（实时）' },
  { id: 'dimple_violation_order', label: 'Dimple 违规委托（实时）' },
  { id: 'dimple_trader_order', label: 'Dimple 交易员委托（实时）' },
  { id: 'dimple_member_order', label: 'Dimple 会员委托（实时）' },
  { id: 'dimple_quota_and_limit', label: 'Dimple 额度与限额（实时）' },
]

// Dimple 实时监控来源 id -> 中文标签（实时页展示用）。
export const REALTIME_SOURCE_LABELS: Record<string, string> = {
  dimple_compliance_alarm: '合规预警',
  dimple_self_deal: '自成交',
  dimple_violation_order: '违规委托',
  dimple_trader_order: '交易员委托',
  dimple_member_order: '会员委托',
  dimple_quota_and_limit: '额度与限额',
}
