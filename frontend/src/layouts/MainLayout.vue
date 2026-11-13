<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DashboardOutlined,
  HistoryOutlined,
  MedicineBoxOutlined,
  TableOutlined,
} from '@ant-design/icons-vue'

import { useHealthStore } from '@/stores/health'

const route = useRoute()
const router = useRouter()
const health = useHealthStore()

const selectedKeys = computed(() => [route.name as string])
const collapsed = ref(false)

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
  { key: 'history', icon: HistoryOutlined, label: '历史诊断' },
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
    <a-sider
      v-model:collapsed="collapsed"
      breakpoint="lg"
      class="app-sider"
    >
      <div class="logo" :class="{ 'logo-collapsed': collapsed }">
        <div class="logo-mark">AI</div>
        <div class="logo-text">
          <span class="logo-title">DIMPLE AIOps</span>
          <span class="logo-sub">智能诊断工作台</span>
        </div>
      </div>
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

.app-sider {
  background: linear-gradient(180deg, #0f2f5c 0%, #0b213f 100%);
}

.logo {
  margin: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.08);
}

.logo-mark {
  width: 36px;
  height: 36px;
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: linear-gradient(135deg, #1677ff, #38a3ff);
  color: #fff;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-title {
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.5px;
}

.logo-sub {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  margin-top: 2px;
}

.logo-collapsed {
  justify-content: center;
  padding: 8px;
}

.logo-collapsed .logo-text {
  display: none;
}

.app-header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 0 rgba(15, 47, 92, 0.08);
}

.page-title {
  font-size: 17px;
  font-weight: 700;
  color: #1f2d3d;
}

.app-content {
  margin: 24px;
}
</style>
