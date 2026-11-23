import { describe, expect, it } from 'vitest'

import { diagnosisClassLabel, labelNull, ruleTypeLabel } from './label'

describe('labelNull', () => {
  it('空值归一化为未识别', () => {
    expect(labelNull(null)).toBe('未识别')
    expect(labelNull(undefined)).toBe('未识别')
    expect(labelNull('')).toBe('未识别')
  })

  it('非空值原样返回', () => {
    expect(labelNull('fund')).toBe('fund')
    expect(labelNull('biz')).toBe('biz')
  })
})

describe('诊断业务标签', () => {
  it('分类代码转为中文并保留未知代码', () => {
    expect(diagnosisClassLabel('biz')).toBe('业务报错')
    expect(diagnosisClassLabel('ora')).toBe('DBA 技术错误')
    expect(diagnosisClassLabel('new_class')).toBe('new_class')
    expect(diagnosisClassLabel(null)).toBe('未识别')
  })

  it('优先使用规则标题，规则不存在时回退类型 id', () => {
    const rules = [{ id: 'price_limit', title: '委托价格超限' }]
    expect(ruleTypeLabel('price_limit', rules)).toBe('委托价格超限')
    expect(ruleTypeLabel('unknown', rules)).toBe('unknown')
    expect(ruleTypeLabel(null, rules)).toBe('未识别')
  })
})
