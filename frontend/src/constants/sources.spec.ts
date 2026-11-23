import { describe, expect, it } from 'vitest'

import { DIAGNOSE_SOURCES, LOG_SOURCES } from './sources'
import { SOURCE_KEYS } from './sourceKeys'

describe('诊断来源与日志来源分组', () => {
  it('诊断取数来源均有主键元数据且不含 Dimple 专用来源', () => {
    expect(DIAGNOSE_SOURCES).toHaveLength(7)
    for (const source of DIAGNOSE_SOURCES) {
      expect(SOURCE_KEYS[source.id]?.id).toBe(source.id)
      expect(source.id.startsWith('dimple_')).toBe(false)
    }
  })

  it('日志筛选保留诊断来源与 Dimple 来源', () => {
    expect(LOG_SOURCES.length).toBeGreaterThan(DIAGNOSE_SOURCES.length)
    expect(LOG_SOURCES.some((source) => source.id === 'ftr_err')).toBe(true)
    expect(LOG_SOURCES.some((source) => source.id === 'dimple_compliance_alarm')).toBe(true)
  })
})
