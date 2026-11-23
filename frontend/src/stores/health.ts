import { defineStore } from 'pinia'

import { getHealth } from '@/api/meta'
import type { HealthStatus } from '@/types/contract'

interface HealthState {
  data: HealthStatus | null
  loading: boolean
  error: string
}

let refreshGeneration = 0

export const useHealthStore = defineStore('health', {
  state: (): HealthState => ({
    data: null,
    loading: false,
    error: '',
  }),
  getters: {
    isDegraded: (state) => state.data?.status === 'degraded',
  },
  actions: {
    async refresh() {
      const requestGeneration = ++refreshGeneration
      this.loading = true
      this.error = ''
      try {
        const data = await getHealth()
        if (requestGeneration !== refreshGeneration) return
        this.data = data
      } catch (e) {
        if (requestGeneration !== refreshGeneration) return
        this.error = e instanceof Error ? e.message : String(e)
      } finally {
        if (requestGeneration === refreshGeneration) this.loading = false
      }
    },
  },
})
