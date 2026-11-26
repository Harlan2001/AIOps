export interface SourceOption {
  id: string
  label: string
}

// 单条诊断与批量回放只支持后端 error_records.SOURCES 中的 7 个取数来源。
export const DIAGNOSE_SOURCES: SourceOption[] = [
  { id: 'ftr_err', label: '期货错误委托' },
  { id: 'quote_err', label: '报价错误委托' },
  { id: 'alarm', label: '敞口/止损报警' },
  { id: 'quote_alarm', label: '报价风控预警' },
  { id: 'rule_alarm', label: '合规报警' },
  { id: 'data_check', label: '数据检查' },
  { id: 'flow_control', label: '结算流程控制' },
]

const DIMPLE_SOURCES: SourceOption[] = [
  { id: 'dimple_compliance_alarm', label: 'Dimple 合规预警（实时）' },
  { id: 'dimple_self_deal', label: 'Dimple 自成交（实时）' },
  { id: 'dimple_violation_order', label: 'Dimple 违规委托（实时）' },
  { id: 'dimple_trader_order', label: 'Dimple 交易员委托（实时）' },
  { id: 'dimple_member_order', label: 'Dimple 会员委托（实时）' },
  { id: 'dimple_quota_and_limit', label: 'Dimple 额度与限额（实时）' },
  { id: 'dimple_alarm_note', label: 'Dimple 预警说明（实时）' },
  { id: 'dimple_client_storage_flow', label: 'Dimple 客户库存流水（实时）' },
  { id: 'dimple_defer_fee_rate', label: 'Dimple 递延费率（实时）' },
  { id: 'dimple_estimate_account_remain', label: 'Dimple 预估账户资金（实时）' },
  { id: 'dimple_estimate_storage_remain', label: 'Dimple 预估库存（实时）' },
  { id: 'dimple_fund_realtime', label: 'Dimple 资金实时（实时）' },
  { id: 'dimple_integrate_posi', label: 'Dimple 综合持仓（实时）' },
  { id: 'dimple_member_exposure', label: 'Dimple 会员风险敞口（实时）' },
  { id: 'dimple_member_hold', label: 'Dimple 会员持仓（实时）' },
  { id: 'dimple_member_inventory', label: 'Dimple 会员库存（实时）' },
  { id: 'dimple_member_qty_weight_limit', label: 'Dimple 会员数量重量限额（实时）' },
  { id: 'dimple_member_transaction', label: 'Dimple 会员交易（实时）' },
  { id: 'dimple_member_wrong_order', label: 'Dimple 会员错单（实时）' },
  { id: 'dimple_option_exec', label: 'Dimple 期权行权（实时）' },
  { id: 'dimple_real_time_arbi_quot', label: 'Dimple 实时套利行情（实时）' },
  { id: 'dimple_real_time_quot', label: 'Dimple 实时行情（实时）' },
  { id: 'dimple_rfq_default_declaration', label: 'Dimple 保证金询价违约申报（实时）' },
  { id: 'dimple_rfq_match', label: 'Dimple 询价成交（实时）' },
  { id: 'dimple_rfq_posi', label: 'Dimple 询价持仓（实时）' },
  { id: 'dimple_rfq_uncheck_match', label: 'Dimple 询价未确认成交（实时）' },
  { id: 'dimple_self_hedging', label: 'Dimple 自营套保（实时）' },
  { id: 'dimple_self_run_trader_deal', label: 'Dimple 自营交易员成交（实时）' },
  { id: 'dimple_self_run_trader_hold', label: 'Dimple 自营交易员持仓（实时）' },
  { id: 'dimple_self_run_trader_stock', label: 'Dimple 自营交易员库存（实时）' },
  { id: 'dimple_self_run_trader_wrong', label: 'Dimple 自营交易员错单（实时）' },
  { id: 'dimple_trade_purpose_posi', label: 'Dimple 交易用途持仓（实时）' },
  { id: 'dimple_trader_credit_limit', label: 'Dimple 交易员授信额度（实时）' },
  { id: 'dimple_trader_delivery_declare', label: 'Dimple 交易员交割申报（实时）' },
  { id: 'dimple_trader_delivery_declare_trade', label: 'Dimple 交易员交割申报成交（实时）' },
  { id: 'dimple_trader_exposure', label: 'Dimple 交易员风险敞口（实时）' },
  { id: 'dimple_trader_qty_weight_limit', label: 'Dimple 交易员数量重量限额（实时）' },
]

const IQUANT_SOURCES: SourceOption[] = [
  { id: 'iquant_day_abnormal_event', label: 'iQuant 事中风控事件（实时）' },
]

// 历史与实时日志筛选可以查看全部来源，与诊断取数来源严格分开。
export const LOG_SOURCES: SourceOption[] = [
  ...DIAGNOSE_SOURCES,
  ...DIMPLE_SOURCES,
  ...IQUANT_SOURCES,
]
export const SOURCE_LABELS: Record<string, string> = Object.fromEntries(
  LOG_SOURCES.map((item) => [item.id, item.label]),
)

// 实时监控来源 id -> 中文标签（实时页展示用，含 Dimple 与 iQuant）。
export const REALTIME_SOURCE_LABELS: Record<string, string> = {
  iquant_day_abnormal_event: 'iQuant 事中风控事件',
  dimple_compliance_alarm: '合规预警',
  dimple_self_deal: '自成交',
  dimple_violation_order: '违规委托',
  dimple_trader_order: '交易员委托',
  dimple_member_order: '会员委托',
  dimple_quota_and_limit: '额度与限额',
  dimple_alarm_note: '预警说明',
  dimple_client_storage_flow: '客户库存流水',
  dimple_defer_fee_rate: '递延费率',
  dimple_estimate_account_remain: '预估账户资金',
  dimple_estimate_storage_remain: '预估库存',
  dimple_fund_realtime: '资金实时',
  dimple_integrate_posi: '综合持仓',
  dimple_member_exposure: '会员风险敞口',
  dimple_member_hold: '会员持仓',
  dimple_member_inventory: '会员库存',
  dimple_member_qty_weight_limit: '会员数量重量限额',
  dimple_member_transaction: '会员交易',
  dimple_member_wrong_order: '会员错单',
  dimple_option_exec: '期权行权',
  dimple_real_time_arbi_quot: '实时套利行情',
  dimple_real_time_quot: '实时行情',
  dimple_rfq_default_declaration: '保证金询价违约申报',
  dimple_rfq_match: '询价成交',
  dimple_rfq_posi: '询价持仓',
  dimple_rfq_uncheck_match: '询价未确认成交',
  dimple_self_hedging: '自营套保',
  dimple_self_run_trader_deal: '自营交易员成交',
  dimple_self_run_trader_hold: '自营交易员持仓',
  dimple_self_run_trader_stock: '自营交易员库存',
  dimple_self_run_trader_wrong: '自营交易员错单',
  dimple_trade_purpose_posi: '交易用途持仓',
  dimple_trader_credit_limit: '交易员授信额度',
  dimple_trader_delivery_declare: '交易员交割申报',
  dimple_trader_delivery_declare_trade: '交易员交割申报成交',
  dimple_trader_exposure: '交易员风险敞口',
  dimple_trader_qty_weight_limit: '交易员数量重量限额',
}
