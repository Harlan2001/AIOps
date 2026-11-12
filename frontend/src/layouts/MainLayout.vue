<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DashboardOutlined,
  MedicineBoxOutlined,
  TableOutlined,
} from '@ant-design/icons-vue'

import { useHealthStore } from '@/stores/health'

const route = useRoute()
const router = useRouter()
const health = useHealthStore()

const selectedKeys = computed(() => [route.name as string])

// 四态映射：加载中 / 正常 / 降级 / 请求失败（未知），避免加载失败时仍显示绿色。
const badgeStatus = computed<
  'processing' | 'success' | 'warning' | 'error'
>(() => {
  if (health.loading) return 'processing'
  if (health.error || !health.data) return 'error'
  return health.isDegraded ? 'warning' : 'success'
})

const badgeText = computed(() => {
  if (health.loading) return '检测中…'
  if (health.error || !health.data) return '健康检查失败'
  return health.isDegraded ? '服务降级' : '服务正常'
})

const menuItems = [
  { key: 'diagnose', icon: MedicineBoxOutlined, label: '单条诊断' },
  { key: 'batch', icon: TableOutlined, label: '批量回放' },
  { key: 'dashboard', icon: DashboardOutlined, label: '管理看板' },
]

function onMenuClick({ key }: { key: string }) {
  router.push({ name: key })
}

// 健康状态轮询间隔：SPA 长时间打开时也能反映数据库/网络的故障与恢复。
const POLL_INTERVAL = 30000
let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  health.refresh()
  timer = setInterval(() => {
    health.refresh()
  }, POLL_INTERVAL)
})

// 路由切换时立即刷新一次，避免展示旧状态。
watch(
  () => route.name,
  () => {
    health.refresh()
  },
)

// 组件卸载时清理定时器，防止内存泄漏与卸载后更新。
onBeforeUnmount(() => {
  if (timer !== null) {
    clearInterval(timer)
    timer = null
  }
})
</script>

<template>
  <a-layout class="app-layout">
    <a-sider breakpoint="lg" collapsible>
      <div class="logo">DIMPLE AIOps</div>
      <a-menu
        theme="dark"
        mode="inline"
        :selected-keys="selectedKeys"
        @click="onMenuClick"
      >
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </a-menu-item>
      </a-menu>
    </a-sider>

    <a-layout>
      <a-header class="app-header">
        <span class="page-title">{{ route.meta.title }}</span>
        <a-badge :status="badgeStatus" :text="badgeText" />
      </a-header>
      <a-content class="app-content">
        <router-view />
      </a-content>
    </a-layout>
  </a-layout>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.logo {
  height: 48px;
  margin: 16px;
  color: #fff;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 1px;
}

.app-header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
}

.app-content {
  margin: 24px;
}
</style>
