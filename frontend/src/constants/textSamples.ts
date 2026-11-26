// 自由文本诊断常用示例：点击即可填充到输入框，覆盖规则命中 / 未覆盖 / 噪音等不同路径。
export interface TextSample {
  id: string
  label: string
  text: string
  hint: string
}

export const TEXT_SAMPLES: TextSample[] = [
  {
    id: 'price_limit',
    label: '价格超出涨停板',
    text: '自营交易员错单：exchCode：01，orderTime：14:46:08，traderNo：fml，memberId：0415，clientId：00000415，varietyId：au，contractId：au2612-au2702，price：0，qty：10，reason：价格超出涨停板',
    hint: '规则命中 price_limit，含组合合约拆分',
  },
  {
    id: 'quota_short',
    label: '保值额度不足',
    text: '会员错单：investAbbr：世界银行，memberId：0415，clientId：00000415，varietyId：ag，contractId：ag2612-ag2704，price：0，qty：1，reason：保值额度不足',
    hint: '规则未覆盖，适合打开 LLM 兜底',
  },
  {
    id: 'position',
    label: '持仓不足',
    text: '报错：客户持仓不足，平仓数量超过可用持仓，memberId：0415，contractId：au2612',
    hint: '规则命中 position_not_enough',
  },
  {
    id: 'market_closed',
    label: '非交易时间',
    text: '当前为非交易时间，市场已闭市，无法提交委托',
    hint: '规则命中 market_closed',
  },
  {
    id: 'noise',
    label: '定时任务成功（噪音）',
    text: '定时任务执行成功，结算流程正常完成',
    hint: '噪音过滤，无需诊断',
  },
  {
    id: 'plain',
    label: '简短自由文本',
    text: '本地报单号没有递增',
    hint: '通用文本，看规则或兜底',
  },
]
