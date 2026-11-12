// 各来源（历史表）主键元数据：日期列由日期输入自动补，requiredKeys 为仍需在 JSON 中提供的主键列。
// sample 为可直接使用的完整示例（ftr_err 示例已实测可命中真实记录）。
export interface SourceKeyMeta {
  id: string
  dateCol: string
  requiredKeys: string[]
  sample: Record<string, string>
}

export const SOURCE_KEYS: Record<string, SourceKeyMeta> = {
  ftr_err: {
    id: 'ftr_err',
    dateCol: 'trade_date',
    requiredKeys: ['trader_no', 'local_no', 'purpose_code'],
    sample: {
      trader_no: 'trader1',
      local_no: '000000240421',
      purpose_code: 'ZY',
    },
  },
  quote_err: {
    id: 'quote_err',
    dateCol: 'trade_date',
    requiredKeys: ['trader_no', 'local_no'],
    sample: { trader_no: 'trader1', local_no: '000000000001' },
  },
  alarm: {
    id: 'alarm',
    dateCol: 'alarm_date',
    requiredKeys: ['seq_no', 'alarm_type'],
    sample: { seq_no: '1', alarm_type: '1' },
  },
  quote_alarm: {
    id: 'quote_alarm',
    dateCol: 'trade_date',
    requiredKeys: ['seq_no'],
    sample: { seq_no: '1' },
  },
  rule_alarm: {
    id: 'rule_alarm',
    dateCol: 'alarm_date',
    requiredKeys: ['seq_no', 'member_id', 'alarm_type'],
    sample: { seq_no: '1', member_id: '016811', alarm_type: '1' },
  },
  data_check: {
    id: 'data_check',
    dateCol: 'check_date',
    requiredKeys: ['seq_no'],
    sample: { seq_no: '1' },
  },
  flow_control: {
    id: 'flow_control',
    dateCol: 'clear_date',
    requiredKeys: ['flow_code', 'exch_code'],
    sample: { flow_code: '1', exch_code: 'SSE' },
  },
}
