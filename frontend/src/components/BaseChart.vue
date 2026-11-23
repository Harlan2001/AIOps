<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { BarChartOutlined, TableOutlined } from '@ant-design/icons-vue'

export interface ChartDatum {
  label: string
  value: number
}

const props = withDefaults(defineProps<{
  option: echarts.EChartsOption
  title: string
  rows?: ChartDatum[]
  seriesName?: string
  loading?: boolean
  height?: number
  emptyText?: string
}>(), {
  rows: () => [],
  seriesName: '数量',
  loading: false,
  height: 300,
  emptyText: '当前筛选范围内暂无数据',
})

const el = ref<HTMLDivElement | null>(null)
const showTable = ref(false)
let chart: echarts.ECharts | null = null
let observer: ResizeObserver | null = null
const isEmpty = computed(() => props.rows.length === 0)

function render() {
  chart?.setOption(props.option, true)
}

onMounted(() => {
  if (!el.value) return
  chart = echarts.init(el.value)
  render()
  observer = new ResizeObserver(() => chart?.resize())
  observer.observe(el.value)
})

watch(() => props.option, render, { deep: true })
watch(showTable, async (visible) => {
  if (!visible) {
    await nextTick()
    chart?.resize()
  }
})

onBeforeUnmount(() => {
  observer?.disconnect()
  chart?.dispose()
  chart = null
})
</script>

<template>
  <figure class="chart-container" :aria-busy="loading">
    <div class="chart-toolbar">
      <span v-if="loading && rows.length" class="refresh-copy">正在更新，当前保留上次数据</span>
      <a-button v-if="rows.length" size="small" type="text" @click="showTable = !showTable">
        <TableOutlined v-if="!showTable" />
        <BarChartOutlined v-else />
        {{ showTable ? '查看图表' : '数据表' }}
      </a-button>
    </div>

    <a-empty v-if="isEmpty && !loading" :description="emptyText" />
    <a-skeleton v-else-if="isEmpty && loading" active :paragraph="{ rows: 5 }" />

    <div v-show="!isEmpty && !showTable" :class="{ 'is-refreshing': loading }">
      <div
        ref="el"
        class="base-chart"
        role="img"
        :aria-label="`${title}，可切换数据表查看全部数值`"
        :style="{ height: `${height}px` }"
      />
    </div>

    <div v-if="!isEmpty && showTable" class="chart-table-wrap">
      <table class="chart-table">
        <caption>{{ title }} · 数据表</caption>
        <thead><tr><th scope="col">项目</th><th scope="col">{{ seriesName }}</th></tr></thead>
        <tbody>
          <tr v-for="row in rows" :key="row.label">
            <td>{{ row.label }}</td>
            <td>{{ row.value.toLocaleString('zh-CN') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </figure>
</template>

<style scoped>
.chart-container {
  min-width: 0;
  margin: 0;
}

.chart-toolbar {
  display: flex;
  min-height: 32px;
  gap: 12px;
  align-items: center;
  justify-content: flex-end;
}

.refresh-copy {
  margin-right: auto;
  color: var(--text-muted);
  font-size: 12px;
}

.base-chart {
  width: 100%;
}

.is-refreshing {
  opacity: 0.58;
}

.chart-table-wrap {
  max-height: 360px;
  overflow: auto;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
}

.chart-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.chart-table caption {
  padding: 12px 14px;
  color: var(--text-secondary);
  background: var(--surface-subtle);
  font-weight: 600;
}

.chart-table th,
.chart-table td {
  padding: 10px 14px;
  border-top: 1px solid var(--border-soft);
}

.chart-table th {
  color: var(--text-secondary);
  background: #fbfcfe;
  font-size: 12px;
}

.chart-table td:last-child,
.chart-table th:last-child {
  width: 120px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>
