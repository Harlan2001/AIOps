<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{ option: echarts.EChartsOption }>()

const el = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
let observer: ResizeObserver | null = null

function render() {
  chart?.setOption(props.option, true)
}

onMounted(() => {
  if (el.value) {
    chart = echarts.init(el.value)
    render()
    // 监听容器自身尺寸：侧栏折叠仅改变父容器宽度、不触发 window.resize，
    // 用 ResizeObserver 保证 canvas 跟随重排，避免留白或裁切。
    observer = new ResizeObserver(() => {
      chart?.resize()
    })
    observer.observe(el.value)
  }
})

watch(() => props.option, render, { deep: true })

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
  chart?.dispose()
  chart = null
})
</script>

<template>
  <div ref="el" class="base-chart" />
</template>

<style scoped>
.base-chart {
  width: 100%;
  height: 320px;
}
</style>
