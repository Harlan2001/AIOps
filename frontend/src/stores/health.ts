import { defineStore } from 'pinia'

import { getHealth } from '@/api/meta'
import type { HealthStatus } from '@/types/contract'

interface HealthState {
  data: HealthStatus | null
  loading: boolean
  error: string
}

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
      this.loading = true
      this.error = ''
      try {
        this.data = await getHealth()
      } catch (e) {
        this.error = e instanceof Error ? e.message : String(e)
      } finally {
        this.loading = false
      }
    },
  },
})
