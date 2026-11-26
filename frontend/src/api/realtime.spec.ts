import { beforeEach, describe, expect, it, vi } from 'vitest'

const mocks = vi.hoisted(() => ({
  getDiagnoses: vi.fn(),
  getDiagnosisDetail: vi.fn(),
}))

vi.mock('./diagnoses', () => mocks)

import { getRealtimeAlarms } from './realtime'

describe('getRealtimeAlarms', () => {
  beforeEach(() => {
    mocks.getDiagnoses.mockReset()
    mocks.getDiagnoses.mockResolvedValue({ total: 0, items: [] })
  })

  it('默认查询全部实时来源的真实异常', async () => {
    await getRealtimeAlarms()

    expect(mocks.getDiagnoses).toHaveBeenCalledWith({
      offset: 0,
      limit: 20,
      anomaly_only: true,
      realtime_only: true,
    })
  })

  it('全部记录模式仍限定实时来源', async () => {
    await getRealtimeAlarms(20, 10, false)

    expect(mocks.getDiagnoses).toHaveBeenCalledWith({
      offset: 20,
      limit: 10,
      anomaly_only: false,
      realtime_only: true,
    })
  })

  it('叠加来源与分类筛选时保留实时和异常语义', async () => {
    await getRealtimeAlarms(0, 10, true, {
      source: 'iquant_day_abnormal_event',
      diag_class: 'biz',
    })

    expect(mocks.getDiagnoses).toHaveBeenCalledWith({
      offset: 0,
      limit: 10,
      anomaly_only: true,
      realtime_only: true,
      source: 'iquant_day_abnormal_event',
      diag_class: 'biz',
    })
  })
})
