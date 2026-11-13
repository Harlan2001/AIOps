<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { EChartsOption } from 'echarts'

import { getRules } from '@/api/meta'
import { getDiagnosisStats } from '@/api/diagnoses'
import { ApiError } from '@/api/client'
import BaseChart from '@/components/BaseChart.vue'
import { labelNull } from '@/utils/label'
import type { DiagStats, RulesResponse } from '@/types/contract'

const data = ref<RulesResponse | null>(null)
const loading = ref(false)
const errorMsg = ref('')

const stats = ref<DiagStats | null>(null)
const statsLoading = ref(false)
const statsError = ref('')

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

function label(key: string | null): string {
  return labelNull(key)
}

const trendChart = computed<EChartsOption>(() => {
  const rows = stats.value?.by_date ?? []
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 30, bottom: 40 },
    xAxis: { type: 'category', data: rows.map((r) => label(r.key)) },
    yAxis: { type: 'value', name: '诊断量' },
    series: [
      {
        type: 'line',
        smooth: true,
        data: rows.map((r) => r.count),
        itemStyle: { color: '#1677ff' },
      },
    ],
  }
})

const topTypeChart = computed<EChartsOption>(() => {
  const rows = stats.value?.top_types ?? []
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 110, right: 30, top: 20, bottom: 30 },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: rows.map((r) => label(r.key)) },
    series: [
      {
        type: 'bar',
        data: rows.map((r) => r.count),
        itemStyle: { color: '#13a8a8' },
      },
    ],
  }
})

const classChart = computed<EChartsOption>(() => {
  const rows = stats.value?.by_class ?? []
  return {
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        data: rows.map((r) => ({ name: label(r.key), value: r.count })),
      },
    ],
  }
})

const abnormalPct = computed(() =>
  stats.value ? (stats.value.abnormal_rate * 100).toFixed(1) : '0.0')

onMounted(() => {
  loadData()
  loadStats()
})

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

async function loadStats() {
  statsLoading.value = true
  statsError.value = ''
  try {
    stats.value = await getDiagnosisStats()
  } catch (e) {
    // 存储未就绪（表未建/未开启）：友好提示而非整页报错
    stats.value = null
    statsError.value =
      e instanceof ApiError
        ? `诊断结果存储未就绪（${e.status}）：开启持久化后展示趋势与统计`
        : '诊断结果存储未就绪，开启持久化后展示趋势与统计'
  } finally {
    statsLoading.value = false
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

    <a-spin :spinning="statsLoading">
      <a-row :gutter="16" class="block">
        <a-col :span="6">
          <a-card>
            <a-statistic title="累计诊断" :value="stats?.total ?? 0" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic
              title="诊断异常率"
              :value="Number(abnormalPct)"
              suffix="%"
            />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic title="LLM 升级数" :value="stats?.escalated ?? 0" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic title="已人工标注" :value="stats?.annotated ?? 0" />
          </a-card>
        </a-col>
      </a-row>

      <a-alert
        v-if="statsError"
        type="info"
        show-icon
        :message="statsError"
        class="block"
      />

      <template v-if="stats && stats.total > 0">
        <a-card title="诊断量趋势" class="block">
          <BaseChart :option="trendChart" />
        </a-card>
        <a-row :gutter="16" class="block">
          <a-col :span="14">
            <a-card title="高频问题 TOP">
              <BaseChart :option="topTypeChart" />
            </a-card>
          </a-col>
          <a-col :span="10">
            <a-card title="诊断分类分布">
              <BaseChart :option="classChart" />
            </a-card>
          </a-col>
        </a-row>
      </template>
    </a-spin>
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
