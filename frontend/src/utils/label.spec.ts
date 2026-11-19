import { describe, expect, it } from 'vitest'

import { labelNull } from './label'

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
