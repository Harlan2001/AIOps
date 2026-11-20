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

  it('默认仅查询 Dimple 真实异常', async () => {
    await getRealtimeAlarms()

    expect(mocks.getDiagnoses).toHaveBeenCalledWith({
      offset: 0,
      limit: 20,
      anomaly_only: true,
      dimple_only: true,
    })
  })

  it('全部记录模式仍限定 Dimple 来源', async () => {
    await getRealtimeAlarms(20, 10, false)

    expect(mocks.getDiagnoses).toHaveBeenCalledWith({
      offset: 20,
      limit: 10,
      anomaly_only: false,
      dimple_only: true,
    })
  })
})
