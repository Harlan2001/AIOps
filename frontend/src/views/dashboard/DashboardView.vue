<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { EChartsOption } from 'echarts'

import { getRules } from '@/api/meta'
import { ApiError } from '@/api/client'
import BaseChart from '@/components/BaseChart.vue'
import type { RulesResponse } from '@/types/contract'

const data = ref<RulesResponse | null>(null)
const loading = ref(false)
const errorMsg = ref('')

const keywordChart = computed<EChartsOption>(() => {
  const rules = data.value?.rules ?? []
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 60, right: 20, top: 30, bottom: 80 },
    xAxis: {
      type: 'category',
      data: rules.map((r) => r.title),
      axisLabel: { interval: 0, rotate: 35, fontSize: 11 },
    },
    yAxis: { type: 'value', name: '关键词数' },
    series: [
      {
        type: 'bar',
        data: rules.map((r) => r.keywords.length),
        itemStyle: { color: '#1677ff' },
      },
    ],
  }
})

onMounted(loadData)

async function loadData() {
  loading.value = true
  try {
    data.value = await getRules()
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError
        ? `加载失败（${e.status}）：${e.message}`
        : '加载异常'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <a-spin :spinning="loading">
    <a-row :gutter="16">
      <a-col :span="8">
        <a-card>
          <a-statistic title="规则类型总数" :value="data?.total ?? 0" />
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card>
          <a-statistic
            title="噪音关键词数"
            :value="data?.noise_keywords.length ?? 0"
          />
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card>
          <a-statistic
            title="规则覆盖率"
            :formatter="() => '离线扫描'"
          />
          <p class="note">{{ data?.coverage }}</p>
        </a-card>
      </a-col>
    </a-row>

    <a-alert
      v-if="errorMsg"
      type="error"
      show-icon
      :message="errorMsg"
      class="block"
    />

    <a-card title="各规则关键词数量" class="block">
      <BaseChart :option="keywordChart" />
    </a-card>

    <a-card title="趋势 / 降级率 / 高频问题排行" class="block">
      <a-empty description="该类指标依赖诊断结果持久化，待数据层具备后接入" />
    </a-card>
  </a-spin>
</template>

<style scoped>
.block {
  margin-top: 16px;
}

.note {
  margin-top: 8px;
  color: #888;
  font-size: 12px;
}
</style>
