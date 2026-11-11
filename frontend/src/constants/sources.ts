// 错误来源（与后端 error_records.SOURCES 对应）。
export const SOURCES: Array<{ id: string; label: string }> = [
  { id: 'ftr_err', label: '期货错误委托' },
  { id: 'quote_err', label: '报价错误委托' },
  { id: 'alarm', label: '敞口/止损报警' },
  { id: 'quote_alarm', label: '报价风控预警' },
  { id: 'rule_alarm', label: '合规报警' },
  { id: 'data_check', label: '数据检查' },
  { id: 'flow_control', label: '结算流程控制' },
]
