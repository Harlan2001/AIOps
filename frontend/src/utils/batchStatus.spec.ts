import { describe, expect, it } from 'vitest'

import { classifyBatchItem } from './batchStatus'
import type { BatchItem } from '@/types/contract'

const record = {
  text: 'some error',
  ldate: '20250321',
  errcode: 0,
}

function makeItem(partial: Record<string, unknown>): BatchItem {
  return { record, ...partial } as BatchItem
}

describe('classifyBatchItem', () => {
  it('隔离返回 error 字符串时归为 error', () => {
    const item = makeItem({ result: null, error: 'RuntimeError: boom' })
    expect(classifyBatchItem(item)).toBe('error')
  })

  it('无结果且无 error 时归为 error（未知）', () => {
    const item = makeItem({ result: null })
    expect(classifyBatchItem(item)).toBe('error')
  })

  it('存在缺参/ SQL 失败时归为 degraded', () => {
    const item = makeItem({
      result: {
        rule_res: { missing_params: [{ step: 's1', missing: ['x'] }] },
      },
    })
    expect(classifyBatchItem(item)).toBe('degraded')
  })

  it('证据完整时归为 normal', () => {
    const item = makeItem({
      result: { rule_res: { missing_params: [], sql_errors: [] } },
    })
    expect(classifyBatchItem(item)).toBe('normal')
  })
})
